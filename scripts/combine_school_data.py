import pandas as pd
import os

def combine_school_data():
    all_schools = []

    # Helper to identify if it's a university
    def get_type(row):
        name = str(row['name']).lower()
        if 'universit' in name or 'university' in name or 'unigom' in name or 'unikin' in name or 'unilu' in name or 'isp ' in name or 'ista' in name or 'ispt' in name or 'ucc' in name:
            return 'University/Higher Education'
        return 'School'

    # 1. Load DRC_All_SCHool (1).csv (Primary Source)
    try:
        df1 = pd.read_csv('DRC_All_SCHool (1).csv', low_memory=False)
        temp = pd.DataFrame({
            'name': df1['name'],
            'latitude': df1['latitude'],
            'longitude': df1['longitude'],
            'location_name': df1['addr:city'].fillna(df1['addr:province']),
            'type': df1.apply(get_type, axis=1),
            'source': 'DRC_All_SCHool_Local'
        })
        all_schools.append(temp)
    except Exception as e:
        print(f"Error loading DRC_All_SCHool (1).csv: {e}")

    # 2. Load at_risk_schools.csv
    try:
        df2 = pd.read_csv('at_risk_schools.csv')
        temp = pd.DataFrame({
            'name': df2['name'],
            'latitude': df2['latitude'],
            'longitude': df2['longitude'],
            'location_name': 'Unknown',
            'type': df2.apply(get_type, axis=1),
            'source': 'at_risk_schools_Local'
        })
        all_schools.append(temp)
    except Exception as e:
        print(f"Error loading at_risk_schools.csv: {e}")

    # 3. Load schools_1km_historical.csv
    try:
        df3 = pd.read_csv('schools_1km_historical.csv')
        temp = pd.DataFrame({
            'name': df3['name'],
            'latitude': df3['latitude'],
            'longitude': df3['longitude'],
            'location_name': df3['conflict_location'],
            'type': df3.apply(get_type, axis=1),
            'source': 'schools_1km_historical_Local'
        })
        all_schools.append(temp)
    except Exception as e:
        print(f"Error loading schools_1km_historical.csv: {e}")

    # 4. Load School_Conflict_Event  - Clearn.csv
    try:
        df4 = pd.read_csv('School_Conflict_Event  - Clearn.csv')
        temp = pd.DataFrame({
            'name': df4['name'],
            'latitude': df4['latitude'],
            'longitude': df4['longitude'],
            'location_name': df4['addr:city'],
            'type': df4.apply(get_type, axis=1),
            'source': 'School_Conflict_Event_Local'
        })
        all_schools.append(temp)
    except Exception as e:
        print(f"Error loading School_Conflict_Event  - Clearn.csv: {e}")

    # Add some major universities if not present (manual verification points)
    major_universities = pd.DataFrame([
        {'name': 'Université de Kinshasa (UNIKIN)', 'latitude': -4.4194, 'longitude': 15.3097, 'location_name': 'Kinshasa', 'type': 'University/Higher Education', 'source': 'External Verification'},
        {'name': 'Université de Lubumbashi (UNILU)', 'latitude': -11.6144, 'longitude': 27.4806, 'location_name': 'Lubumbashi', 'type': 'University/Higher Education', 'source': 'External Verification'},
        {'name': 'Université Pédagogique Nationale (UPN)', 'latitude': -4.4042, 'longitude': 15.2569, 'location_name': 'Kinshasa', 'type': 'University/Higher Education', 'source': 'External Verification'},
        {'name': 'Université Protestante au Congo (UPC)', 'latitude': -4.3331, 'longitude': 15.2978, 'location_name': 'Kinshasa', 'type': 'University/Higher Education', 'source': 'External Verification'},
        {'name': 'Université de Kisangani (UNIKIS)', 'latitude': 0.5114, 'longitude': 25.1922, 'location_name': 'Kisangani', 'type': 'University/Higher Education', 'source': 'External Verification'}
    ])
    all_schools.append(major_universities)

    # Combine all
    if all_schools:
        combined = pd.concat(all_schools, ignore_index=True)
        # Remove duplicates based on name and coordinates
        combined = combined.drop_duplicates(subset=['name', 'latitude', 'longitude'])
        
        # Save to CSV
        output_file = 'DRC_SCHOOL_.csv'
        combined.to_csv(output_file, index=False)
        
        # Print summary
        types = combined['type'].value_counts()
        print(f"Successfully updated {output_file}")
        print(f"Total entries: {len(combined)}")
        print(f"Breakdown:\n{types}")
    else:
        print("No data found to combine.")

if __name__ == "__main__":
    combine_school_data()
