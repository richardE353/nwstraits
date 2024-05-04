from dataclasses import dataclass

import utils.files_helper as fh

import operator
from pandas import DataFrame, Series

import utils.pandas_helper as ph


@dataclass()
class AnchoringSurvey:
    """Class with key columns from the KoboToolbox export of No Anchor Zone surveys"""
    observer_names: str
    survey_date: str
    start_time: str
    weather: str
    weather_details: str
    county: str
    location: str
    location_label: str
    tidal_height_in_feet: float
    camera: str
    camera_details: str
    notes: str
    has_buoy: bool
    no_buoy_count: int
    inside_buoy_count: int
    outside_buoy_count: int
    photo_1_name: str
    photo_2_name: str
    photo_3_name: str
    photo_4_name: str
    photo_5_name: str
    photo_6_name: str
    uuid: str
    submission_date_time: str
    survey_num: int

    def file_prefix(self) -> str:
        base_str = self.county + "_" + self.location + "_" + str(self.survey_date) + "_" + str(self.survey_num)
        return base_str.replace("-", "_")

    def survey_info(self) -> str:
        if 0 == self.inside_buoy_count + self.outside_buoy_count + self.no_buoy_count:
            cnt_info = " no vessels"
        elif self.has_buoy == 'st_has_buoy':
            cnt_info = " vessels inside buoy: " + str(self.inside_buoy_count) + " outside buoy: " + str(
                self.outside_buoy_count)
        else:
            cnt_info = " no buoy vessel count: " + str(self.no_buoy_count)

        if self.notes:
            notes_for_log = "\n\t\t\t" + self.notes
        else:
            notes_for_log = ''

        return self.location_label + " " + self.survey_date + " " + self.weather + cnt_info + notes_for_log

    def copy_files(self, src: str, dest: str):
        prefix = self.file_prefix()

        if len(self.photo_1_name) > 0:
            fh.copy_file_if_exists(prefix, src, dest, self.photo_1_name, '_photo1')

        if len(self.photo_2_name) > 0:
            fh.copy_file_if_exists(prefix, src, dest, self.photo_2_name, '_photo2')

        if len(self.photo_3_name) > 0:
            fh.copy_file_if_exists(prefix, src, dest, self.photo_3_name, '_photo3')

        if len(self.photo_4_name) > 0:
            fh.copy_file_if_exists(prefix, src, dest, self.photo_4_name, '_photo4')

        if len(self.photo_5_name) > 0:
            fh.copy_file_if_exists(prefix, src, dest, self.photo_5_name, '_photo5')

        if len(self.photo_6_name) > 0:
            fh.copy_file_if_exists(prefix, src, dest, self.photo_6_name, '_photo6')


def row_to_survey(sr: Series) -> AnchoringSurvey:
    # date column format changed in 2023.
    if (len(str(sr.survey_date)) > 10):
        survey_date_str = str(sr.survey_date.date())
    else:
        survey_date_str = sr.survey_date

    survey_data: AnchoringSurvey = AnchoringSurvey(
        sr.observer_names,
        survey_date_str,
        sr.survey_start_time,
        sr.weather,
        sr.other_weather_details,
        sr.data_county,
        sr.eelgrass_bed_name,
        sr.eelgrass_bed_label_val,
        sr.start_tidal_height_ft,
        sr.camera,
        sr.other_camera_details,
        ph.as_string_or_default(sr.other_notes, ''),
        sr.has_buoy,
        int(ph.as_float_or_default(sr.without_buoy_count, 0.0)),
        int(ph.as_float_or_default(sr.inside_buoys_count, 0.0)),
        int(ph.as_float_or_default(sr.outside_buoys_count, 0.0)),
        ph.as_string_or_default(sr.site_photo_1),
        ph.as_string_or_default(sr.site_photo_2),
        ph.as_string_or_default(sr.site_photo_3),
        ph.as_string_or_default(sr.site_photo_4),
        ph.as_string_or_default(ph.get_column_or_default(sr, 'site_photo_5')),
        ph.as_string_or_default(ph.get_column_or_default(sr, 'site_photo_6')),
        sr["_uuid"],
        sr["_submission_time"],
        sr["_index"]
    )

    return survey_data


def extract_rows(df: DataFrame) -> list:
    # https://www.learndatasci.com/solutions/how-iterate-over-rows-pandas/
    surveys = list(df.apply(row_to_survey, axis=1))
    return sorted(surveys, key=operator.attrgetter("location", "survey_date"))
