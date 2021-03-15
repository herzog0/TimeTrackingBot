from telegram import Update
from telegram.ext import CallbackContext

from src.dynamo_db import get_user_states, ChatState
from src.handlers.edit import cancel_edit


def cancel_operation(update: Update, context: CallbackContext):
    setup_state, chat_state = get_user_states(str(update.effective_message.chat_id))

    if chat_state is not None and chat_state is not ChatState.NONE:
        {
            ChatState.AWAITING_EDITED_REGISTRIES: cancel_edit,
            ChatState.AWAITING_EDIT_DAY: cancel_edit
        }[chat_state](update, context)
