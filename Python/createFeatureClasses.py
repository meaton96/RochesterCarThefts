import os
import pandas as pd
import geopandas as gpd
import plotly.express as px
from arcpy import env
from shutil import copyfile

# Set the working directory
base_dir = "C:\\Temp"
csv_file = os.path.join(base_dir, 'rochester-2011-present.csv')
prj_file = os.path.join(base_dir, 'wgs_84.prj')
output_dir = os.path.join(base_dir, 'output')

# Read the CSV file
data = pd.read_csv(csv_file)

# Filter data for 'Motor Vehicle Theft'
theft_data = data[data['Statute_Text'] == 'Motor Vehicle Theft']

# Create output directory if not exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize a dictionary to hold yearly counts
yearly_counts = {}

# Process data for each year
for year in range(2011, 2024):
    yearly_data = theft_data[theft_data['OccurredFrom_Date_Year'] == year]
    yearly_counts[year] = yearly_data.shape[0]  # Add the count for the year
    
    # Convert DataFrame to GeoDataFrame
    gdf = gpd.GeoDataFrame(
        yearly_data, 
        geometry=gpd.points_from_xy(yearly_data.X, yearly_data.Y),
        crs="EPSG:3857"  # WGS 84 Web Mercator (Auxiliary Sphere)
    )

    # Create output folder for the year
    year_output_dir = os.path.join(output_dir, str(year))
    if not os.path.exists(year_output_dir):
        os.makedirs(year_output_dir)

    # Define the shapefile path
    shapefile_path = os.path.join(year_output_dir, f"theft_{year}.shp")

    # Export to shapefile
    gdf.to_file(shapefile_path)

    # Copy the .prj file
    copyfile(prj_file, shapefile_path.replace('.shp', '.prj'))

# Create the bar graph using Plotly
df_plot = pd.DataFrame(list(yearly_counts.items()), columns=['Year', 'Motor Vehicle Thefts'])
fig = px.bar(df_plot, x='Year', y='Motor Vehicle Thefts', title='Motor Vehicle Thefts by Year')
fig.show()

print("Shapefiles created for each year.")
