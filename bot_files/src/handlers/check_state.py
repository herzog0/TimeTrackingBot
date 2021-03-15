from telegram import Update
from telegram.ext import CallbackContext

from src.dynamo_db import get_user_states, SetupState, ChatState
from src.handlers.clock_out import request_clock_out_description
from src.handlers.clocked_in_validator import ensure_valid_clocked_in
from src.handlers.edit import validate_edited_registries, validate_picked_day
from src.handlers.language import request_language_setup
from src.handlers.request_start import request_start
from src.handlers.timezone import request_timezone_setup
from src.support.m17n import set_strings


def check_impeditive_state(update: Update, context: CallbackContext):
    setup_state, chat_state = get_user_states(str(update.effective_message.chat_id))

    if setup_state is None and chat_state is None:
        # the user might have used the /delete command and now
        # is trying to do other things but nothing is configured anymore.
        request_start(update, context)

    if setup_state is not None and setup_state is not SetupState.LANGUAGE_NOT_SET:
        set_strings(chat_id=str(update.effective_message.chat_id))

    if setup_state is not None and setup_state is not SetupState.NONE:
        {
            SetupState.LANGUAGE_NOT_SET: request_language_setup,
            SetupState.TIMEZONE_NOT_SET: request_timezone_setup,
        }[setup_state](update, context)

    if chat_state is not None and chat_state is not ChatState.NONE:
        {
            ChatState.CLOCK_OUT_UNREPORTED: request_clock_out_description,
            ChatState.CLOCKED_IN: ensure_valid_clocked_in,
            ChatState.AWAITING_EDITED_REGISTRIES: validate_edited_registries,
            ChatState.AWAITING_EDIT_DAY: validate_picked_day
        }[chat_state](update, context)
