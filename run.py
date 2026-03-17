import os
import logging

from src.data_fetcher import read_station_config, validate_config, fetch_earthquake_events, generate_station_data_json
from src.plot_generator import process_stations
from src.html_generator import generate_html, copy_static_files
from src.utils import setup_logging

BASE_URL = "http://127.0.0.1:18081"
EVENT_SERVICE_URL = "http://service.iris.edu/fdsnws/event/1/query"
CONFIG_FILE = "config.ini"
OUTPUT_DIR = "helicorder_plots"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    setup_logging()

    stations = read_station_config(CONFIG_FILE)
    validate_config(stations)
    events = fetch_earthquake_events(EVENT_SERVICE_URL)

    plots = process_stations(BASE_URL, stations, OUTPUT_DIR, events)

    if plots:
        generate_html(plots, OUTPUT_DIR)
        copy_static_files(OUTPUT_DIR)
        generate_station_data_json(BASE_URL, stations, OUTPUT_DIR)
        logging.info(f"Successfully created {len(plots)} out of {len(stations)} possible plots.")
    else:
        logging.error("No plots were generated. Check your data source and configuration.")


if __name__ == "__main__":
    main()
