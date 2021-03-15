from enum import Enum


class SetupState(Enum):
    LANGUAGE_NOT_SET = "LANGUAGE_NOT_SET"
    TIMEZONE_NOT_SET = "TIMEZONE_NOT_SET"
    NONE = "NONE"


class ChatState(Enum):
    CLOCK_OUT_UNREPORTED = "CLOCK_OUT_UNREPORTED"
    CLOCKED_IN = "CLOCKED_IN"
    AWAITING_EDIT_DAY = "AWAITING_EDIT_DAY"
    AWAITING_EDITED_REGISTRIES = "AWAITING_EDITED_REGISTRIES"
    NONE = "NONE"


class Language(Enum):
    ENGLISH = "en"
    PORTUGUESE = "pt"
