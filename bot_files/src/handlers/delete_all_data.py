from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, DispatcherHandlerStop

from src import dynamo_db as db
from src.communication.basics import send_markup_msg, edit_message
from src.support.m17n import strings


def delete(update: Update, context: CallbackContext):
    _del_inline_keyboard_buttons = [
        [InlineKeyboardButton(strings()['button:yes'], callback_data='delete#yes')],
        [InlineKeyboardButton(strings()['button:no'], callback_data='delete#no')],
    ]

    _callback_query_options = [
        'delete#yes',
        'delete#no'
    ]

    chat_id = update.effective_chat.id
    if update.callback_query is None or update.callback_query.data not in _callback_query_options:
        reply_markup = InlineKeyboardMarkup(_del_inline_keyboard_buttons)
        send_markup_msg(update, strings()["delete:confirm"], reply_markup, True)
        raise DispatcherHandlerStop
    else:
        if update.callback_query.data == 'delete#yes':
            if not db.delete_user_entries(chat_id) and not db.delete_user_info(chat_id):
                update.effective_message.delete()
                send_markup_msg(update, strings()['delete:nothing'], ReplyKeyboardMarkup([['/start']],
                                                                                         resize_keyboard=True,
                                                                                         one_time_keyboard=True))
            else:
                update.effective_message.delete()
                send_markup_msg(update, strings()['delete:success'], ReplyKeyboardMarkup([['/start']],
                                                                                         resize_keyboard=True,
                                                                                         one_time_keyboard=True))
            raise DispatcherHandlerStop
        else:
            edit_message(update, strings()['delete:cancelled'])
            raise DispatcherHandlerStop
