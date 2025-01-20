import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide")

st.title('Prime results : Mandag 19:10 - Stage 4: Flat is Fast - Douce France')

file_path = 'race_results.json'

# Open and load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

primesData = pd.DataFrame()
for primes in data['segmentScores']:
    primesData_ = pd.DataFrame(primes['fal'])
    primesData_['segment'] = primes['name']
    primesData = pd.concat([primesData,primesData_[['name','points','segment']]])
primesData = primesData.set_index(['segment','points']).unstack()

st.dataframe(primesData)


