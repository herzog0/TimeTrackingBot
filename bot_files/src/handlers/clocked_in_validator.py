from datetime import datetime
from typing import List

from telegram import Update, ForceReply
from telegram.error import BadRequest
from telegram.ext import CallbackContext, DispatcherHandlerStop

from src.communication.basics import send_message, send_markup_msg
from src.dynamo_db import today_entries, get_user_info, set_msg_reply_id, that_day_entries as _that_day_entries, \
    create_full_entry, remove_msg_reply_id
from src.support.logger import logger
from src.support.m17n import strings
from src.support.options_kbd import options_kbd


def compile_entries(entries: List[dict]) -> str:
    clock_in: bool = True
    phrases = []
    entries = sorted(entries, key=lambda k: k['date'])
    for entry in entries:
        _p = f"regx*x{strings()['validator:clockin']}:regx*x " \
            if clock_in \
            else f"regx*x{strings()['validator:clockout']}:regx*x "
        _p += datetime.fromisoformat(entry['date']).strftime('%H:%M')
        phrases.append(_p)
        if 'description' in entry:
            phrases.append(entry['description'] + '\n')
        clock_in = not clock_in
    return "\n".join(phrases)


def generate_reply(update: Update, context: CallbackContext, clocked_in_date: str) -> None:
    chat_id = update.effective_chat.id
    that_day_entries = _that_day_entries(chat_id, clocked_in_date)

    compiled_entries = [
        strings()['request:warning'],
        datetime.fromisoformat(clocked_in_date).strftime('%d/%m/%Y') + '\n',
        compile_entries(that_day_entries) + '\n',
        strings()['request:missing_entry']
    ]

    msg = send_markup_msg(update, "\n".join(compiled_entries), ForceReply(), True)
    set_msg_reply_id(chat_id, msg.message_id)


def ensure_valid_clocked_in(update: Update, context: CallbackContext):
    # if the chat_state is clocked_in but there are no records today, this means that
    # the user forgot to clock out the other day.
    chat_id = update.effective_chat.id
    if len(today_entries(chat_id)) == 0:
        user_info = get_user_info(chat_id)
        clocked_in_date = datetime.fromisoformat(user_info['clocked_in_date'])

        # we are in an inconsistent state
        # check if there's any msg waiting for a reply
        # if not, create one
        try:
            msg_id = int(user_info['msg_reply_id'])
            if not update.effective_message.reply_to_message \
                    or update.effective_message.reply_to_message.message_id != msg_id:
                try:
                    update.effective_message.bot.delete_message(chat_id=chat_id, message_id=msg_id)
                except BadRequest:
                    logger.warn('The message to be replied has been deleted by the user, but we\'ll try again')
                generate_reply(update, context, clocked_in_date.isoformat())
                raise DispatcherHandlerStop

            else:
                msg = update.effective_message.text
                time = msg.split('\n')[0]
                if len(time) != 5:  # hh:mm
                    raise ValueError('It should be in format hh:mm')

                hour, minute = int(time.split(':')[0]), int(time.split(':')[1])
                clock_out_date = clocked_in_date.replace(hour=hour, minute=minute,
                                                         microsecond=clocked_in_date.microsecond + 1).isoformat()
                description = msg.split('\n')[0].strip()

                if len(description) == 0:
                    raise ValueError('Description should not be empty')

                if clock_out_date < clocked_in_date.isoformat():
                    raise ValueError('Clock out date must be greater than the clock in date')

                create_full_entry(chat_id, clock_out_date, description)
                remove_msg_reply_id(chat_id)
                send_markup_msg(update, strings()['request:acknowledgment'], options_kbd(strings()))
                raise DispatcherHandlerStop
        except DispatcherHandlerStop:
            raise DispatcherHandlerStop
        except Exception as e:
            logger.error(e)
            generate_reply(update, context, clocked_in_date.isoformat())
            raise DispatcherHandlerStop
        finally:
            raise DispatcherHandlerStop
