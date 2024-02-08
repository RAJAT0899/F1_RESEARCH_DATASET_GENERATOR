import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Function to fetch race results data from the F1 API
def fetch_race_results(year):
    url = f"https://ergast.com/api/f1/{year}/results.json"
    all_results = []

    # Fetch data for each page until no more data is available
    page_num = 1
    while True:
        response = requests.get(url, params={'limit': 100, 'offset': (page_num - 1) * 100})
        if response.status_code == 200:
            page_data = response.json()['MRData']['RaceTable']['Races']
            if not page_data:
                break  # No more data available
            all_results.extend(page_data)
            page_num += 1
        else:
            return None
    
    return all_results

# Streamlit app
def main():
    st.title("F1 Research Dataset Generator")

    # Year selection
    year = st.number_input("Enter the year:", min_value=1950, max_value=2022, value=2021, step=1)

    # Button to trigger data download
    if st.button("Download Dataset"):
        race_results = fetch_race_results(year)
        
        if race_results:
            data = []
            for race in race_results:
                race_name = race['raceName']
                round_num = race['round']
                # Convert date to standard format
                date = datetime.strptime(race['date'], "%Y-%m-%d").strftime("%Y-%m-%d")
                circuit = race['Circuit']['circuitName']
                for result in race['Results']:
                    driver_info = result['Driver']
                    constructor_info = result['Constructor']
                    position = result['position']
                    points = result['points']
                    data.append({
                        'Race Name': race_name,
                        'Round': round_num,
                        'Date': date,
                        'Circuit': circuit,
                        'Driver Name': driver_info['givenName'] + ' ' + driver_info['familyName'],
                        'Driver Nationality': driver_info['nationality'],
                        'Constructor': constructor_info['name'],
                        'Position': position,
                        'Points': points
                    })
            df = pd.DataFrame(data)
            # Save data to CSV
            df.to_csv(f"f1_dataset_{year}.csv", index=False)
            
            st.success(f"Dataset downloaded successfully for {year}")
        else:
            st.error("Failed to download dataset. Please try again.")

if __name__ == "__main__":
    main()
