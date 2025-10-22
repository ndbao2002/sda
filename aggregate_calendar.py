import pandas as pd
import os
import glob

# Paths
INPUT_DIR = "airbnb_data/calendar_truncated"
INPUT_LISTINGS_DIR = "airbnb_data/listings"

# Collect all CSVs
calendar_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.csv")))

# Take corresponding listing files
listing_files = []
for calendar_file in calendar_files:
    period_name = os.path.basename(calendar_file).replace("_calendar.csv", "")
    listing_file = os.path.join(INPUT_LISTINGS_DIR, f"{period_name}_listings.csv")
    listing_files.append(listing_file)
all_summaries = []

for (calendar_file, listing_file) in zip(calendar_files, listing_files):
    print(f"Processing {os.path.basename(calendar_file)} and {os.path.basename(listing_file)}...")
    df = pd.read_csv(calendar_file, usecols=['listing_id', 'date', 'available', 'price'], low_memory=False)
    listings_df = pd.read_csv(listing_file, usecols=['id', 'neighbourhood_cleansed'], low_memory=False)
    
    # Drop null rows safely (retain rows with valid data)
    df = df.dropna(subset=['available', 'price'])
    
    # Clean price (remove $ and commas)
    df['price'] = (
        df['price']
        .astype(str)
        .str.replace(r'[\$,]', '', regex=True)
        .astype(float)
    )
    
    # Convert available to boolean
    df['available'] = df['available'].map({'t': True, 'f': False})

    # Merge with listings to get neighbourhood info
    df = df.merge(listings_df, left_on='listing_id', right_on='id', how='left')
    df.drop(columns=['id'], inplace=True)

    # Aggregate per neighborhood -> per date
    summary = df.groupby(['neighbourhood_cleansed', 'date']).agg(
        avg_price_calendar=('price', 'mean'),
        occupancy_rate=('available', lambda x: 1 - x.mean())  # unavailable fraction
    ).reset_index()
    
    # Save per-file summary
    period_name = os.path.basename(calendar_file).replace("_calendar.csv", "")
    
    summary['snapshot_date'] = period_name
    all_summaries.append(summary)

# Combine all summaries
calendar_summary_all = pd.concat(all_summaries, ignore_index=True)
calendar_summary_all.to_csv("airbnb_data/merged_calendar_summary.csv", index=False)

print("✅ Calendar cleaning and merging complete!")
