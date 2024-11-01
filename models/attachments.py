from dataclasses import dataclass

from pandas import Series

from utils.files_helper import copy_file_if_exists

import utils.pandas_helper as ph


@dataclass(frozen=True)
class DataSetAttachments:
    data_sheet_1: str
    data_sheet_2: str
    track_gps_file: str
    second_gps_file: str
    third_gps_file: str
    fourth_gps_file: str
    spreadsheet_1: str
    spreadsheet_2: str

    def copy_files(self, file_prefix: str, src: str, dest: str):
        if len(self.data_sheet_1) > 0:
            copy_file_if_exists(file_prefix, src, dest, self.data_sheet_1, '_DataSheet1')
        if len(self.data_sheet_2) > 0:
            copy_file_if_exists(file_prefix, src, dest, self.data_sheet_2, '_DataSheet2')
        if len(self.track_gps_file) > 0:
            copy_file_if_exists(file_prefix, src, dest, self.track_gps_file, '_Gps1')
        if len(self.second_gps_file) > 0:
            copy_file_if_exists(file_prefix, src, dest, self.second_gps_file, '_Gps2')
        if len(self.third_gps_file) > 0:
            copy_file_if_exists(file_prefix, src, dest, self.second_gps_file, '_Gps3')
        if len(self.fourth_gps_file) > 0:
            copy_file_if_exists(file_prefix, src, dest, self.second_gps_file, '_Gps4')
        if len(self.spreadsheet_1) > 0:
            copy_file_if_exists(file_prefix, src, dest, self.spreadsheet_1, '_SpreadSheet1')
        if len(self.spreadsheet_2) > 0:
            copy_file_if_exists(file_prefix, src, dest, self.spreadsheet_2, '_SpreadSheet2')


def extract_data_attachments(survey_row: Series) -> DataSetAttachments:
    if survey_row.data_sheet_format == "ds_pdf":
        data_sheet_1 = ph.as_string_or_default(survey_row.data_sheet_pdf_1)
        data_sheet_2 = ph.as_string_or_default(survey_row.data_sheet_pdf_2)
    else:
        data_sheet_1 = ph.as_string_or_default(survey_row.data_sheet_page_1)
        data_sheet_2 = ph.as_string_or_default(survey_row.data_sheet_page_2)

    return DataSetAttachments(
        data_sheet_1,
        data_sheet_2,
        ph.as_string_or_default(survey_row.Track_data_file),
        ph.as_string_or_default(survey_row.Second_data_file),
        ph.as_string_or_default(survey_row.Third_data_file),
        ph.as_string_or_default(survey_row.Fourth_data_file),
        ph.as_string_or_default(survey_row.CSV1_data_file),
        ph.as_string_or_default(survey_row.CSV2_data_file)
    )
