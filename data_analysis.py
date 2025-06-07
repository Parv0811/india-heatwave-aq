import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import zipfile
import tempfile

# Step 1: Define the file paths
zip_path = "/Users/parvjain/Library/CloudStorage/GoogleDrive-jparv@stanford.edu/MyDrive/EAC4_data/CAMS_black-carbon-aerosol-optical-depth-550nm_2003_Jul.zip"

# Create a temporary directory to extract files
with tempfile.TemporaryDirectory() as temp_dir:
    # Extract the ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Find the .nc file in the extracted contents
    nc_file = next(f for f in os.listdir(temp_dir) if f.endswith('.nc'))
    nc_path = os.path.join(temp_dir, nc_file)
    
    # Open the NetCDF file
    with Dataset(nc_path, mode='r') as nc:
        # Step 3: Explore available variables
        print("Variables in the file:")
        print(nc.variables.keys())

        # Step 4: Extract relevant variables
        data_var = nc.variables["aod550"][:]  
        lat = nc.variables["latitude"][:]
        lon = nc.variables["longitude"][:]
        
        # Step 5: Prepare data for plotting
        data_var = np.squeeze(data_var)  # remove time or singleton dimensions if needed

        # Step 6: Plot the data
        plt.figure(figsize=(12, 6))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_global()

        # Add map features
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.gridlines(draw_labels=True)

        # Plot the aerosol data
        aerosol = ax.pcolormesh(lon, lat, data_var, transform=ccrs.PlateCarree(), cmap='OrRd')

        # Add colorbar
        cb = plt.colorbar(aerosol, orientation='horizontal', pad=0.05, aspect=50)
        cb.set_label("Black Carbon Aerosol Optical Depth @ 550nm")

        # Title
        plt.title("CAMS Black Carbon Aerosol Optical Depth (550nm)")

        plt.tight_layout()
        plt.show()