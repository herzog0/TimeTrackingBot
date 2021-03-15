from telegram import Update
from telegram.ext import CallbackContext, DispatcherHandlerStop

from src.communication.basics import send_message, send_markup_msg
from src.dynamo_db import create_or_reset_user, get_user_states, ChatState
from src.handlers.language import request_language_setup
from src.support.logger import logger
from src.support.m17n import strings
from src.support.options_kbd import options_kbd

_sensitive_states = [
    ChatState.CLOCKED_IN,
    ChatState.CLOCK_OUT_UNREPORTED
]


def start(update: Update, context: CallbackContext):
    _, chat_state = get_user_states(str(update.effective_message.chat_id))
    if chat_state in _sensitive_states:
        logger.debug(f"Not letting user perform a restart because they're in {chat_state} state")
        send_markup_msg(update, strings()['start:prohibit'], options_kbd(strings()))
    else:
        create_or_reset_user(str(update.message.chat_id))
        request_language_setup(update, context)
    raise DispatcherHandlerStop
