from enum import Enum

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import CallbackContext, DispatcherHandlerStop
from datetime import datetime, timedelta

from src.communication.basics import send_markup_msg, send_document, edit_message
from src.dynamo_db import today_entries, yesterday_entries, week_entries, last_week_entries, last_month_entries, \
    month_entries
from src.support.escapers import remove_regxx
from src.support.m17n import strings
from src.support.utils import seconds_to_str


def report_compiler(_entries: list):
    if len(_entries) == 0:
        return None

    # Converting entry iso dates to datetime objects
    def _ec(_e):
        _e['date'] = datetime.fromisoformat(_e['date'])

    # map just creates a map object, you have to iterate over it to actually do the mapping
    list(map(_ec, _entries))

    # Sorting entries based on date
    entries = list(sorted(_entries, key=lambda k: k['date']))

    # Ensuring an even length to loop through
    # Screw the last clock in event that has no clock out yet
    final = len(entries) if len(entries) % 2 == 0 else len(entries) - 1
    entries = entries[:final]

    if len(entries) == 0:
        return None

    # Setup
    total_accum = timedelta(seconds=0)
    day_accum = timedelta(seconds=0)
    paragraphs = []
    phrases = []
    curr_day: datetime = entries[0]['date']

    def insert_day_total():
        phrases.insert(0, f"regx*x{curr_day.strftime('%d/%m/%Y')} - {strings()[curr_day.strftime('%A')]}regx*x")
        phrases.append(f"regx_xregx_x{strings()['report:total_of_day']}: "
                       f"regx*x{seconds_to_str(day_accum.total_seconds())}regx*xregx_xregx_x\n\n")

    # The loop.
    for i in range(0, final, 2):
        f_entry = entries[i]
        s_entry = entries[i + 1]

        if curr_day.day != f_entry['date'].day:
            insert_day_total()
            paragraph = "\n".join(phrases)
            paragraphs.append(paragraph)
            # cleanup
            day_accum = timedelta(seconds=0)
            curr_day = f_entry['date']
            phrases = []

        partial_accum = s_entry['date'] - f_entry['date']
        day_accum += partial_accum
        total_accum += partial_accum

        description = s_entry['description'] if 'description' in s_entry else strings()['report:description:not_found']
        phrase = f"{f_entry['date'].strftime('%H:%M')} - {s_entry['date'].strftime('%H:%M')} => " \
                 f"regx*x{seconds_to_str(partial_accum.total_seconds())}regx*x\n" \
                 f"regx_x{description}regx_x"
        phrases.append(phrase)

    insert_day_total()
    paragraph = "\n".join(phrases)
    paragraphs.append(paragraph)

    paragraphs.append(f"{strings()['report:total_of_period']}: "
                      f"regx*x{seconds_to_str(total_accum.total_seconds())}regx*x\n\n")

    return "\n\n".join(paragraphs)


def generate_report(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if update.callback_query.data == "report#today":
        entries = today_entries(chat_id)
        return report_compiler(entries)

    elif update.callback_query.data == "report#yesterday":
        entries = yesterday_entries(chat_id)
        return report_compiler(entries)

    elif update.callback_query.data == "report#week":
        entries = week_entries(chat_id)
        return report_compiler(entries)

    elif update.callback_query.data == "report#month":
        entries = month_entries(chat_id)
        return report_compiler(entries)

    elif update.callback_query.data == "report#last_week":
        entries = last_week_entries(chat_id)
        return report_compiler(entries)

    elif update.callback_query.data == "report#last_month":
        entries = last_month_entries(chat_id)
        return report_compiler(entries)


def choose_report(update: Update, context: CallbackContext) -> None:
    class InlineKeyboardOptions(Enum):
        TODAY = strings()['button:today']
        YESTERDAY = strings()['button:yesterday']
        WEEK = strings()['button:report:week']
        MONTH = strings()['button:report:month']
        LAST_WEEK = strings()['button:report:last_week']
        LAST_MONTH = strings()['button:report:last_month']

    inline_keyboard_buttons = [
        [InlineKeyboardButton(InlineKeyboardOptions.TODAY.value, callback_data="report#today")],
        [InlineKeyboardButton(InlineKeyboardOptions.YESTERDAY.value, callback_data="report#yesterday")],
        [InlineKeyboardButton(InlineKeyboardOptions.WEEK.value, callback_data="report#week")],
        [InlineKeyboardButton(InlineKeyboardOptions.MONTH.value, callback_data="report#month")],
        [InlineKeyboardButton(InlineKeyboardOptions.LAST_WEEK.value, callback_data="report#last_week")],
        [InlineKeyboardButton(InlineKeyboardOptions.LAST_MONTH.value, callback_data="report#last_month")],
    ]

    reply_markup = InlineKeyboardMarkup(inline_keyboard_buttons)
    send_markup_msg(update, strings()["report:period:choose"], reply_markup)
    raise DispatcherHandlerStop


def show_report(update: Update, context: CallbackContext) -> None:
    msg = generate_report(update, context)
    if msg is None:
        edit_message(update, strings()['report:choice:empty'])
        raise DispatcherHandlerStop
    try:
        edit_message(update, msg, True)
    except BadRequest:
        edit_message(update, strings()['report:choice:too_many_chars'])
        send_document(update, bytes(remove_regxx(msg), 'utf-8'), f"{update.callback_query.data}.txt")
    finally:
        raise DispatcherHandlerStop


bla = [{'chat_id': '154885116', 'date': '2021-03-05T19:58:02.142986'},
       {'chat_id': '154885116',
        'date': '2021-03-05T20:00:05.704890',
        'description': 'desc 1'},
       {'chat_id': '154885116', 'date': '2021-03-05T20:05:12.507041'},
       {'chat_id': '154885116',
        'date': '2021-03-05T20:10:16.820838',
        'description': 'desc 2'},
       {'chat_id': '154885116', 'date': '2021-03-05T20:15:22.992281'},
       {'chat_id': '154885116',
        'date': '2021-03-05T20:20:25.612673',
        'description': 'desc 3'},
       {'chat_id': '154885116', 'date': '2021-03-05T20:25:31.910612'},
       {'chat_id': '154885116',
        'date': '2021-03-05T20:30:35.722838',
        'description': 'desc 4'},
       {'chat_id': '154885116', 'date': '2021-03-05T20:35:42.456275'}]

if __name__ == '__main__':
    pass
    # result = te(bla)
    # print(result)
