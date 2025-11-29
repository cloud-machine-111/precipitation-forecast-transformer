import cdsapi
import os
import time
import logging

# Initialize CDS API
c = cdsapi.Client()

# Output folder
OUTDIR = "/users/hsoaresb/data/hsoaresb/"
os.makedirs(OUTDIR, exist_ok=True)

# Logging setup
logging.basicConfig(filename=OUTDIR + 'download_log.txt',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Southern Brazil (North, West, South, East)
southern_brazil_area = [-22, -57, -34, -48]

# Hours for hourly data
hours = [f"{h:02d}:00" for h in range(24)]

# Years and months to download
years = range(1980, 2021)
months = range(1, 13)

# Check if file exists
def file_exists(path):
    return os.path.exists(path)

# Function to download with retry
def download_with_retry(func, *args, max_retries=5, sleep_sec=10):
    retries = 0
    while retries < max_retries:
        try:
            func(*args)
            return True
        except Exception as e:
            retries += 1
            logging.warning(f"Download failed: {e}. Retry {retries}/{max_retries} after {sleep_sec}s.")
            time.sleep(sleep_sec)
    logging.error(f"Failed after {max_retries} retries: {args}")
    return False

for year in years:
    for month in months:
        month_str = f"{month:02d}"

        # -----------------------------
        # Single-level variables
        # -----------------------------
        single_file = f"{OUTDIR}era5_amazon_single_levels_{year}_{month_str}.nc"
        if file_exists(single_file):
            logging.info(f"Single-level file exists, skipping: {single_file}")
        else:
            logging.info(f"Downloading single-level data for {year}-{month_str}")
            download_with_retry(
                c.retrieve,
                "reanalysis-era5-land",
                {
                    "variable": [
                        "2m_temperature",
                        "volumetric_soil_water_layer_1"
                    ],
                    "area": amazon_area,
                    "year": str(year),
                    "month": month_str,
                    "day": [f"{d:02d}" for d in range(1, 32)],
                    "time": hours,
                    "format": "netcdf"
                },
                single_file
            )

        # -----------------------------
        # Pressure-level variable: geopotential 500 hPa
        # -----------------------------
        pressure_file = f"{OUTDIR}era5_amazon_geopotential500_{year}_{month_str}.nc"
        if file_exists(pressure_file):
            logging.info(f"Pressure-level file exists, skipping: {pressure_file}")
        else:
            logging.info(f"Downloading geopotential 500hPa for {year}-{month_str}")
            download_with_retry(
                c.retrieve,
                "reanalysis-era5-pressure-levels",
                {
                    "product_type": "reanalysis",
                    "variable": ["geopotential"],
                    "pressure_level": ["500"],
                    "area": amazon_area,
                    "year": str(year),
                    "month": month_str,
                    "day": [f"{d:02d}" for d in range(1, 32)],
                    "time": hours,
                    "format": "netcdf"
                },
                pressure_file
            )

logging.info("All downloads complete!")

