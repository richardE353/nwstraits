from dataclasses import dataclass

from pandas import Series

import utils.FilesHelper as fh
import utils.PandasHelper as ph


@dataclass(frozen=True)
class VolunteerInfo:
    lead_name: str
    names: str
    image_file_1: str
    image_file_2: str
    image_file_3: str
    image_file_4: str

    def copy_files(self, file_prefix: str, src: str, dest: str):
        if len(self.image_file_1) > 0:
            fh.copy_file_if_exists(file_prefix, src, dest, self.image_file_1, '_volunteer1')
        if len(self.image_file_2) > 0:
            fh.copy_file_if_exists(file_prefix, src, dest, self.image_file_2, '_volunteer2')
        if len(self.image_file_3) > 0:
            fh.copy_file_if_exists(file_prefix, src, dest, self.image_file_3, '_volunteer3')
        if len(self.image_file_4) > 0:
            fh.copy_file_if_exists(file_prefix, src, dest, self.image_file_4, '_volunteer4')


def extract_volunteer_info(ds: Series) -> VolunteerInfo:
    return VolunteerInfo(
        ph.as_string_or_default(ds.team_leader),
        ph.as_string_or_default(ds.name_of_surveyors),  # Scala code used Volunteer_Names
        ph.as_string_or_default(ds.volunteer_photo_1),
        ph.as_string_or_default(ds.volunteer_photo_2),
        ph.as_string_or_default(ds.volunteer_photo_3),
        ph.as_string_or_default(ds.volunteer_photo_4)
    )
