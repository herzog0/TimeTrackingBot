from telegram import Update
from telegram.ext import CallbackContext, DispatcherHandlerStop

from src.communication.basics import send_message
from src.support.m17n import strings


def request_start(update: Update, context: CallbackContext):
    send_message(update, strings()["request:start"])
    raise DispatcherHandlerStop
