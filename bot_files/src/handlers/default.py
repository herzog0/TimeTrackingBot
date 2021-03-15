from telegram import Update
from telegram.ext import CallbackContext, DispatcherHandlerStop

from src.communication.basics import send_markup_msg
from src.support.m17n import strings
from src.support.options_kbd import options_kbd


def default(update: Update, context: CallbackContext):
    send_markup_msg(update, strings()['default'], options_kbd(strings()))
    raise DispatcherHandlerStop
