DRC Conflict & Schools Analysis
This project analyzes the proximity of schools in the Democratic Republic of the Congo to known conflict events.Strategic Objectives
1. Develop a data-driven strategy
Design an integrated system that uses open data (conflict events, health, school locations) to identify how conflict dynamics affect education access.
2. Create geospatial monitoring tools
Create interactive maps and dashboards that visualize education risk and support real-time monitoring of schools during conflict events.
3. Build EBI staff capacity for scalable use
Train staff to interpret spatial risk outputs and replicate the methodology across different infrastructure types and humanitarian sectors.

🌍 Live Map
You can view the interactive map here: [https://aganzeeliud.github.io/Crash_Course_Exam/](https://aganzeeliud.github.io/Exam/index.html)
Intelligence for a safer education.
Providing geospacial visibility into the impact of armed conflict on school systems across the Democratic Republic of Congo
📊 Features
Map View: Interactive Leaflet map showing schools that are located near conflict events.
Data Analysis:
National Risk Map https://aganzeeliud.github.io/Exam/map.html
Regional Risqk Map https://aganzeeliud.github.io/Exam/map-kivu.html
At-Risk Schools: Schools within 10km of a conflict event.
Safe Schools: Schools further than 10km from conflict events.
Data Sources:
Schools: Fetched from OpenStreetMap via Overpass API.
Conflicts: Provided via CSV.
📁 Project Structure
/data: Contains the processed CSV and GeoJSON datasets.
/scripts: Python scripts used for data fetching, conversion, and risk analysis.
index.html & map.js: The code for the interactive web map.
Methodology & Transparency
Our system utilizes a unified data pipeline aggregating conflict data from ACLED and UCDP GED. Schools are geolocated using GRID3 and OSM datasets. Risk classification is determined via an automated Haversine distance analysis, flagging any facility within a 10km radius of a conflict event.
🛠 Tools Used
Python: For data processing and Haversine distance calculations.
Leaflet.js: For the interactive mapping interface.
GitHub Pages: For hosting the live analysis.
