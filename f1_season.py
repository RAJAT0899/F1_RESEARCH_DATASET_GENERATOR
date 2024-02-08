import streamlit as st
import requests
import csv
from datetime import datetime

# Function to fetch data from F1 API endpoints
def fetch_f1_data(season):
    driver_data = requests.get(f"https://ergast.com/api/f1/{season}/drivers.json").json()
    team_data = requests.get(f"https://ergast.com/api/f1/{season}/constructors.json").json()
    race_data = requests.get(f"https://ergast.com/api/f1/{season}.json").json()
    # Fetch additional data as needed
    return driver_data, team_data, race_data

# Function to process and aggregate fetched data into a single dataset
def aggregate_f1_data(driver_data, team_data, race_data):
    f1_dataset = []
    
    # Process driver data
    drivers = driver_data["MRData"]["DriverTable"]["Drivers"]
    driver_dict = {driver["driverId"]: driver for driver in drivers}
    
    # Process team data
    teams = team_data["MRData"]["ConstructorTable"]["Constructors"]
    team_dict = {team["constructorId"]: team for team in teams}
    
    # Process race data
    races = race_data["MRData"]["RaceTable"]["Races"]
    st.write(f"Number of Races: {len(races)}")  # Debug statement
    for race in races:
        race_info = {
            "race_name": race["raceName"],
            "circuit": race["Circuit"]["circuitName"],
            "country": race["Circuit"]["Location"]["country"],
            "date": race["date"],
            "season": race["season"]
        }
        # Process race results
        if "Results" in race:
            results = race["Results"]
            st.write(f"Number of Results for {race['raceName']}: {len(results)}")  # Debug statement
            for result in results:
                driver_id = result["Driver"]["driverId"]
                team_id = result["Constructor"]["constructorId"]
                driver_info = driver_dict.get(driver_id, {})
                team_info = team_dict.get(team_id, {})
                result_info = {
                    "driver": f"{driver_info.get('givenName', '')} {driver_info.get('familyName', '')}",
                    "team": team_info.get('name', ''),
                    "nationality": driver_info.get('nationality', ''),
                    "position": result["position"],
                    "points": result["points"]
                }
                f1_dataset.append({**race_info, **result_info})
        else:
            st.write(f"No results available for {race['raceName']}")  # Debug statement
    return f1_dataset

# Function to save F1 data to a CSV file
def save_to_csv(data):
    filename = "f1_dataset.csv"
    with open(filename, mode='w', newline='') as file:
        fieldnames = ["race_name", "circuit", "country", "date", "season", "driver", "team", "nationality", "position", "points"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    st.success(f"Data saved to {filename}")

# Main function to fetch, process, and save F1 data
def main():
    st.title("Formula 1 Dataset Viewer")

    # Get user input for the season
    season = st.number_input("Enter the season (e.g., 2023)", min_value=1950, max_value=datetime.now().year, value=datetime.now().year)

    # Fetch F1 data
    driver_data, team_data, race_data = fetch_f1_data(season)
    f1_season_dataset = aggregate_f1_data(driver_data, team_data, race_data)

    # Display the dataset
    st.header("Formula 1 Dataset")
    st.write(f"Total Records: {len(f1_season_dataset)}")
    st.write(f1_season_dataset)

    # Add a button to save data to CSV
    if st.button("Save Data to CSV"):
        save_to_csv(f1_season_dataset)

if __name__ == "__main__":
    main()
