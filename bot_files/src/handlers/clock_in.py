from telegram import Update, ForceReply, ParseMode
from telegram.ext import CallbackContext, DispatcherHandlerStop

from src.communication.basics import send_message, send_markup_msg
from src.dynamo_db import clock_in, today_entries, set_unreported_clock_out
from src.support.m17n import strings


def clockin(update: Update, context: CallbackContext) -> None:
    chat_id = str(update.message.chat_id)
    _date = clock_in(chat_id)
    entries = today_entries(chat_id)
    if len(entries) % 2 == 0:
        msg = send_markup_msg(update, strings()['feedback:exit'], ForceReply(), True)
        set_unreported_clock_out(chat_id, msg.message_id, _date)
        raise DispatcherHandlerStop
    else:
        send_message(update, strings()['feedback:entrance'])
        raise DispatcherHandlerStop
