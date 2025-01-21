import json
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

# Step 1: Read and parse the JSON data
file_path = 'data.json'

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"File {file_path} not found.")
    exit(1)
except json.JSONDecodeError as e:
    print("Failed to decode JSON:", e)
    exit(1)

# Step 2: Extract segments and riders
segments = [segment['name'] for segment in data.get('segmentScores', [])]
riders = [racer['name'] for racer in data.get('racerScores', [])]

# Step 3: Create MultiIndex for columns
multi_columns = []
for segment in segments:
    multi_columns.append((segment, 'fts'))
    multi_columns.append((segment, 'fal'))

columns = pd.MultiIndex.from_tuples(multi_columns, names=['Segment', 'Point_Type'])

# Step 4: Initialize the DataFrame
points_df = pd.DataFrame(0, index=riders, columns=columns)

# Step 5: Populate the DataFrame
for segment in data.get('segmentScores', []):
    segment_name = segment['name']
    
    # Populate FTS points
    for fts in segment.get('fts', []):
        rider_name = fts.get('name', 'Unknown')
        points = fts.get('points', 0)
        if rider_name in riders:
            points_df.at[rider_name, (segment_name, 'fts')] = points
    
    # Populate FAL points
    for fal in segment.get('fal', []):
        rider_name = fal.get('name', 'Unknown')
        points = fal.get('points', 0)
        if rider_name in riders:
            points_df.at[rider_name, (segment_name, 'fal')] = points



# Populate 'finPoints' from racerScores
for racer in data.get('racerScores', []):
    rider_name = racer.get('name', 'Unknown')
    fin_points = racer.get('finPoints', 0)
    if rider_name in riders:
        points_df.at[rider_name, ('Finish','fin')] = fin_points

# Step 7: Add Total Points per Rider
points_df[('Total Points','tot')] = points_df.sum(axis=1)

# Step 8: Sort the DataFrame based on Total Points
points_df_sorted = points_df.sort_values(by=('Total Points','tot'), ascending=False)

points_df_sorted = points_df_sorted.reset_index()
points_df_sorted.index = range(1,len(points_df_sorted)+1)
points_df_sorted = points_df_sorted.rename(columns={'':'Name'}).rename(columns={'index':''})
points_df_sorted.columns.names = ['','Number']

st.dataframe(points_df_sorted, use_container_width=True)
