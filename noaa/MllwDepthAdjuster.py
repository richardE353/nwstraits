from dataclasses import dataclass
from datetime import date, time, datetime

from models.TidalStation import TidalStation

import noaa.WaterLevelQuery as wlq
from noaa.WaterLevelQuery import WaterLevel


@dataclass()
class MllDepthAdjuster:
    tidal_station: TidalStation
    data_date: date
    start_time: time
    _water_level: WaterLevel = None

    def initialize_water_level(self):
        ref_stn = self.tidal_station.tidal_correction.reference_station_id
        start_dt = datetime.combine(self.data_date, self.start_time)
        self._water_level = wlq.derive_mllw_water_height(ref_stn, start_dt)

    def adjust_depth(self, meas_depth: float) -> float:
        if meas_depth == float("NaN"): return float("NaN")

        if (self._water_level is None): self.initialize_water_level()

        tc = self.tidal_station.tidal_correction
        adjusted_noaa_depth = self._water_level.value * tc.height_scaling + tc.height_offset

        return meas_depth - adjusted_noaa_depth


def create_depth_adjuster(ts: TidalStation, dt: date, st: time) -> MllDepthAdjuster:
    return MllDepthAdjuster(ts, dt, st)
