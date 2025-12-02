from netCDF4 import Dataset
import xarray as xr

# for quick viewing & testing.

file_path = "chirps_data/era5_amazon_geopotential500_2000_01.nc"

xrds = xr.open_dataset(file_path)
print(xrds.data_vars)
print(xrds.valid_time.dtype)
