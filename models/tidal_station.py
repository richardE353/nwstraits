from dataclasses import dataclass

import noaa.api_fetcher as naf
import models.tidal_correction as tc

from models.tidal_correction import TidalCorrection


@dataclass()
class TidalStation:
    name: str
    id: int
    _tidal_correction: TidalCorrection = TidalCorrection(0, 0, 0, 0.0, 0.0)

    @property
    def tidal_correction(self) -> TidalCorrection:
        if self._tidal_correction.is_unknown():
            self._tidal_correction = tc.fetch_tidal_correction(self.id)

        return self._tidal_correction


known_stations = {9447905: TidalStation("Admiralty Head", 9447905),
                  9448683: TidalStation("Burrows Bay", 9448683),
                  9449424: TidalStation("Cherry Point", 9449424),
                  9447995: TidalStation("Cornet Bay", 9447995),
                  9447952: TidalStation("Crescent Harbor", 9447952),
                  9447427: TidalStation("Edmonds", 9447427),
                  9449880: TidalStation("Friday Harbor", 9449880),
                  9447814: TidalStation("Glendale", 9447814),
                  9449184: TidalStation("Gooseberry Point", 9449184),
                  9443090: TidalStation("Neah Bay", 9443090),
                  9447934: TidalStation("Point Partridge", 9447934),
                  9444090: TidalStation("Port Angeles", 9444090),
                  9444900: TidalStation("Port Townsend", 9444900),
                  9447856: TidalStation("Sandy Point", 9447856),
                  9447130: TidalStation("Seattle", 9447130),
                  9448772: TidalStation("Ship Harbor", 9448772),
                  9448601: TidalStation("Yokeko Point", 9448601)
                  }


def lookup_station(station_id: int) -> TidalStation:
    if station_id in known_stations: return known_stations[station_id]

    reply = naf.fetch_station_info(station_id)

    if 'stations' in reply:
        noaa_station_info = dict(reply['stations'][0])
        new_id = int(noaa_station_info['id'])
        new_station = TidalStation(noaa_station_info['name'], new_id)
        known_stations[new_id] = new_station

        return new_station

    raise Exception('Failed to find NOAA station: {}'.format(station_id))
