import datetime
from pprint import pprint
from typing import Union

import boto3
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv

from src.dynamo_db.enums import SetupState, Language, ChatState

load_dotenv()

boto3.setup_default_session()
table_name = os.environ['USER_INFO_TABLE']

dynamodb = boto3.resource('dynamodb')
_table = dynamodb.Table(table_name)


def delete_user_info(chat_id: Union[str, int]) -> bool:
    chat_id = str(chat_id)
    response = _table.delete_item(
        Key={
            'chat_id': chat_id
        },
        ReturnValues='ALL_OLD'
    )
    if 'Attributes' in response:
        return True
    return False


def create_or_reset_user(chat_id: Union[str, int]):
    chat_id = str(chat_id)
    _table.put_item(
        Item={
            'chat_id': chat_id,
            'last_update': datetime.utcnow().isoformat(),
            'setup_state': SetupState.LANGUAGE_NOT_SET.value
        }
    )
    set_setup_state(chat_id, SetupState.LANGUAGE_NOT_SET)


def get_user_info(chat_id: Union[str, int]):
    chat_id = str(chat_id)
    try:
        return _table.get_item(
                Key={
                    'chat_id': chat_id
                },
                ConsistentRead=True
            )['Item']
    except KeyError:
        return None


def get_user_states(chat_id: Union[str, int]) -> (Union[SetupState, None], Union[ChatState, None]):
    user_info = get_user_info(chat_id)
    if user_info is None:
        return None, None
    setup_state = SetupState(user_info['setup_state']) if 'setup_state' in user_info else None
    chat_state = ChatState(user_info['chat_state']) if 'chat_state' in user_info else None
    return setup_state, chat_state


def user_now(chat_id: Union[str, int], iso: bool = False):
    offset = get_user_info(chat_id)['utc_delta_seconds']
    _now = datetime.utcnow() + timedelta(seconds=int(offset))
    return _now.isoformat() if iso else _now


def do_user_offset(chat_id: Union[str, int], date: datetime, iso: bool = False):
    offset = get_user_info(chat_id)['utc_delta_seconds']
    _date = date + timedelta(seconds=int(offset))
    return _date.isoformat() if iso else _date


def cancel_edit(chat_id: Union[str, int]):
    chat_id = str(chat_id)
    _table.update_item(
        Key={
            'chat_id': chat_id,
        },
        UpdateExpression="REMOVE editing_day SET last_update = :d, chat_state = :cs",
        ExpressionAttributeValues={
            ':d': datetime.utcnow().isoformat(),
            ':cs': ChatState.NONE.value
        }
    )


def set_edit_day(chat_id: Union[str, int], edit_day: str):
    chat_id = str(chat_id)
    _table.update_item(
        Key={
            'chat_id': chat_id,
        },
        UpdateExpression="SET editing_day = :s, last_update = :d",
        ExpressionAttributeValues={
            ':d': datetime.utcnow().isoformat(),
            ':s': edit_day
        }
    )


def set_chat_state(chat_id: Union[str, int], state: ChatState):
    chat_id = str(chat_id)
    _table.update_item(
        Key={
            'chat_id': chat_id,
        },
        UpdateExpression="SET chat_state = :s, last_update = :d",
        ExpressionAttributeValues={
            ':d': datetime.utcnow().isoformat(),
            ':s': state.value
        }
    )


def set_setup_state(chat_id: Union[str, int], state: SetupState):
    chat_id = str(chat_id)
    _table.update_item(
        Key={
            'chat_id': chat_id,
        },
        UpdateExpression="SET setup_state = :s, last_update = :d",
        ExpressionAttributeValues={
            ':d': datetime.utcnow().isoformat(),
            ':s': state.value
        }
    )


def set_clocked_in(chat_id: Union[str, int]):
    chat_id = str(chat_id)
    _table.update_item(
        Key={
            'chat_id': chat_id,
        },
        UpdateExpression="SET last_update = :d, chat_state = :st, clocked_in_date = :d",
        ExpressionAttributeValues={
            ':d': datetime.utcnow().isoformat(),
            ':st': ChatState.CLOCKED_IN.value
        }
    )


def set_msg_reply_id(chat_id: Union[str, int], msg_reply_id: int):
    chat_id = str(chat_id)
    _table.update_item(
        Key={
            'chat_id': chat_id,
        },
        UpdateExpression="SET msg_reply_id = :s, last_update = :d",
        ExpressionAttributeValues={
            ':d': datetime.utcnow().isoformat(),
            ':s': msg_reply_id,
        }
    )


def set_unreported_clock_out(chat_id: Union[str, int], msg_reply_id: int, iso_date: str):
    chat_id = str(chat_id)
    _table.update_item(
        Key={
            'chat_id': chat_id,
        },
        UpdateExpression="REMOVE clocked_in_date SET msg_reply_id = :s, last_update = :d, chat_state = :st, "
                         "clock_out_date = :cd",
        ExpressionAttributeValues={
            ':d': datetime.utcnow().isoformat(),
            ':s': msg_reply_id,
            ':st': ChatState.CLOCK_OUT_UNREPORTED.value,
            ':cd': iso_date
        }
    )


def set_clock_out_msg_reply_id(chat_id: Union[str, int], msg_reply_id: int):
    chat_id = str(chat_id)
    _table.update_item(
        Key={
            'chat_id': chat_id,
        },
        UpdateExpression="SET msg_reply_id = :s, last_update = :d",
        ExpressionAttributeValues={
            ':d': datetime.utcnow().isoformat(),
            ':s': msg_reply_id,
        }
    )


def set_timezone(chat_id: Union[str, int], utc_delta_seconds: int, next_state: SetupState = None):
    chat_id = str(chat_id)
    _query = "SET utc_delta_seconds = :s, last_update = :d"
    _attr_values = {
        ':d': datetime.utcnow().isoformat(),
        ':s': utc_delta_seconds
    }

    if next_state:
        _query = _query + ", setup_state = :st"
        _attr_values[':st'] = next_state.value

    _table.update_item(
        Key={
            'chat_id': chat_id,
        },
        UpdateExpression=_query,
        ExpressionAttributeValues=_attr_values
    )


def set_language(chat_id: Union[str, int], lang: Language, next_state: SetupState = None):
    chat_id = str(chat_id)
    _query = "SET lang = :l, last_update = :d"
    _attr_values = {
        ':d': datetime.utcnow().isoformat(),
        ':l': lang.value
    }

    if next_state:
        _query = _query + ", setup_state = :s"
        _attr_values[':s'] = next_state.value

    _table.update_item(
        Key={
            'chat_id': chat_id,
        },
        UpdateExpression=_query,
        ExpressionAttributeValues=_attr_values
    )


def remove_msg_reply_id(chat_id: Union[str, int], next_state: ChatState = ChatState.NONE):
    chat_id = str(chat_id)
    _table.update_item(
        Key={
            'chat_id': chat_id
        },
        UpdateExpression='REMOVE msg_reply_id, clocked_in_date, clock_out_date SET chat_state = :s, last_update = :d',
        ExpressionAttributeValues={
            ':s': next_state.value,
            ':d': datetime.utcnow().isoformat()
        }
    )


if __name__ == '__main__':
    pass
    # remove_test()
    # print(get_user_info('123'))
    # create_or_reset_user('123')
    # set_language('123', Language.ENGLISH, State.TIMEZONE_NOT_SET)
    # set_timezone('123', -10800, State.NONE)
    # print(get_user_info('154885116'))
