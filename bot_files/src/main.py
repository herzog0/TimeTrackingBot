import os
from queue import Queue
from telegram import Update, Bot
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters, Dispatcher
import re

from src.handlers.cancel import cancel_operation
from src.handlers.cb_router import callback_query_router
from src.handlers.check_state import check_impeditive_state
from src.handlers.clock_in import clockin
from src.handlers.default import default
from src.handlers.delete_all_data import delete
from src.handlers.edit import edit_choice_selector
from src.handlers.help import handle_help
from src.handlers.options import options
from src.handlers.report import choose_report
from src.handlers.start import start


def main(data) -> None:
    bot = Bot(token=os.environ.get('TELEGRAM_TOKEN'))
    dispatcher = Dispatcher(bot=bot, update_queue=Queue())
    update = Update.de_json(data, bot)
    # PRIORITY 0
    dispatcher.add_handler(CommandHandler('delete', delete), 0)
    dispatcher.add_handler(CommandHandler('apagar', delete), 0)
    # Yes! /start is priority 0
    # If the user is in an inconsistent state we cannot let them
    # restart their info. That would lead to potential problems
    # if they change their timezone info. Record times in different
    # timezones may be operated on and the user will get the wrong
    # number of hours of work.
    # But, if they're not in a sensitive state, we could ignore the rest and 
    # override whatever info they where relying on earlier.
    dispatcher.add_handler(CommandHandler('start', start), 0)

    # PRIORITY 1
    dispatcher.add_handler(CommandHandler('cancel', cancel_operation), 1)
    dispatcher.add_handler(CommandHandler('cancelar', cancel_operation), 1)
    dispatcher.add_handler(MessageHandler(Filters.text, check_impeditive_state), 1)

    # PRIORITY 2
    # These are the ones with the preceding backslash '\<command>'
    dispatcher.add_handler(CommandHandler('report', choose_report), 2)
    dispatcher.add_handler(CommandHandler('relatorio', choose_report), 2)
    dispatcher.add_handler(CommandHandler('clockin', clockin), 2)
    dispatcher.add_handler(CommandHandler('ponto', clockin), 2)
    dispatcher.add_handler(CommandHandler('edit', edit_choice_selector), 2)
    dispatcher.add_handler(CommandHandler('editar', edit_choice_selector), 2)
    dispatcher.add_handler(CommandHandler('options', options), 2)
    dispatcher.add_handler(CommandHandler('opcoes', options), 2)
    dispatcher.add_handler(CommandHandler('cancel', cancel_operation), 2)
    dispatcher.add_handler(CommandHandler('cancelar', cancel_operation), 2)
    dispatcher.add_handler(CommandHandler('help', handle_help), 2)
    dispatcher.add_handler(CommandHandler('ajuda', handle_help), 2)

    # These are answers from the markup keyboard
    dispatcher.add_handler(
        MessageHandler(Filters.regex(re.compile(r'^(ponto|clock)', re.IGNORECASE)), clockin),
        2
    )
    dispatcher.add_handler(
        MessageHandler(Filters.regex(re.compile(r'^(report|relatorio|relatório)', re.IGNORECASE)), choose_report),
        2
    )
    dispatcher.add_handler(
        MessageHandler(Filters.regex(re.compile(r'^(edit|editar)', re.IGNORECASE)), edit_choice_selector),
        2
    )
    dispatcher.add_handler(
        MessageHandler(Filters.regex(re.compile(r'^(options|opção|option|opções)', re.IGNORECASE)), options),
        2
    )
    dispatcher.add_handler(
        MessageHandler(Filters.regex(re.compile(r'^(cancel|cancelar)', re.IGNORECASE)), cancel_operation),
        2
    )
    dispatcher.add_handler(
        CallbackQueryHandler(callback_query_router),
        2
    )

    # Handle anything that hasn't been matched above!
    dispatcher.add_handler(
        MessageHandler(Filters.regex('.*'), default),
        3
    )

    dispatcher.process_update(update)


# if __name__ == '__main__':
#     main()
