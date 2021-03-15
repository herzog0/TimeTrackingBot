from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.support.m17n import strings


def help_inline_kdb():
    _inline_keyboard_buttons = [
        [InlineKeyboardButton(strings()['button:help:clockin'], callback_data='help#clockin')],
        [InlineKeyboardButton(strings()['button:help:report'], callback_data='help#report')],
        [InlineKeyboardButton(strings()['button:help:edit'], callback_data='help#edit')],
        [InlineKeyboardButton(strings()['button:help:deleteall'], callback_data='help#deleteall')],
        [InlineKeyboardButton(strings()['button:help:issue'], callback_data='help#issue')],
    ]
    return InlineKeyboardMarkup(_inline_keyboard_buttons)
