"""
Process KoboToolbox export of data in an Excel file and an associated attachment directory.
"""
import os
import sys

import pandas as pd
from pandas import DataFrame

from models.GISKelpDataFrame import create_gis_excel_workbook
from models.KelpDataRow import extract_rows
from utils.FilesHelper import copy_beach_images_to
from utils.KelpDataLog import KelpDataLog

import RuntimeArgs as rt_args


def main():
    data_year: int = rt_args.select_collection_year()
    input_xlsx = select_database_path()
    start_date = select_start_date()
    attach_dir = select_attachment_dir()
    output_dir = select_target_dir(data_year)

    user_params = [("Year", str(data_year)),
                   ("Excel File", input_xlsx),
                   ("Attachments", attach_dir),
                   ("Start Date", start_date),
                   ("Target", output_dir)]

    print_runtime_args(user_params)

    print('\n\tcopying attachments to output directory.')
    df = pd.read_excel(input_xlsx).sort_values("data_county")
    surveys_by_county = extract_surveys_by_county(df)

    counties = list(surveys_by_county.keys())
    create_target_directories(counties, output_dir)

    copy_attachments_to_target_dir(surveys_by_county, attach_dir, output_dir)

    print('\texporting GIS Worksheet.')
    create_gis_excel_workbook(surveys_by_county, output_dir)

    print('\tcreating log file.')
    logger = KelpDataLog(user_params, output_dir, surveys_by_county)
    logger.create_and_write_log()

    print('Done.')


def copy_attachments_to_target_dir(surveys_by_county: dict, attachments_dir: str, target: str):
    for county in surveys_by_county.keys():
        for s in surveys_by_county[county]:
            s.copy_files(attachments_dir, target)

    album_dir = os.path.join(target, 'to_beach_album')
    copy_beach_images_to(album_dir)


def extract_surveys_by_county(df: DataFrame) -> dict:
    grouped_rows = dict(tuple(df.groupby('data_county')))

    surveys_by_county = dict()
    for cty in grouped_rows.keys():
        surveys_by_county[cty] = extract_rows(grouped_rows[cty])

    return surveys_by_county


def select_start_date() -> str:
    candidate = input("Enter starting submission date (yyyy-mm-dd) (blank = process all data): ").strip()
    if len(candidate) > 0:
        return candidate

    return str(rt_args.default_year) + "-01-01"


def select_database_path() -> str:
    input_xlsx = input("Enter .xlsx file to read: ").strip()
    if len(input_xlsx) > 0:
        return input_xlsx

    return rt_args.default_excel


def select_attachment_dir() -> str:
    attach_dir = input("Enter directory containing attachments: ").strip()
    if len(attach_dir) > 0:
        return attach_dir

    return rt_args.default_attach_dir


def select_target_dir(year: int) -> str:
    output_dir = input("Output directory: ").strip()
    if len(output_dir) > 0:
        return output_dir

    return os.path.join(rt_args.default_output_dir, str(year))


# https://stackoverflow.com/questions/69998096/how-to-create-multiple-folders-inside-a-directory
def create_target_directories(c_names, base_dir):
    try:
        sub_dirs = ["data_files", "site_photos", "volunteer_photos"]
        for cty_name in c_names:
            cty_path = os.path.join(base_dir, cty_name)
            os.makedirs(cty_path)
            for leaf in sub_dirs:
                os.makedirs(os.path.join(cty_path, leaf))

        album_dir = os.path.join(base_dir, 'to_beach_album')
        os.makedirs(album_dir)
    except FileExistsError:
        print("Invalid output directory.  Make sure directory does not exist, or is writable")


def print_runtime_args(args: list):
    print("Runtime parameters")
    for k, v in args:
        print("\t" + k + ": " + v)


if __name__ == "__main__":
    sys.exit(main())
