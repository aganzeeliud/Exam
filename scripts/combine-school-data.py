import pandas as pd
import os

def combine_school_data():
    raw_dir = 'raw-data'
    processed_dir = 'processed-data'
    all_schools = []

    def get_type(row):
        name = str(row['name']).lower()
        if 'universit' in name or 'university' in name or 'unigom' in name or 'unikin' in name or 'unilu' in name or 'isp ' in name or 'ista' in name or 'ispt' in name or 'ucc' in name:
            return 'University/Higher Education'
        return 'School'

    # 1. Load drc-all-school.csv
    try:
        df1 = pd.read_csv(os.path.join(raw_dir, 'drc-all-school.csv'), low_memory=False)
        temp = pd.DataFrame({
            'name': df1['name'],
            'latitude': df1['latitude'],
            'longitude': df1['longitude'],
            'location_name': df1['addr:city'].fillna(df1['addr:province']),
            'type': df1.apply(get_type, axis=1),
            'source': 'drc-all-school-local'
        })
        all_schools.append(temp)
    except Exception as e:
        print(f"Error loading drc-all-school.csv: {e}")

    # 2. Load at-risk-schools.csv
    try:
        df2 = pd.read_csv(os.path.join(raw_dir, 'at-risk-schools.csv'))
        temp = pd.DataFrame({
            'name': df2['name'],
            'latitude': df2['latitude'],
            'longitude': df2['longitude'],
            'location_name': 'Unknown',
            'type': df2.apply(get_type, axis=1),
            'source': 'at-risk-schools-local'
        })
        all_schools.append(temp)
    except Exception as e:
        print(f"Error loading at-risk-schools.csv: {e}")

    # 3. Load schools-1km-historical.csv
    try:
        df3 = pd.read_csv(os.path.join(raw_dir, 'schools-1km-historical.csv'))
        temp = pd.DataFrame({
            'name': df3['name'],
            'latitude': df3['latitude'],
            'longitude': df3['longitude'],
            'location_name': df3['conflict_location'],
            'type': df3.apply(get_type, axis=1),
            'source': 'schools-1km-historical-local'
        })
        all_schools.append(temp)
    except Exception as e:
        print(f"Error loading schools-1km-historical.csv: {e}")

    # 4. Load school-conflict-event-clearn.csv
    try:
        df4 = pd.read_csv(os.path.join(raw_dir, 'school-conflict-event-clearn.csv'))
        temp = pd.DataFrame({
            'name': df4['name'],
            'latitude': df4['latitude'],
            'longitude': df4['longitude'],
            'location_name': df4['addr:city'],
            'type': df4.apply(get_type, axis=1),
            'source': 'school-conflict-event-local'
        })
        all_schools.append(temp)
    except Exception as e:
        print(f"Error loading school-conflict-event-clearn.csv: {e}")

    # Major Universities
    major_universities = pd.DataFrame([
        {'name': 'Université de Kinshasa (UNIKIN)', 'latitude': -4.4194, 'longitude': 15.3097, 'location_name': 'Kinshasa', 'type': 'University/Higher Education', 'source': 'External Verification'},
        {'name': 'Université de Lubumbashi (UNILU)', 'latitude': -11.6144, 'longitude': 27.4806, 'location_name': 'Lubumbashi', 'type': 'University/Higher Education', 'source': 'External Verification'},
        {'name': 'Université Pédagogique Nationale (UPN)', 'latitude': -4.4042, 'longitude': 15.2569, 'location_name': 'Kinshasa', 'type': 'University/Higher Education', 'source': 'External Verification'},
        {'name': 'Université Protestante au Congo (UPC)', 'latitude': -4.3331, 'longitude': 15.2978, 'location_name': 'Kinshasa', 'type': 'University/Higher Education', 'source': 'External Verification'},
        {'name': 'Université de Kisangani (UNIKIS)', 'latitude': 0.5114, 'longitude': 25.1922, 'location_name': 'Kisangani', 'type': 'University/Higher Education', 'source': 'External Verification'}
    ])
    all_schools.append(major_universities)

    if all_schools:
        combined = pd.concat(all_schools, ignore_index=True)
        combined = combined.drop_duplicates(subset=['name', 'latitude', 'longitude'])
        combined.to_csv(os.path.join(processed_dir, 'drc-school.csv'), index=False)
        print(f"Successfully updated drc-school.csv with {len(combined)} entries.")

if __name__ == "__main__":
    combine_school_data()
