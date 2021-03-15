from pprint import pprint

from googlemaps.timezone import timezone
from googlemaps.client import geocode
from datetime import datetime, timedelta
from dotenv import load_dotenv

import googlemaps
import os

load_dotenv()


def get_address_and_timezone_by_name(loc_name):
    client = googlemaps.Client(key=os.environ.get('GOOGLEMAPS_TOKEN', None))
    loc = geocode(client, loc_name)
    if not loc:
        raise LocationNotFoundException()
    address = loc[0]['formatted_address']
    coords = loc[0]['geometry']['location']
    tz = timezone(client, coords, datetime.utcnow())
    offset = tz['rawOffset']  # in seconds
    timezone_id = tz['timeZoneId']

    return {
        'offset': offset,
        'timezone_id': timezone_id,
        'address': address,
        'coords': coords
    }


class LocationNotFoundException(Exception):
    def __init__(self):
        super()


if __name__ == '__main__':
    print(get_address_and_timezone_by_name('rua dois'))
