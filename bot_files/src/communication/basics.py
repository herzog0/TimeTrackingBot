from telegram import Update, ParseMode

from src.support.escapers import aggressive_escaper, escaped


def send_message(update: Update, message: str):
    return update.effective_message.reply_text(text=message)


def send_markdown_msg(update: Update, message: str):
    msg = escaped(message)
    return update.effective_message.reply_text(text=msg, parse_mode=ParseMode.MARKDOWN_V2)


def send_markup_msg(update: Update, message: str, markup, markdown: bool = False):
    if markdown:
        msg = escaped(message)
        return update.effective_message.reply_text(text=msg, reply_markup=markup, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        return update.effective_message.reply_text(text=message, reply_markup=markup)


def edit_message(update: Update, message: str, markdown: bool = False, markup=None):
    if markdown:
        msg = escaped(message)
        args = {
            "text": msg,
            "parse_mode": ParseMode.MARKDOWN_V2
        }
    else:
        args = {
            "text": message
        }

    if markup:
        args['reply_markup'] = markup

    return update.effective_message.edit_text(**args)


def send_document(update: Update, document, filename):
    return update.effective_chat.send_document(document=document, filename=filename)
