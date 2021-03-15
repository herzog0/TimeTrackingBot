from telegram import Update
from telegram.ext import CallbackContext

from src.handlers.delete_all_data import delete
from src.handlers.edit import user_selected_edit_day
from src.handlers.help import handle_help
from src.handlers.language import request_language_setup
from src.handlers.options import handle_chosen_option
from src.handlers.timezone import request_timezone_setup
from src.handlers.report import show_report


def callback_query_router(update: Update, context: CallbackContext):
    update.callback_query.answer()

    if 'language#' in update.callback_query.data:
        return request_language_setup(update, context)

    if 'timezone#' in update.callback_query.data:
        return request_timezone_setup(update, context)

    if 'report#' in update.callback_query.data:
        return show_report(update, context)

    if 'delete#' in update.callback_query.data:
        return delete(update, context)

    if 'edit#' in update.callback_query.data:
        return user_selected_edit_day(update, context)

    if 'option#' in update.callback_query.data:
        return handle_chosen_option(update, context)

    if 'help#' in update.callback_query.data:
        return handle_help(update, context)
