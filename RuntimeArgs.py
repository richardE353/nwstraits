# The values in this file will be used for processing the data if no value is entered at the prompts.
# To use, modify the value to the right of each line to be what you want

import os

default_year: int = 2022
default_excel: str = './Kelp_Data_2022_-_all_versions_-_False_-_2022-11-10-17-01-40.xlsx'
default_attach_dir: str = './attachments'
default_output_dir: str = './output'

# login to SmugMug, and follow the API Keys on this page: https://www.smugmug.com/app/account/settings?nick=nwstraits
smug_mug_key: str = 'incorrect api key value'


def select_collection_year() -> int:
    candidate = input("Enter collection year (2022 or later): ").strip()
    if len(candidate) > 0:
        return int(candidate)

    return default_year



