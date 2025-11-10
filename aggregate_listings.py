import pandas as pd
import numpy as np
from pathlib import Path

# ======== CONFIG ========
DATA_DIR = Path("airbnb_data/listings")
OUTLIER_DIR = Path("airbnb_data/removed_outliers")
OUTPUT_FILE = Path("airbnb_data/airbnb_neighbourhood_summary.csv")

# Create output directories if missing
OUTLIER_DIR.mkdir(parents=True, exist_ok=True)

# ======== FILES TO PROCESS ========
files = [
    "2024-12-07_listings.csv",
    "2025-03-02_listings.csv",
    "2025-06-09_listings.csv",
    "2025-09-11_listings.csv"
]

# ======== COLUMNS TO USE ========
cols = [
    'id', 'host_id', 'neighbourhood_cleansed',
    'latitude', 'longitude', 'room_type', 'accommodates',
    'price', 'minimum_nights', 'number_of_reviews', 'review_scores_rating',
    'last_review', 'reviews_per_month', 'calculated_host_listings_count',
    'calculated_host_listings_count_entire_homes', 'calculated_host_listings_count_private_rooms',
    'calculated_host_listings_count_shared_rooms', 'host_listings_count', 'host_is_superhost',
    'amenities', 'last_scraped', 'license', 'availability_90'
]

# ======== FUNCTIONS ========

def clean_and_aggregate(file_path):
    print(f"\nProcessing: {file_path.name}")
    snapshot_date = file_path.stem.split("_")[0]  # e.g., '2025-03-02' → '2025-03-02'

    # --- Load data ---
    df = pd.read_csv(file_path, usecols=cols, low_memory=False)
    df['snapshot_date'] = snapshot_date

    # --- Clean columns ---
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
    df['host_is_superhost'] = df['host_is_superhost'].fillna('f')
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0) # No use
    df['number_of_reviews'] = df['number_of_reviews'].fillna(0) # No use
    df['review_scores_rating'] = df['review_scores_rating'].fillna(df['review_scores_rating'].median()) # No use

    # --- Outlier thresholds ---
    min_nights_threshold = 30
    price_threshold = df['price'].quantile(0.99)

    # --- Remove outliers ---
    outliers = df[(df['minimum_nights'] > min_nights_threshold) | (df['price'] > price_threshold)].copy()
    cleaned = df[(df['minimum_nights'] <= min_nights_threshold) & (df['price'] <= price_threshold)].copy()

    # Save outliers for reference
    outliers.to_csv(OUTLIER_DIR / f"{snapshot_date}_removed_outliers.csv", index=False)

    print(f"  Removed {len(outliers)} outliers ({len(outliers)/len(df)*100:.2f}%)")

    # --- Feature engineering ---
    cleaned['price_per_accommodate'] = cleaned['price'] / cleaned['accommodates']
    cleaned['multi_host_flag'] = (cleaned['calculated_host_listings_count'] > 1).astype(int)

    # --- Aggregate by neighbourhood ---
    agg = cleaned.groupby('neighbourhood_cleansed').agg(
        n_listings=('id', 'count'),
        avg_price=('price', 'mean'),
        median_price=('price', 'median'),
        avg_price_per_person=('price_per_accommodate', 'mean'),
        pct_entire_home=('room_type', lambda x: (x=='Entire home/apt').mean()*100),
        pct_superhost=('host_is_superhost', lambda x: (x=='t').mean()*100),
        avg_availability=('availability_90', 'mean'),
        avg_rating=('review_scores_rating', 'mean'),
        avg_reviews=('number_of_reviews', 'mean'),
        avg_min_nights=('minimum_nights', 'mean'),
        pct_multi_host=('multi_host_flag', 'mean')
    ).reset_index()

    agg['snapshot_date'] = snapshot_date
    return agg


# ======== MAIN PIPELINE ========
if __name__ == "__main__":
    all_aggs = []

    for file in files:
        file_path = DATA_DIR / file
        agg_df = clean_and_aggregate(file_path)
        all_aggs.append(agg_df)

    # Merge all snapshots
    merged = pd.concat(all_aggs, ignore_index=True)
    merged.to_csv(OUTPUT_FILE, index=False)

    print("\n✅ Processing complete!")
    print(f"Saved merged neighbourhood summary → {OUTPUT_FILE}")
    print(f"Outliers saved per month in → {OUTLIER_DIR}")