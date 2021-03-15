from enum import Enum

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from src.support.m17n import strings


def options_kbd(_strings: dict) -> ReplyKeyboardMarkup:
    class ReplyKeyboardOptions(Enum):
        CLOCKIN = _strings['button:clock_inout']
        REPORT = _strings['button:report']
        OPTIONS = _strings['button:options']

    reply_keyboard = [
        [
            ReplyKeyboardOptions.CLOCKIN.value
        ],
        [
            ReplyKeyboardOptions.REPORT.value,
            ReplyKeyboardOptions.OPTIONS.value
        ]
    ]
    return ReplyKeyboardMarkup(reply_keyboard,
                               resize_keyboard=True,
                               one_time_keyboard=False)


def options_inline_kdb():
    _inline_keyboard_buttons = [
        [InlineKeyboardButton(strings()['button:edit'], callback_data='option#edit')],
        [InlineKeyboardButton(strings()['button:help'], callback_data='option#help')],
        [InlineKeyboardButton(strings()['button:source'], callback_data='option#source')],
        [InlineKeyboardButton(strings()['button:delete_all'], callback_data='option#delete')],
    ]
    return InlineKeyboardMarkup(_inline_keyboard_buttons)
