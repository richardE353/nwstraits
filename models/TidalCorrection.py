from dataclasses import dataclass

import noaa.NoaaApiFetcher as naf


@dataclass(frozen=True)
class TidalCorrection:
    station_id: int
    reference_station_id: int
    time_offset: int
    height_scaling: float
    height_offset: float

    def is_unknown(self) -> bool:
        return self.station_id == 0


# I cannot find this information on the NOAA site, but co-ops.userservices@noaa.gov sent me this clarification:
#
#  Type has only 2 options
#    1) S - Subordinate tide station
#    2) R - Reference tide station
#
#  For Subordinate tide prediction stations there are only 2 options for the "Height Adjustment Type":
#    1) R - Ratio - height adjustments are a multiplication factor applied to the tide prediction heights for the associated harmonic station.
#    2) F - Fixed - height adjustments are an additive value applied to the tide prediction heights for the associated harmonic station.
#
# sample subordinate response:
# {
#   'refStationId': '9444900',
#   'type': 'S',
#   'heightOffsetHighTide': 0.93,
#   'heightOffsetLowTide': 1.02,
#   'timeOffsetHighTide': 18,
#   'timeOffsetLowTide': 29,
#   'heightAdjustedType': 'R',
#   'self': None
# }
#
# sample reference response:
# {
#   "refStationId": "9447130",
#   "type": "R",
#   "heightOffsetHighTide": 0.0,
#   "heightOffsetLowTide": 0.0,
#   "timeOffsetHighTide": 0,
#   "timeOffsetLowTide": 0,
#   "heightAdjustedType": "F",
#   "self": null
# }
def fetch_tidal_correction(a_station_id: int) -> TidalCorrection:
    reply = naf.fetch_tide_offsets_reply(a_station_id)
    t_offset = reply['timeOffsetLowTide']
    ref_station = reply['refStationId'].strip()
    if len(ref_station) == 0: ref_station = str(a_station_id)

    # Reference stations do not have a Tidal Correction
    if reply['type'] == 'R':
        return TidalCorrection(a_station_id, a_station_id, 0, 1.0, 0.0)

    if reply['heightAdjustedType'] == 'R':
        return TidalCorrection(a_station_id, ref_station, t_offset, reply['heightOffsetLowTide'], 0.0)

    if reply['heightAdjustedType'] == 'F':
        return TidalCorrection(a_station_id, ref_station, t_offset, 1.0, reply['heightOffsetLowTide'])

    print("fetch_tidal_correction given unknown station id: {}".format(a_station_id))
    return TidalCorrection(0, 0, 0, 1.0, 0.0)  # unknown correction
