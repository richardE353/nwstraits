"""
Process KoboToolbox export of data in an Excel file and an associated attachment directory.
"""

from models.anchor_row import extract_rows

import os
import sys

import pandas as pd
from pandas import DataFrame

import runtime_args as rt_args
from utils.anchoring_log import AnchoringLog


def main():
    data_year: int = rt_args.select_collection_year()
    input_xlsx = rt_args.select_database_path()
    attach_dir = rt_args.select_attachment_dir()
    output_dir = rt_args.select_target_dir(data_year)

    user_params = [("Year", str(data_year)),
                   ("Excel File", input_xlsx),
                   ("Attachments", attach_dir),
                   ("Target", output_dir)]

    rt_args.print_runtime_args(user_params)

    print('\n\tcopying attachments to output directory.')
    df = pd.read_excel(input_xlsx).sort_values("data_county")
    surveys_by_county = extract_surveys_by_county(df)

    counties = list(surveys_by_county.keys())
    create_target_directories(counties, output_dir)

    copy_attachments_to_target_dir(surveys_by_county, attach_dir, output_dir)

    print('\tcreating log file.')
    logger = AnchoringLog(user_params, output_dir, surveys_by_county)
    logger.create_and_write_log(data_year)

    print('Done.')


def create_target_directories(c_names, base_dir):
    try:
        for cty_name in c_names:
            cty_path = os.path.join(base_dir, cty_name, 'site_photos')
            os.makedirs(cty_path)
    except FileExistsError:
        print("Invalid output directory.  Make sure directory does not exist, or is writable")


def extract_surveys_by_county(df: DataFrame) -> dict:
    grouped_rows = dict(tuple(df.groupby('data_county')))

    surveys_by_county = dict()
    for cty in grouped_rows.keys():
        surveys_by_county[cty] = extract_rows(grouped_rows[cty])

    return surveys_by_county


def copy_attachments_to_target_dir(surveys_by_county: dict, attachments_dir: str, target: str):
    for county in surveys_by_county.keys():
        cnty_dir = os.path.join(target, county, 'site_photos')
        for s in surveys_by_county[county]:
            s.copy_files(attachments_dir, cnty_dir)


if __name__ == "__main__":
    sys.exit(main())
