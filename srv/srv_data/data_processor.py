import time
from srv.srv_firebase.firebase_handler import set_firebase_data, get_firebase_data
from srv.srv_json.json_handler import load_json

def process_transit_data(station_data, station_id, current_env_data, bus_lines, scraping_interval_seconds):
    """Process transit data for each station."""
    for transit in station_data.get("data", []):
        if "time" in transit and "realtime" in transit:
            current_line = transit["line"]["name"]
            arrival_in = int(transit["realtime"]) - int(time.time())

            if -60 < arrival_in <= scraping_interval_seconds and current_line in bus_lines:
                delay = int(transit["realtime"]) - int(transit["time"])
                cancelled = bool(transit.get("cancelled", False))
                delay_type = get_delay_type(delay, cancelled)

                ref_path = f"/stations_test/{station_id}/lines/{current_line}"
                env_data = get_firebase_data(ref_path) or initialize_line_data(station_id, current_line)

                # Now call the update function
                update_env_data(env_data, delay, delay_type, current_env_data)
                set_firebase_data(ref_path, env_data)
            elif arrival_in > (scraping_interval_seconds + 300):
                break



def initialize_line_data(station_id, current_line):
    """Initialize line data in Firebase if it doesn't exist."""
    data_by_env = load_json('json_templates/data_by_env.json')
    return data_by_env

def update_env_data(env_data, delay, delay_type, current_env_data):
    """Update environmental data for the station."""
    for factor_type, factor_data_list in current_env_data.items():
        for factor in factor_data_list:
            env_data = set_env_data(env_data, delay, delay_type, factor, factor_type)
    return env_data


def set_env_data(env_data, delay, delay_type, factor, factor_type):
    """Set environmental data for a specific factor."""
    if factor in env_data.get(factor_type, {}):
        if delay > 0:
            env_data[factor_type][factor]["delay_info"][delay_type] = int(env_data[factor_type][factor]["delay_info"][delay_type]) + 1
            delay_total = int(env_data[factor_type][factor]["delay_total"])
            new_delay_total = delay_total + 1
            average_delay = float(env_data[factor_type][factor]["average_delay"])
            new_average_delay = str((average_delay * delay_total + delay) / new_delay_total)
            env_data[factor_type][factor]["delay_total"] = str(new_delay_total)
            env_data[factor_type][factor]["average_delay"] = str(new_average_delay)
        
        delay_score = create_delay_score(env_data[factor_type][factor]["delay_info"], int(env_data[factor_type][factor]["data_size"]) + 1)
        factor_data_size = int(env_data[factor_type][factor]["data_size"]) + 1
        env_data[factor_type][factor]["score"] = delay_score
        env_data[factor_type][factor]["data_size"] = str(factor_data_size)

    return env_data


def get_delay_type(delay, cancelled):
    """Return the delay type based on delay duration."""
    if cancelled:
        return "cancelled"
    if delay == 0:
        return "punctual"
    if delay <= 300:
        return "short"
    if delay <= 900:
        return "medium"
    if delay <= 1800:
        return "long"
    return "extreme"

def create_delay_score(delay_info, data_size):
    """Calculate a delay score."""
    penalty = sum(
        float(delay_info[key]) * weight
        for key, weight in zip(["short", "medium", "long", "extreme", "cancelled"], [0.5, 0.6, 0.7, 0.8, 1.0])
    )
    return round(100 * (1 - penalty / data_size), 2)
