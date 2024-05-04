# The values in this file will be used for processing the data if no value is entered at the prompts.
# To use, modify the value to the right of each line to be what you want

import os

default_year: int = 2023

default_excel: str = '/Users/Richard/Documents/NWStraits/KelpProject/2023_Data/Kelp_Data_2023_-_all_versions_-_False_-_2023-12-28-19-01-19.xlsx'
default_attach_dir: str = '/Users/Richard/Documents/NWStraits/KelpProject/2023_Data/attachments'
default_output_dir: str = '/Users/Richard/Documents/NWStraits/KelpProject/testing'

# login to SmugMug, and follow the API Keys on this page: https://www.smugmug.com/app/account/settings?nick=nwstraits
smug_mug_key: str = 'go get the right key from Suzanne'


def select_collection_year() -> int:
    candidate = input("Enter collection year (2022 or later): ").strip()
    if len(candidate) > 0:
        return int(candidate)

    return default_year

def select_database_path() -> str:
    input_xlsx = input("Enter .xlsx file to read: ").strip()
    if len(input_xlsx) > 0:
        return input_xlsx

    return default_excel

def select_attachment_dir() -> str:
    attach_dir = input("Enter directory containing attachments: ").strip()
    if len(attach_dir) > 0:
        return attach_dir

    return default_attach_dir

def select_target_dir(year: int) -> str:
    output_dir = input("Output directory: ").strip()
    if len(output_dir) > 0:
        return output_dir

    return os.path.join(default_output_dir, str(year))

def print_runtime_args(args: list):
    print("Runtime parameters")
    for k, v in args:
        print("\t" + k + ": " + v)
