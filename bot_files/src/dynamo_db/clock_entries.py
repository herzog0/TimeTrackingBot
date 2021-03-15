import datetime
from pprint import pprint
from typing import Union
from dateutil import relativedelta
import boto3
import os

from datetime import datetime, timedelta, time
from boto3.dynamodb.conditions import Key

from dotenv import load_dotenv

from src.dynamo_db.user_info import user_now, set_clocked_in

load_dotenv()

boto3.setup_default_session()
table_name = os.environ['CLOCK_ENTRIES_TABLE']

dynamodb = boto3.resource('dynamodb')
_table = dynamodb.Table(table_name)


def _beginning(_date: datetime):
    return datetime.combine(_date, time())


def _end(_date: datetime):
    return datetime.combine(_date, time()) - timedelta(microseconds=1) + timedelta(days=1)


def delete_user_entries(chat_id: Union[str, int]) -> bool:
    chat_id = str(chat_id)
    # The year the bot was made, grab all since then
    beginning_2021 = datetime.combine(datetime.now().replace(year=2021, day=1, month=1), time())
    items = _table.query(
        KeyConditionExpression=Key('chat_id').eq(chat_id) & Key('date').gte(beginning_2021.isoformat()),
        ProjectionExpression='chat_id, #d',
        ExpressionAttributeNames={'#d': 'date'}
    )['Items']
    if len(items) == 0:
        return False
    with _table.batch_writer() as batch:
        for item in items:
            batch.delete_item(Key=item)
    return True


def delete_that_day_entries(chat_id: Union[str, int], date: datetime):
    chat_id = str(chat_id)
    that_day_beginning = _beginning(date)
    next_day_beginning = (that_day_beginning + timedelta(days=1)).isoformat()
    that_day_beginning = that_day_beginning.isoformat()
    items = _table.query(
        ConsistentRead=True,
        KeyConditionExpression=Key('chat_id').eq(chat_id) & Key('date').between(that_day_beginning, next_day_beginning),
        ProjectionExpression='chat_id, #d',
        ExpressionAttributeNames={'#d': 'date'}
    )['Items']
    with _table.batch_writer() as batch:
        for item in items:
            batch.delete_item(Key=item)


def ttl():
    # defaults to 63 days
    _ttl = int(os.environ.get('TTL', 5443200))
    beginning_of_month = _beginning(datetime.now().replace(day=1))
    return int(beginning_of_month.timestamp() + _ttl)


def insert_entry_description(chat_id: Union[str, int], date: str, description: str):
    chat_id = str(chat_id)
    _table.update_item(
        Key={
            'chat_id': chat_id,
            'date': date
        },
        UpdateExpression="SET description = :d",
        ExpressionAttributeValues={
            ':d': description
        }
    )


def create_full_entry(chat_id: Union[str, int], date: str, description: str = None):
    chat_id = str(chat_id)
    if description is None:
        _table.put_item(
            Item={
                'chat_id': chat_id,
                'date': date,
                'ttl': ttl()
            }
        )
    else:
        _table.put_item(
            Item={
                'chat_id': chat_id,
                'date': date,
                'description': description,
                'ttl': ttl()
            }
        )


def clock_in(chat_id: Union[str, int]):
    chat_id = str(chat_id)
    _date = user_now(chat_id, True)
    _table.put_item(
        Item={
            'chat_id': chat_id,
            'date': _date,
            'ttl': ttl()
        }
    )

    # in main, when we perform a clock in/out we check for which state
    # we'll end up in.
    # if it is a clock out, then it'll override whatever it is in the user_info field
    # so we can safely put "clocked_in" as the state for now
    set_clocked_in(chat_id)
    return _date


def max_entry(entries: list):
    return max(entries, key=lambda x: x['date'])


def replied_entry_description(chat_id: Union[str, int], description: str, clock_out_date: str):
    insert_entry_description(chat_id, clock_out_date, description)


def query_interval(chat_id: Union[str, int], start: str, end: str):
    chat_id = str(chat_id)
    items = _table.query(
        KeyConditionExpression=Key('chat_id').eq(chat_id) & Key('date').between(start, end)
    )
    return items['Items']


def that_day_entries(chat_id: Union[str, int], iso_date: str):
    chat_id = str(chat_id)
    start = _beginning(datetime.fromisoformat(iso_date))
    end = _end(start).isoformat()
    start = start.isoformat()
    items = _table.query(
        ConsistentRead=True,
        KeyConditionExpression=Key('chat_id').eq(chat_id) & Key('date').between(start, end)
    )
    return items['Items']


def today_entries(chat_id: Union[str, int]):
    return that_day_entries(chat_id, user_now(chat_id).isoformat())


def yesterday_entries(chat_id: Union[str, int]):
    yesterday = user_now(chat_id) - timedelta(days=1)
    return that_day_entries(chat_id, yesterday.isoformat())


def week_entries(chat_id: Union[str, int]):
    now = user_now(chat_id)
    end = _end(now + timedelta(days=(5-now.weekday())))
    start = _beginning(end - timedelta(days=6)).isoformat()
    end = end.isoformat()
    return query_interval(chat_id, start, end)


def last_week_entries(chat_id: Union[str, int]):
    now = user_now(chat_id)
    end = _end(now - timedelta(days=(now.weekday() + 2)))
    start = _beginning(end - timedelta(days=6)).isoformat()
    end = end.isoformat()
    return query_interval(chat_id, start, end)


def month_entries(chat_id: Union[str, int]):
    end = _beginning(user_now(chat_id) + relativedelta.relativedelta(months=1, day=1)) - timedelta(microseconds=1)
    start = _beginning(end.replace(day=1)).isoformat()
    end = end.isoformat()
    return query_interval(chat_id, start, end)


def last_month_entries(chat_id: Union[str, int]):
    end = _beginning(user_now(chat_id).replace(day=1)) - timedelta(microseconds=1)
    start = _beginning(end.replace(day=1)).isoformat()
    end = end.isoformat()
    return query_interval(chat_id, start, end)


if __name__ == '__main__':
    _chat_id = '154885116'
    # clock_in(_chat_id)
    # _t = today_entries(_chat_id)
    # pprint(_t)
    # print(yesterday_entries(_chat_id))
    # insert_entry_description(_chat_id, '2021-02-28T22:31:55.499867', 'testtt')
    # print(week_entries(_chat_id))
    # insert_entry_description('123456789', '2021-03-01T01:36:08.774452', 'teste vrau')
    # last_week_entries('123456789')
    # month_entries('123456789')
    # yesterday_entries('123456789')
    # pprint(delete_user_entries(_chat_id))
    pprint(that_day_entries(_chat_id, '2021-02-28T22:31:55.499867'))
