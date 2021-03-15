from telegram import Update, ForceReply, ParseMode
from telegram.error import BadRequest
from telegram.ext import CallbackContext, DispatcherHandlerStop

from src.communication.basics import send_markup_msg
from src.dynamo_db import get_user_info, remove_msg_reply_id, replied_entry_description, \
    set_clock_out_msg_reply_id
from src.support.logger import logger
from src.support.m17n import strings
from src.support.options_kbd import options_kbd


def request_clock_out_description(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        user_info = get_user_info(chat_id)
        msg_id = int(user_info['msg_reply_id'])
        clock_out_date = user_info['clock_out_date']
    except KeyError:
        return

    if not update.effective_message.reply_to_message or update.effective_message.reply_to_message.message_id != msg_id:
        try:
            update.effective_message.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except BadRequest:
            logger.warn('The message to be replied has been deleted by the user, but we\'ll try again')
        msg = send_markup_msg(update, strings()['feedback:exit:insist_reply'], ForceReply(), True)
        set_clock_out_msg_reply_id(chat_id, msg.message_id)
        raise DispatcherHandlerStop
    else:
        replied_entry_description(chat_id, update.effective_message.text, clock_out_date)
        send_markup_msg(update, strings()['feedback:exit:acknowledgment'], options_kbd(strings()))
        remove_msg_reply_id(chat_id)
        raise DispatcherHandlerStop
