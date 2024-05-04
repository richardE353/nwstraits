import os
import pathlib
import shutil

kobo_attachment_files = {}

normalized_attachment_files = {}


def init_attachment_files(src: str):
    for root, dirs, files in os.walk(src):
        for file in files:
            kobo_attachment_files[file] = os.path.join(root, file)


def find_attachment_path(file_name: str) -> str:
    return normalized_attachment_files[file_name]


def find_path(file_name: str) -> str:
    # KoboToolbox modifies specified file names for export.  Do what they do to the filename
    search_name = remove_invalid_chars(file_name)
    search_name = search_name.replace(" ", "_")

    return kobo_attachment_files[search_name]

def remove_invalid_chars(file_name: str) -> str:
    invalid_chars = [":", ",", ":", "(", ")", "°", "'"]

    clean_str = file_name
    for c in invalid_chars:
        clean_str = clean_str.replace(c, "")

    return clean_str

def copy_file_if_exists(prefix: str, src: str, dest: str, file_name: str, new_name: str):
    if not kobo_attachment_files:
        init_attachment_files(src)

    try:
        file_path = find_path(file_name)
        target_name = prefix + new_name + pathlib.Path(file_name).suffix.lower()
        full_dest = os.path.join(dest, target_name)
        shutil.copy2(file_path, full_dest)

        normalized_attachment_files[file_name] = full_dest
    except KeyError:
        print("Failed to find path for file: " + file_name)

def copy_beach_images_to(dest: str):
    def is_beach_image(name: str) -> bool:
        return '_ToBe.' in name

    files_to_copy = filter(is_beach_image, normalized_attachment_files.values())
    for sf in files_to_copy:
        fn = os.path.basename(sf)
        fd = os.path.join(dest, fn)
        shutil.copy2(sf, fd)

