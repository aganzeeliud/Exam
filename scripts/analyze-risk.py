import pandas as pd
import numpy as np
import os

def haversine_vectorized(lat1, lon1, lat2_vec, lon2_vec):
    """
    Calculate the great circle distance between a point and an array of points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lat1, lon1, lat2_vec, lon2_vec = map(np.radians, [lat1, lon1, lat2_vec, lon2_vec])

    # Haversine formula 
    dlat = lat2_vec - lat1 
    dlon = lon2_vec - lon1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2_vec) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def analyze_risk():
    processed_dir = 'processed-data'
    output_dir = os.path.join(processed_dir, 'drc-conflict-risk-school')
    os.makedirs(output_dir, exist_ok=True)

    # Load data
    schools = pd.read_csv(os.path.join(processed_dir, 'drc-school.csv'))
    conflicts = pd.read_csv(os.path.join(processed_dir, 'drc-conflict-event.csv'))

    # Convert coordinates to numeric, coercing errors to NaN
    schools['latitude'] = pd.to_numeric(schools['latitude'], errors='coerce')
    schools['longitude'] = pd.to_numeric(schools['longitude'], errors='coerce')
    conflicts['latitude'] = pd.to_numeric(conflicts['latitude'], errors='coerce')
    conflicts['longitude'] = pd.to_numeric(conflicts['longitude'], errors='coerce')

    # Drop rows with missing coordinates
    schools = schools.dropna(subset=['latitude', 'longitude'])
    conflicts = conflicts.dropna(subset=['latitude', 'longitude'])

    conflict_lats = conflicts['latitude'].values
    conflict_lons = conflicts['longitude'].values

    min_distances = []
    
    print(f"Analyzing {len(schools)} schools against {len(conflicts)} conflict events...")

    for i, school in schools.iterrows():
        distances = haversine_vectorized(school['latitude'], school['longitude'], conflict_lats, conflict_lons)
        min_distances.append(np.min(distances))
        if (i + 1) % 1000 == 0:
            print(f"Processed {i + 1} schools...")

    schools['distance_to_nearest_conflict_km'] = min_distances
    
    # Define risk status: "at-risk" if within 10km (encompassing the 5-10km range mentioned)
    # The prompt mentioned "within 5-10km as at-risk" and "1km is a reasonable proximity threshold".
    # I will classify as 'at-risk' if distance <= 10km.
    schools['risk_status'] = np.where(schools['distance_to_nearest_conflict_km'] <= 10, 'at-risk', 'safe')

    # Save to two files
    at_risk = schools[schools['risk_status'] == 'at-risk']
    safe = schools[schools['risk_status'] == 'safe']

    at_risk.to_csv(os.path.join(output_dir, 'at-risk-schools.csv'), index=False)
    safe.to_csv(os.path.join(output_dir, 'safe-schools.csv'), index=False)

    print(f"Analysis complete.")
    print(f"At-risk schools: {len(at_risk)}")
    print(f"Safe schools: {len(safe)}")
    print(f"Files saved to {output_dir}")

if __name__ == "__main__":
    analyze_risk()
