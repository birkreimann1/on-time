import os
import json

def load_station_data(file_path):
    """Test"""
    with open(file_path, 'r', encoding="utf-8") as file:
        return json.load(file)

def reformat_station_data(station_data):
    reformatted_station_data = {}
    for station_name, station in station_data.items():
        station_id = station["id"]
        data = {
            "name": station_name,
            "lines": station["lines"],
            "coords": station["coords"]
        }
        reformatted_station_data[station_id] = data
    return reformatted_station_data

def save_reformatted_data(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

def main():
    input_file_path = os.path.join("station_data", "station.json")
    output_file_path = os.path.join("station_data", "station_ids.json")

    try:
        station_data = load_station_data(input_file_path)
        reformatted_station_data = reformat_station_data(station_data)
        save_reformatted_data(output_file_path, reformatted_station_data)
        print(f"Reformatted station data has been saved to {output_file_path}.")
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
