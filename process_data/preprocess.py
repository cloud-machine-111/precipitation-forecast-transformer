# objectives: Convert CHIRPSv2 and ERA5 to weekly data of resolution of 0.25°
# This involves coarsening CHIRPS rainfall data from 0.05° resolution to 0.25°.
# we then take weekly aggregate statistics of ERA5's hourly environmental data.
# we manipulate with xarray, often used to manipulate geospatial data in .cd format. we output NetCDF after processing.

import argparse 
import numpy as np
from pathlib import Path
from netCDF4 import Dataset
import xarray as xr # handles cdf->array conversion & array operations.
# import xesmf as xe # handles regridding (e.g. coarsenning)

def preprocess_era5(ds: xr.Dataset, var="z") -> xr.Dataset:
    """preprocess era5 geoppotential variables. Takes in xrarray and outputs xrarray. Open netcdf file as xarray, then pass it in."""
    # NOTE: "z" is the data variable for our geopotential data, thus var defaults to z. However, the other ERA & CHIRPS data are unreadable atm, so I don't know whether their data field is also "z".

    # lower resolution:
    ds_coarse = ds.coarsen(latitude=5, longitude=5, boundary="trim").max() # TODO: check that max works

    weekly = ds_coarse.resample(valid_time = "1W")
    
    # take weekly aggr:
    out = xr.Dataset({
        "mean": weekly.mean()[var],
        "median": weekly.median()[var],
        "min": weekly.min()[var],
        "max": weekly.max()[var],
        "std": weekly.std()[var],
        "p25": weekly.quantile(0.25)[var],
        "p75": weekly.quantile(0.75)[var],
    })
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    SAMPLE_FILE = "chirps_data/era5_amazon_geopotential500_2000_01.nc"
    parser.add_argument(
        "input_file",
        nargs="?",                 # ← makes it optional
        default=SAMPLE_FILE,      # ← fallback
        help="Path to ERA5 NetCDF file (optional)"
    )

    args = parser.parse_args()
    path = Path(args.input_file)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    ds = xr.open_dataset(args.input_file)
    out = preprocess_era5(ds)

    print(out)

