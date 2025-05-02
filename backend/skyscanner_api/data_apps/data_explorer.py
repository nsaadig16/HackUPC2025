import json
import os

import pandas as pd

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the parent directory
parent_dir = os.path.dirname(current_dir)
# Path to the CSV file
csv_file_path = os.path.join(parent_dir, 'datasets', 'iata_airports_and_locations_with_vibes.csv')

# Check if file exists
if not os.path.exists(csv_file_path):
    print(f"Error: File {csv_file_path} not found!")
    exit(1)

# Read the CSV data into a DataFrame
df = pd.read_csv(csv_file_path)

# Process the vibes column to convert JSON strings to dictionaries
def parse_vibes(vibes_str):
    if pd.isna(vibes_str) or vibes_str == 'null':
        return None
    try:
        # Replace escaped quotes with regular quotes
        cleaned_str = vibes_str.replace('\\"', '"')
        return json.loads(cleaned_str)
    except:
        return None

df['vibes_dict'] = df['vibes'].apply(parse_vibes)

# Create a dictionary from the DataFrame
airports_dict = df.to_dict('records')

# Generate a summary
summary = {
    'total_airports': len(df),
    'airports_with_vibes': df['vibes_dict'].notna().sum(),
    'latitude_range': f"{df['latitude'].min():.2f} to {df['latitude'].max():.2f}",
    'longitude_range': f"{df['longitude'].min():.2f} to {df['longitude'].max():.2f}",
    'countries_represented': len(df['en-GB'].unique()),
    'underrated_destinations': sum(1 for v in df['vibes_dict'] if v and v.get('underrated_destinations') == '1')
}

# Display results
print("Summary of Airport Data:")
for key, value in summary.items():
    print(f"{key.replace('_', ' ').title()}: {value}")

print("\nSample of the first 3 airports as dictionaries:")
for airport in airports_dict[:3]:
    print(airport)