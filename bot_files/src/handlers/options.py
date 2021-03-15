from telegram import Update
from telegram.ext import CallbackContext, DispatcherHandlerStop

from src.communication.basics import send_markup_msg, send_markdown_msg, edit_message
from src.handlers.delete_all_data import delete
from src.handlers.edit import edit_choice_selector
from src.support.help_kbd import help_inline_kdb
from src.support.m17n import strings
from src.support.options_kbd import options_inline_kdb


def handle_chosen_option(update: Update, context: CallbackContext):
    if update.callback_query.data == "option#edit":
        return edit_choice_selector(update, context)

    elif update.callback_query.data == "option#help":
        return edit_message(update, strings()['help'], True, help_inline_kdb())

    elif update.callback_query.data == "option#source":
        return edit_message(update, strings()['source'], True)

    elif update.callback_query.data == "option#delete":
        return delete(update, context)


def options(update: Update, context: CallbackContext):
    send_markup_msg(update, strings()['options:choose'], options_inline_kdb())
    raise DispatcherHandlerStop
