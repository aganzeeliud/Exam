import pandas as pd
import os

def harmonize_and_combine():
    # 1. Load UCDP Data
    # Columns of interest: date_start, event_type (type_of_violence), latitude, longitude, where_description, best (fatalities)
    try:
        ucdp = pd.read_csv('ucdp_drc.csv')
        ucdp_processed = pd.DataFrame({
            'date': ucdp['date_start'],
            'event_type': ucdp['type_of_violence'].map({1: 'State-based', 2: 'Non-state', 3: 'One-sided'}),
            'latitude': ucdp['latitude'],
            'longitude': ucdp['longitude'],
            'location': ucdp['where_description'],
            'fatalities': ucdp['best'],
            'source': 'UCDP GED'
        })
        print(f"Loaded {len(ucdp_processed)} records from UCDP.")
    except Exception as e:
        print(f"Error loading UCDP: {e}")
        ucdp_processed = pd.DataFrame()

    # 2. Load Local School Conflict Data
    # Columns: conflict_date, conflict_type, latitude, longitude, addr:city (location)
    try:
        school = pd.read_csv('School_Conflict_Event  - Clearn.csv')
        school_processed = pd.DataFrame({
            'date': school['conflict_date'],
            'event_type': school['conflict_type'],
            'latitude': school['latitude'],
            'longitude': school['longitude'],
            'location': school['addr:city'],
            'fatalities': 0, # Not specified in this dataset
            'source': 'Local School Conflict Data'
        })
        print(f"Loaded {len(school_processed)} records from Local School Data.")
    except Exception as e:
        print(f"Error loading Local School Data: {e}")
        school_processed = pd.DataFrame()

    # 3. Combine
    combined = pd.concat([ucdp_processed, school_processed], ignore_index=True)
    
    # Save
    combined.to_csv('DRC_CONFLICT_EVENT.csv', index=False)
    print(f"Saved {len(combined)} total records to DRC_CONFLICT_EVENT.csv")

if __name__ == "__main__":
    harmonize_and_combine()
