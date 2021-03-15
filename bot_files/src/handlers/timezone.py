import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, DispatcherHandlerStop
from datetime import timedelta

from src.communication.basics import send_message, send_markup_msg
from src.dynamo_db import get_user_states, SetupState, set_timezone
from src.google_maps.geocode_functions import get_address_and_timezone_by_name, LocationNotFoundException
from src.support.logger import logger
from src.support.m17n import strings
from src.support.options_kbd import options_kbd

_callback_query_options = [
    'timezone#yes',
    'timezone#no'
]


def request_timezone_setup(update: Update, context: CallbackContext) -> None:
    state, _ = get_user_states(str(update.effective_chat.id))
    if state is not SetupState.TIMEZONE_NOT_SET:
        logger.error('request_timezone_setup being called when state is not TIMEZONE_NOT_SET')
        return

    if update.message is not None:
        try:
            tz = get_address_and_timezone_by_name(update.message.text)
            is_negative = "-" if tz['offset'] < 0 else ""
            pretty_offset = is_negative + str(timedelta(seconds=abs(tz['offset'])))[:-3]
            _inline_keyboard_buttons = [[
                InlineKeyboardButton(strings()['button:yes'], callback_data=f"timezone#yes#{pretty_offset}"),
                InlineKeyboardButton(strings()['button:no'], callback_data='timezone#no'),
            ]]
            reply_markup = InlineKeyboardMarkup(_inline_keyboard_buttons)
            tz_msg = f"regx*x{tz['timezone_id']}regx*x \nregx*xUTC{pretty_offset}regx*x\n"
            full_msg = strings()["timezone:location:confirm"].format(tz_msg)
            send_markup_msg(update, full_msg, reply_markup, True)
        except LocationNotFoundException:
            send_message(update, strings()['timezone:location:not_found'])
    else:
        query = update.callback_query
        if not any(cb_option in query.data for cb_option in _callback_query_options):
            send_message(update, strings()['timezone:request'])
        else:
            if 'timezone#no' in query.data:
                send_message(update, strings()['timezone:request'])
            else:
                pretty_offset = query.data.split('#')[-1]
                hours, minutes = map(int, pretty_offset.split(':'))
                minutes = minutes if hours >= 0 else minutes * (-1)
                offset = (hours * 60 * 60) + (minutes * 60)
                set_timezone(str(update.effective_chat.id), offset, SetupState.NONE)
                send_markup_msg(update, strings()['setup:complete'], options_kbd(strings()))
    raise DispatcherHandlerStop
