from netCDF4 import Dataset
import os
from pathlib import Path
import logging

# This script checks that downloads are readable in netcdf format. Go to OUTDIR to check files that are readable or unreadable by netcdf4.
OUTDIR = "logging"

# Logger for unreadable files
bad_log = logging.getLogger("bad")
bad_log.setLevel(logging.INFO)
bad_handler = logging.FileHandler(os.path.join(OUTDIR, "unreadable_files.txt"))
bad_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
bad_log.addHandler(bad_handler)

# Logger for readable files
good_log = logging.getLogger("good")
good_log.setLevel(logging.INFO)
good_handler = logging.FileHandler(os.path.join(OUTDIR, "readable_files.txt"))
good_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
good_log.addHandler(good_handler)

# Console logging:
console = logging.StreamHandler()
console.setFormatter(logging.Formatter("%(message)s"))
good_log.addHandler(console)   # prints good results
bad_log.addHandler(console)    # prints bad results

def process_file(file_path):
    print(f"Processing: {file_path}")

    try:
        ds = Dataset(file_path)
        ds.close()

        # If success:
        good_log.info(f"OK: {file_path}")

    except Exception as e:
        bad_log.info(f"BAD: {file_path} — not readable ({repr(e)})")


def iterate_folder(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    for file_path in folder.iterdir():
        if file_path.is_file():
            process_file(file_path)


if __name__ == "__main__":
    iterate_folder("chirps_data")
