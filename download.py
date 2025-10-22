
import requests
import gzip
import shutil
import os

listing_link = [
    "https://data.insideairbnb.com/italy/veneto/venice/2025-09-11/data/listings.csv.gz",
    "https://data.insideairbnb.com/italy/veneto/venice/2025-06-09/data/listings.csv.gz",
    "https://data.insideairbnb.com/italy/veneto/venice/2025-03-02/data/listings.csv.gz",
    "https://data.insideairbnb.com/italy/veneto/venice/2024-12-07/data/listings.csv.gz",
]

calendar_link = [
    "https://data.insideairbnb.com/italy/veneto/venice/2025-09-11/data/calendar.csv.gz",
    "https://data.insideairbnb.com/italy/veneto/venice/2025-06-09/data/calendar.csv.gz",
    "https://data.insideairbnb.com/italy/veneto/venice/2025-03-02/data/calendar.csv.gz",
    "https://data.insideairbnb.com/italy/veneto/venice/2024-12-07/data/calendar.csv.gz",
]

geo_link = "https://data.insideairbnb.com/italy/veneto/venice/2025-09-11/visualisations/neighbourhoods.geojson"

def download_and_extract(url, output_dir):
    local_filename = url.split('/')[-1]
    local_filepath = os.path.join(output_dir, local_filename)

    # Download the file
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # Extract the gzip file
    extracted_filepath = local_filepath[:-3]  # Remove .gz extension
    with gzip.open(local_filepath, 'rb') as f_in:
        with open(extracted_filepath, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Rename the extracted file to match month and year from URL
    date_part = url.split('/')[-3]
    new_filename = f"{date_part}_{os.path.basename(extracted_filepath)}"
    new_filepath = os.path.join(output_dir, new_filename)
    os.rename(extracted_filepath, new_filepath)

    # Remove the gzip file
    os.remove(local_filepath)

    return new_filepath

output_directory = "airbnb_data"
os.makedirs(output_directory, exist_ok=True)

# Create folder for listing files
listing_directory = os.path.join(output_directory, "listings")
os.makedirs(listing_directory, exist_ok=True)

for link in listing_link:
    extracted_file = download_and_extract(link, listing_directory)
    print(f"Extracted listing file: {extracted_file}")

# Create folder for calendar files
calendar_directory = os.path.join(output_directory, "calendar")
os.makedirs(calendar_directory, exist_ok=True)

for link in calendar_link:
    extracted_file = download_and_extract(link, calendar_directory)
    print(f"Extracted calendar file: {extracted_file}")

# Download geojson file to output directory
# I haven't try this yet, but it should work
geo_response = requests.get(geo_link)
geo_filepath = os.path.join(output_directory, "neighbourhoods.geojson")
with open(geo_filepath, 'wb') as f:
    f.write(geo_response.content)
print(f"Downloaded geojson file: {geo_filepath}")
