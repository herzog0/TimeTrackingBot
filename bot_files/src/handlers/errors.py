from pprint import pprint

from telegram.ext import CallbackContext

from src.support.logger import logger


def error_handler(update: object, context: CallbackContext):
    logger.error(context.error)
    pprint(update)
    raise context.error
