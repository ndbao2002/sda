import pandas as pd
import os
import glob

# Paths
INPUT_DIR = "airbnb_data/calendar_truncated"

# Collect all CSVs
calendar_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.csv")))
all_summaries = []

for file_path in calendar_files:
    print(f"Processing {os.path.basename(file_path)}...")
    df = pd.read_csv(file_path, usecols=['listing_id', 'date', 'available', 'price'], low_memory=False)
    
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
    
    # Aggregate per listing_id
    summary = df.groupby('listing_id').agg(
        avg_price_calendar=('price', 'mean'),
        occupancy_rate=('available', lambda x: 1 - x.mean())  # unavailable fraction
    ).reset_index()
    
    # Save per-file summary
    period_name = os.path.basename(file_path).replace("_calendar.csv", "")
    
    summary['snapshot_date'] = period_name
    all_summaries.append(summary)

# Combine all summaries
calendar_summary_all = pd.concat(all_summaries, ignore_index=True)
calendar_summary_all.to_csv("airbnb_data/merged_calendar_summary.csv", index=False)

print("✅ Calendar cleaning and merging complete!")
