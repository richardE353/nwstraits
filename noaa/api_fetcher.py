from datetime import datetime

import requests
from requests import Response


# Useful links regarding NOAA api
#   https://tidesandcurrents.noaa.gov/PageHelp.html
#   https://tidesandcurrents.noaa.gov/products.html
#   https://api.tidesandcurrents.noaa.gov/api/prod/#station

# Sample data variable formats:
#   stationId = "9449424"
#   beginDate = "20210810 11:00"
#   endDate = "20210810 13:45"
# For details, see: https://api.tidesandcurrents.noaa.gov/api/prod#DataAPIResponse

def process_reply(r: Response) -> dict:
    if (r.status_code != 200):
        print("Query failed due to: {}", r.reason)
        print(r.content)

    return dict(r.json())

def fetch_water_data_reply(station_id: int, begin_date: datetime, end_date: datetime,
                           product: str = 'one_minute_water_level') -> dict:
    start_str = begin_date.strftime('%Y%m%d %H:%M')
    end_str = end_date.strftime('%Y%m%d %H:%M')

    payload = {'application': 'nwstraits.org', 'begin_date': start_str, 'end_date': end_str,
               'station': station_id, 'product': product, 'units': 'metric', 'time_zone': 'lst_ldt',
               'datum': 'MLLW', 'format': 'json'}

    reply = requests.get('https://api.tidesandcurrents.noaa.gov/api/prod/datagetter', params=payload)
    return process_reply(reply)


def fetch_tide_offsets_reply(stn_id: int) -> dict:
    base_str = 'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{}/tidepredoffsets.json?units=metric'
    qry_str = base_str.format(stn_id)
    reply = requests.get(qry_str)

    return process_reply(reply)


def fetch_station_info(station_id: int) -> dict:
    qry_str = 'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{}.json'.format(station_id)
    reply = requests.get(qry_str)
    return process_reply(reply)
