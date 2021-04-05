from telegram import Update
from telegram.ext import CallbackContext, DispatcherHandlerStop

from src.communication.basics import edit_message, send_markup_msg
from src.support.help_kbd import help_inline_kdb
from src.support.m17n import strings


def help_message(update: Update, context: CallbackContext):
    send_markup_msg(update, strings()['help'], help_inline_kdb(), True)
    raise DispatcherHandlerStop


def handle_help(update: Update, context: CallbackContext):
    if update.callback_query.data == 'help#clockin':
        edit_message(update, strings()['help:clockin'], True)

    elif update.callback_query.data == 'help#report':
        edit_message(update, strings()['help:report'], True)

    elif update.callback_query.data == 'help#edit':
        edit_message(update, strings()['help:edit'], True)

    elif update.callback_query.data == 'help#deleteall':
        edit_message(update, strings()['help:deleteall'], True)

    elif update.callback_query.data == 'help#issue':
        edit_message(update, strings()['help:issue'], True)

    raise DispatcherHandlerStop
