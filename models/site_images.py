from dataclasses import dataclass

from pandas import Series

import utils.files_helper as fh
import utils.pandas_helper as ph

@dataclass(frozen=True)
class SurveySiteImages:
    beach_to_the_left: str      # 2022 only
    beach_to_the_right: str     # 2022 only
    to_beach: str
    to_water: str               # 2022 only
    kelp_photo_1: str           # 2023 and later
    kelp_photo_2: str           # 2023 and later
    kelp_photo_3: str           # 2023 and later
    kelp_photo_4: str           # 2023 and later

    def copy_files(self, file_prefix: str, src: str, dest: str):
        if len(self.beach_to_the_left) > 0:
            fh.copy_file_if_exists(file_prefix, src, dest, self.beach_to_the_left, '_BeL')
        if len(self.beach_to_the_right) > 0:
            fh.copy_file_if_exists(file_prefix, src, dest, self.beach_to_the_right, '_BeR')
        if len(self.to_beach) > 0:
            fh.copy_file_if_exists(file_prefix, src, dest, self.to_beach, '_ToBe')
        if len(self.to_water) > 0:
            fh.copy_file_if_exists(file_prefix, src, dest, self.to_water, '_ToWa')
        if len(self.kelp_photo_1) > 0:
            fh.copy_file_if_exists(file_prefix, src, dest, self.kelp_photo_1, '_Kelp1')
        if len(self.kelp_photo_2) > 0:
            fh.copy_file_if_exists(file_prefix, src, dest, self.kelp_photo_2, '_Kelp2')
        if len(self.kelp_photo_3) > 0:
            fh.copy_file_if_exists(file_prefix, src, dest, self.kelp_photo_3, '_Kelp3')
        if len(self.kelp_photo_4) > 0:
            fh.copy_file_if_exists(file_prefix, src, dest, self.kelp_photo_4, '_Kelp4')


def extract_site_image_attachments(survey_row: Series) -> SurveySiteImages:
    # using dictionary access to handle different Series columns between 2022 and 2023
    keys = survey_row.keys()
    def get_value_for_key(a_key: str) -> str:
        if a_key in keys:
            return ph.as_string_or_default(survey_row[a_key])
        return ''

    return SurveySiteImages(
        get_value_for_key('beach_to_the_left_photo'),
        get_value_for_key('beach_to_the_right_photo'),
        get_value_for_key('to_beach_photo'),
        get_value_for_key('to_water_photo'),
        get_value_for_key('kelp_photo_1'),
        get_value_for_key('kelp_photo_2'),
        get_value_for_key('kelp_photo_3'),
        get_value_for_key('kelp_photo_4')
    )
