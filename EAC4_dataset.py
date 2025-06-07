import cdsapi

client = cdsapi.Client()

dataset = "cams-global-reanalysis-eac4"

variables = [
    "black_carbon_aerosol_optical_depth_550nm",
    "dust_aerosol_optical_depth_550nm",
    "organic_matter_aerosol_optical_depth_550nm",
    "particulate_matter_2.5um",
    "sea_salt_aerosol_optical_depth_550nm",
    "sulphate_aerosol_optical_depth_550nm",
    "total_aerosol_optical_depth_550nm",
    "total_column_formaldehyde",
    "total_column_isoprene",
    "total_column_nitrogen_dioxide",
    "total_column_ozone",
    "total_column_peroxyacetyl_nitrate"
]

# Years from 2003 to 2024
years = list(range(2003, 2025))

# Months (May to August)
months = ["05", "06", "07", "08"]
month_names = ["May", "Jun", "Jul", "Aug"]

for var in variables:
    for year in years:
        for i, month in enumerate(months):
            # Create date range for the specific month
            if month == "02":
                # Handle February (leap year consideration)
                if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                    end_day = "29"
                else:
                    end_day = "28"
            elif month in ["04", "06", "09", "11"]:
                end_day = "30"
            else:
                end_day = "31"
            
            date_range = f"{year}-{month}-01/{year}-{month}-{end_day}"
            
            request = {
                "date": [date_range],
                "time": [
                    "00:00", "03:00", "06:00",
                    "09:00", "12:00", "15:00",
                    "18:00", "21:00"
                ],
                "data_format": "netcdf_zip",
                "variable": [var]
            }
            
            # Create descriptive filename
            var_short = var.replace("_", "-")
            save_path = "/Users/parvjain/Library/CloudStorage/GoogleDrive-jparv@stanford.edu/My Drive/EAC4_data"
            filename = f"{save_path}/CAMS_{var_short}_{year}_{month_names[i]}.zip"

            print(f"Downloading: {filename}")
            client.retrieve(dataset, request).download(filename)
