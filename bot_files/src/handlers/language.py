import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, DispatcherHandlerStop

from src.communication.basics import send_markup_msg, edit_message, send_message
from src.dynamo_db import Language, set_language, SetupState, get_user_states, set_timezone
from src.support.logger import logger
from src.support.m17n import strings, set_strings
from src.support.options_kbd import options_kbd

_lang_inline_keyboard_buttons = [
    [InlineKeyboardButton('English', callback_data='language#en')],
    [InlineKeyboardButton('Português (Br)', callback_data='language#pt')],
]

_callback_query_options = [
    'language#en',
    'language#pt'
]


def request_language_setup(update: Update, context: CallbackContext) -> None:
    setup_state, _ = get_user_states(str(update.effective_chat.id))
    if setup_state is not SetupState.LANGUAGE_NOT_SET:
        logger.error('request_language_setup being called when state is not LANGUAGE_NOT_SET')
        return None

    if update.callback_query is None or update.callback_query.data not in _callback_query_options:
        reply_markup = InlineKeyboardMarkup(_lang_inline_keyboard_buttons)
        send_markup_msg(update, strings()["language:choose"], reply_markup)
    else:
        query = update.callback_query

        lang = Language(query.data.split("#")[1])
        if lang is Language.ENGLISH:
            set_strings(force_lang=Language.ENGLISH)
        else:
            set_strings(force_lang=Language.PORTUGUESE)

        set_language(chat_id=str(update.callback_query.message.chat.id),
                     lang=lang,
                     next_state=SetupState.TIMEZONE_NOT_SET)

        try:
            set_timezone(str(update.effective_chat.id), int(os.environ.get('TIMEZONE_SECONDS_OFFSET', None)),
                         SetupState.NONE)
            send_markup_msg(update, strings()['setup:complete'], options_kbd(strings()))
        except Exception as e:
            logger.warn(e)
            logger.warn('TIMEZONE_SECONDS_OFFSET not present or in wrong format.\n'
                        'Switching to fallback mode with google maps api.')
            edit_message(update, strings()['language:set'])
            send_message(update, strings()['timezone:request'])

    raise DispatcherHandlerStop
