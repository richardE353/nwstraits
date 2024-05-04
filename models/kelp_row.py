import os
from dataclasses import dataclass
import operator
from datetime import date, time

from pandas import DataFrame, Series

import models.site_images as SurveySiteImages
import models.attachments as DataSetAttachments
import models.cluster_point as KelpClusterPoint
import models.volunteer_info as VolunteerInfo
import models.tidal_station as TidalStation

import utils.pandas_helper as ph

import noaa.mllw_adjuster as MllwDepthAdjuster
from models.tidal_station import lookup_station


@dataclass()
class KelpSurvey:
    """Class with key columns from the KoboToolbox export of Kelp surveys"""
    survey_date: str
    location: str
    survey_num: int
    county: str
    weather: str
    tidal_ht: float
    tide_station_label: str
    tide_station: TidalStation
    time_start: str
    time_end: str
    survey_observations: str
    survey_notes: str
    depth_1_at_shore_edge: float
    temp_1_at_shore_edge: float
    depth_1_at_outer_edge: float
    temp_1_at_outer_edge: float
    depth_2_at_shore_edge: float
    temp_2_at_shore_edge: float
    depth_2_at_outer_edge: float
    temp_2_at_outer_edge: float
    kelp_obs_1: str
    kelp_obs_2: str
    kelp_obs_3: str
    kelp_obs_4: str
    uuid: str
    submission_date_time: str
    gps_track_name: str
    site_image_names: SurveySiteImages
    data_file_names: DataSetAttachments
    volunteer_info: VolunteerInfo
    kelp_clusters: list
    current_knots: float = float('NaN')
    current_station: str = ''
    survey_conditions: str = ''
    extent_start_waypoint: str = ''
    extent_end_waypoint: str = ''
    _depth_adjuster: MllwDepthAdjuster = None

    @property
    def depth_adjuster(self) -> MllwDepthAdjuster:
        if self._depth_adjuster is None:
            dt = date.fromisoformat(self.survey_date)
            st = time.fromisoformat(self.time_start)
            t_stn = self.tide_station
            self._depth_adjuster = MllwDepthAdjuster.create_depth_adjuster(t_stn, dt, st)

        return self._depth_adjuster

    def file_prefix(self) -> str:
        base_str = self.county + "_" + self.location + "_" + str(self.survey_date) + "_" + str(self.survey_num)
        return base_str.replace("-", "_")

    def noaa_data_missing(self) -> bool:
        return self.tide_station.tidal_correction.is_unknown()

    def copy_files(self, src: str, dest: str) -> bool:
        pics_dir = os.path.join(dest, self.county, "site_photos")
        self.site_image_names.copy_files(self.file_prefix(), src, pics_dir)

        data_pics_dir = os.path.join(dest, self.county, "data_files")
        self.data_file_names.copy_files(self.file_prefix(), src, data_pics_dir)

        volunteer_dir = os.path.join(dest, self.county, "volunteer_photos")
        self.volunteer_info.copy_files(self.file_prefix(), src, volunteer_dir)


def celsius_temp(t: float, t_units: str) -> float:
    if t_units == "fahrenheit": return (t - 32.0) / 1.8
    return t


def metric_depth(ft: float) -> float:
    if ft == float("NaN"): return ft
    return ft * 0.3048


def extract_rows(df: DataFrame) -> list:
    # https://www.learndatasci.com/solutions/how-iterate-over-rows-pandas/
    surveys = list(df.apply(row_to_kelp_survey, axis=1))
    return sorted(surveys, key=operator.attrgetter("location", "survey_date"))


def row_to_kelp_survey(sr: Series) -> KelpSurvey:
    temp_units = ph.as_string_or_default(sr["Temperature_Units"], "fahrenheit")
    survey_date_str = str(sr.survey_date.date())
    survey_data: KelpSurvey = KelpSurvey(
        survey_date_str,
        sr.kelp_bed_name,
        sr["_index"],
        sr.data_county,
        sr.weather,
        metric_depth(ph.as_float_or_default(sr.start_tidal_height_ft)),
        sr.tide_stn_label,
        lookup_station(int(sr.tide_stn_name)),
        ph.as_string_or_default(sr.survey_start_time),
        ph.as_string_or_default(sr.end_time),
        sr.observations,
        ph.as_string_or_default(sr.other_notes),
        metric_depth(ph.as_float_or_default(sr.closest_edge_depth1)),
        celsius_temp(sr.closest_edge_temp1, temp_units),
        metric_depth(ph.as_float_or_default(sr.farthest_edge_depth1)),
        celsius_temp(sr.farthest_edge_temp1, temp_units),
        metric_depth(ph.as_float_or_default(sr.closest_edge_depth2)),
        celsius_temp(sr.closest_edge_temp2, temp_units),
        metric_depth(ph.as_float_or_default(sr.farthest_edge_depth2)),
        celsius_temp(sr.farthest_edge_temp2, temp_units),
        ph.as_string_or_default(sr.kc_observation1),
        ph.as_string_or_default(sr.kc_observation2),
        ph.as_string_or_default(sr.kc_observation3),
        ph.as_string_or_default(sr.kc_observation4),
        sr["_uuid"],
        str(sr["_submission_time"]),
        ph.as_string_or_default(sr.GPS_perimeter_track_name),
        SurveySiteImages.extract_site_image_attachments(sr),
        DataSetAttachments.extract_data_attachments(sr),
        VolunteerInfo.extract_volunteer_info(sr),
        KelpClusterPoint.extract_kelp_clusters(sr),
        ph.as_float_or_default(sr.current_in_knots),
        ph.as_string_or_default(sr.tide_station_source),
        ph.get_column_or_default(sr, "survey_conditions"),
        ph.get_column_or_default(sr, "extent_start_waypoint"),
        ph.get_column_or_default(sr, "extent_end_waypoint")
    )

    return survey_data
