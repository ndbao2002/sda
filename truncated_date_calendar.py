import pandas as pd
import datetime as dt

import os

DATE_MAPPING = {
    '2024-12-07': '2025-03-01',
    '2025-03-02': '2025-06-08',
    '2025-06-09': '2025-09-10',
    '2025-09-11': '2025-12-08',
}

INPUT_DIR = "./airbnb_data/calendar/"
OUTPUT_DIR = "./airbnb_data/calendar_truncated/"

def truncate_calendar_dates(df):
    min_date = df.date.min()
    max_date = DATE_MAPPING[min_date]
    truncated_df = df[df.date <= max_date]
    truncated_df = truncated_df[['listing_id', 'date', 'available', 'price']]
    return truncated_df

if "__main__" == __name__:
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".csv"):
            filepath = os.path.join(INPUT_DIR, filename)
            df = pd.read_csv(filepath)
            if len(df) == 0:
                continue
            truncated_df = truncate_calendar_dates(df)
            output_filepath = os.path.join(OUTPUT_DIR, filename)
            truncated_df.to_csv(output_filepath, index=False)
            print(f"Processed and saved: {output_filepath}")