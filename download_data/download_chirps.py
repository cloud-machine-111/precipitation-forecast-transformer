import os
import time
import logging
import cdsapi
import requests

# Output folder
OUTDIR = "./chirps_data"
os.makedirs(OUTDIR, exist_ok=True)

# Logging
logging.basicConfig(filename=os.path.join(OUTDIR, "download_log.txt"),
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Regions
regions = {
    "amazon": [5, -75, -20, -45],
    "southern_brazil": [-28, -55, -34, -48]
}

# Years and months
years = range(2000, 2001) # 1980 - 2021
months = range(1, 13)

# Hours for ERA5
hours = [f"{h:02d}:00" for h in range(24)]

# CDS API client
c = cdsapi.Client()

def file_exists(path):
    return os.path.exists(path)

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

def download_chirps(year, month, region_name):
    month_str = f"{month:02d}"
    filename = os.path.join(OUTDIR, f"chirps_{region_name}_{year}_{month_str}.nc")
    if file_exists(filename):
        logging.info(f"CHIRPS file exists, skipping: {filename}")
        return
    url = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p25/chirps-v2.0.{year}.{month_str}.days_p25.nc"
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        logging.info(f"Downloaded CHIRPS: {filename}")
    except Exception as e:
        logging.error(f"Failed CHIRPS download {filename}: {e}")

# Main loop
for year in years:
    for month in months:
        month_str = f"{month:02d}"
        for region_name, area in regions.items():
            # ERA5 single-level
            era5_file = os.path.join(OUTDIR, f"era5_{region_name}_single_levels_{year}_{month_str}.nc")
            if not file_exists(era5_file):
                logging.info(f"Downloading ERA5 single-level: {era5_file}")
                download_with_retry(
                    c.retrieve,
                    "reanalysis-era5-land",
                    {
                        "variable": ["2m_temperature","volumetric_soil_water_layer_1"],
                        "area": area,
                        "year": str(year),
                        "month": month_str,
                        "day": [f"{d:02d}" for d in range(1, 32)],
                        "time": hours,
                        "format": "netcdf"
                    },
                    era5_file
                )

            # ERA5 500 hPa geopotential
            era5_press_file = os.path.join(OUTDIR, f"era5_{region_name}_geopotential500_{year}_{month_str}.nc")
            if not file_exists(era5_press_file):
                logging.info(f"Downloading ERA5 geopotential 500hPa: {era5_press_file}")
                download_with_retry(
                    c.retrieve,
                    "reanalysis-era5-pressure-levels",
                    {
                        "product_type": "reanalysis",
                        "variable": ["geopotential"],
                        "pressure_level": ["500"],
                        "area": area,
                        "year": str(year),
                        "month": month_str,
                        "day": [f"{d:02d}" for d in range(1, 32)],
                        "time": hours,
                        "format": "netcdf"
                    },
                    era5_press_file
                )

            # CHIRPS
            download_chirps(year, month, region_name)

logging.info("All downloads complete!")
