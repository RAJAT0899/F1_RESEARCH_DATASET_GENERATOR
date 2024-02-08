import streamlit as st
import requests
import csv
from datetime import datetime

# Function to fetch F1 data from the API
def fetch_f1_data():
    endpoint = "https://ergast.com/api/f1/drivers.json"
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()["MRData"]["DriverTable"]["Drivers"]
    else:
        st.error("Error: Unable to retrieve data from the API.")
        return []

# Function to infer schema from the fetched F1 data
def infer_schema(data):
    schema = {}
    sample_record = data[0] if data else {}
    for key, value in sample_record.items():
        if isinstance(value, str):
            schema[key] = "string"
        elif isinstance(value, int):
            schema[key] = "integer"
        elif isinstance(value, float):
            schema[key] = "float"
        else:
            schema[key] = "string"  # Fallback if data type is unknown
    return schema

# Function to convert fetched F1 data to the inferred schema
def convert_to_schema(data, schema):
    converted_data = []
    for record in data:
        converted_record = {}
        for key in schema.keys():
            converted_record[key] = record.get(key, "")
        converted_data.append(converted_record)
    return converted_data

# Function to save F1 data to a CSV file
def save_to_csv(data):
    filename = "f1_dataset.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    st.success(f"Data saved to {filename}")

# Main Streamlit app
def main():
    st.title("F1 Dataset Viewer")

    # Fetch F1 data
    f1_data = fetch_f1_data()

    # Infer schema from fetched F1 data
    f1_schema = infer_schema(f1_data)

    # Convert fetched F1 data to the inferred schema
    converted_data = convert_to_schema(f1_data, f1_schema)

    # Display F1 data
    st.header("F1 Dataset")
    st.write(converted_data)

    # Add a button to save data to CSV
    if st.button("Save Data to CSV"):
        save_to_csv(converted_data)

if __name__ == "__main__":
    main()
