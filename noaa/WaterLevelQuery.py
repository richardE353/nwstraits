from dataclasses import dataclass
from datetime import datetime, timedelta

import noaa.NoaaApiFetcher as naf

@dataclass()
class WaterLevel:
    source_name: str
    value: float

    def is_estimated(self) -> bool:
        return self.source_name != 'one_minute_water_level'

def extract_first_v_or_nan(json: dict) -> float:
    if 'data' in json:
        elements = list(json['data'])
        if len(elements) > 0:
            return float(elements[0]['v'])
    return float('Nan')

def derive_mllw_water_height(station_id: int, dt: datetime) -> WaterLevel:
    import math
    reply = naf.fetch_water_data_reply(station_id, dt, dt)

    level_v = extract_first_v_or_nan(reply)
    if math.isnan(level_v) == False:
        return WaterLevel('one_minute_water_level', level_v)

    # no 1 minute data - try the 6 minute query
    six_min = timedelta(0, 0, 0, 0, 6, 0, 0)
    reply = naf.fetch_water_data_reply(station_id, dt - six_min, dt + six_min, 'water_level')
    level_v = extract_first_v_or_nan(reply)

    return WaterLevel('water_level', level_v)



