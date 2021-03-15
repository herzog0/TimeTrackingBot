from datetime import datetime, date, time, timedelta
from typing import List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, DispatcherHandlerStop
from telegram.error import BadRequest
from itertools import groupby

from src.communication.basics import send_markdown_msg, edit_message, send_markup_msg
from src.dynamo_db import today_entries, yesterday_entries, that_day_entries, set_chat_state, ChatState, set_edit_day, \
    get_user_info, create_full_entry, cancel_edit as _cancel_edit, delete_that_day_entries
from src.support.escapers import aggressive_escaper
from src.support.logger import logger
from src.support.m17n import strings


def cancel_edit(update: Update, context: CallbackContext):
    _cancel_edit(update.effective_chat.id)
    send_markdown_msg(update, strings()['cancelled'])
    raise DispatcherHandlerStop


def edit_choice_selector(update: Update, context: CallbackContext):
    kbd = [
        [InlineKeyboardButton(strings()['button:today'], callback_data='edit#today')],
        [InlineKeyboardButton(strings()['button:yesterday'], callback_data='edit#yesterday')],
        [InlineKeyboardButton(strings()['button:other'], callback_data='edit#other')],
    ]
    try:
        edit_message(update,
                     strings()['edit:choose:message'],
                     True,
                     InlineKeyboardMarkup(kbd))
    except BadRequest as e:
        send_markup_msg(
            update,
            strings()['edit:choose:message'],
            InlineKeyboardMarkup(kbd),
            True,
        )
    raise DispatcherHandlerStop


def user_selected_edit_day(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_info = get_user_info(chat_id)
    offset = user_info['utc_delta_seconds']
    today = datetime.combine(datetime.utcnow() + timedelta(seconds=int(offset)), time())
    if update.callback_query.data == 'edit#today':
        entries = today_entries(chat_id)
        if len(entries) % 2 != 0:
            send_markdown_msg(update, strings()['edit:incomplete_day'])
            raise DispatcherHandlerStop
        set_edit_day(chat_id, today.isoformat())
        edit_entry_request(update, context, entries)

    elif update.callback_query.data == 'edit#yesterday':
        entries = yesterday_entries(chat_id)
        set_edit_day(chat_id, (today - timedelta(days=1)).isoformat())
        edit_entry_request(update, context, entries)

    elif update.callback_query.data == 'edit#other':
        send_markdown_msg(update, strings()['edit:request_day'])
        set_chat_state(chat_id, ChatState.AWAITING_EDIT_DAY)

    raise DispatcherHandlerStop


def validate_picked_day(update: Update, context: CallbackContext):
    try:
        chat_id = update.effective_chat.id
        day, month, year = map(int, update.effective_message.text.split('/'))
        _date = datetime.combine(date(year=year, month=month, day=day), time())
        entries = that_day_entries(chat_id, _date.isoformat())
        set_edit_day(chat_id, _date.isoformat())
        edit_entry_request(update, context, entries)
    except DispatcherHandlerStop:
        raise
    except Exception as e:
        logger.error(e)
        msg = "\n".join([
            strings()['edit:request:date:wrong_format'],
            strings()['edit:request:date_model'],
            strings()['edit:suggest:cancel'],
        ])
        send_markdown_msg(update, msg)
    finally:
        raise DispatcherHandlerStop


def compile_entries(entries: List[dict]) -> str:
    phrases = []
    entries = sorted(entries, key=lambda k: k['date'])
    for entry in entries:
        _p = datetime.fromisoformat(entry['date']).strftime('%H:%M')
        phrases.append(_p)
        if 'description' in entry:
            phrases.append(entry['description'] + '\n')
    return "\n".join(phrases)


def parse_and_validate_chunk(chunk: List[str],
                             last_clock_out: datetime,
                             editing_day: datetime,
                             chat_id: str):
    def parse_time(_time: str):
        hour, minute = int(_time.split(':')[0]), int(_time.split(':')[1])
        return editing_day.replace(hour=hour, minute=minute)

    start = parse_time(chunk[0])
    end = parse_time(chunk[1])
    chunk = chunk[2:]
    if start > end:
        raise ValueError('start time should be less than end time')

    if end < last_clock_out:
        raise ValueError('entries are not in chronological order')

    return [
               {
                   'chat_id': chat_id,
                   'date': start.isoformat()
               },
               {
                   'chat_id': chat_id,
                   'date': end.isoformat(),
                   'description': ' '.join(chunk)
               }
           ], end


def validate_edited_registries(update: Update, context: CallbackContext):
    try:
        chat_id = update.effective_chat.id
        user_info = get_user_info(chat_id)
        editing_day = datetime.fromisoformat(user_info['editing_day'])
        offset = user_info['utc_delta_seconds']
        _now = datetime.utcnow() + timedelta(seconds=int(offset))

        split_message = (update.effective_message.text + '\n').split('\n')
        i = (list(g) for _, g in groupby(split_message, key=''.__ne__))
        chunks = [a + b for a, b in zip(i, i)]
        last_clock_out = editing_day - timedelta(microseconds=1)
        entries = []
        for chunk in chunks:
            _e, last_clock_out = parse_and_validate_chunk(chunk, last_clock_out, editing_day, chat_id)
            entries = [*entries, *_e]

        # delete before inserting new ones of that day
        delete_that_day_entries(chat_id, editing_day)
        list(map(lambda _e: create_full_entry(**_e), entries))
        send_markdown_msg(update, strings()['edit:done'])
        _cancel_edit(chat_id)
        raise DispatcherHandlerStop
    except DispatcherHandlerStop:
        raise
    except Exception as e:
        logger.error(f"User sent data in wrong format {e}")
        msg = "\n".join([
            strings()['edit:request:entry:wrong_format'],
            strings()['edit:request:model'],
            strings()['edit:suggest:cancel'],
        ])
        send_markdown_msg(update, msg)
    finally:
        raise DispatcherHandlerStop


def edit_entry_request(update: Update, context: CallbackContext, entries: List[dict]):
    chat_id = update.effective_chat.id
    compiled_entries = compile_entries(entries)
    compiled_entries = aggressive_escaper(compiled_entries)
    if len(compiled_entries) == 0:
        send_markdown_msg(update, strings()['edit:request:empty'])
    else:
        send_markdown_msg(update, compiled_entries)
        send_markdown_msg(update, strings()['edit:request:not_empty'])
    send_markdown_msg(update, strings()['edit:request:instructions:1'])
    send_markdown_msg(update, strings()['edit:request:model'])
    send_markdown_msg(update, strings()['edit:request:instructions:2'])
    set_chat_state(chat_id, ChatState.AWAITING_EDITED_REGISTRIES)
    raise DispatcherHandlerStop
