import os
import logging
import obspy
from src.data_fetcher import read_station_config, fetch_earthquake_events, generate_station_data_json
from src.plot_generator import process_stations
from src.html_generator import generate_html, copy_static_files, copy_map_view_html
from src.utils import setup_logging

def main():
    # Setup
    base_url = "http://127.0.0.1:18081"
    config_file = "config.ini"
    output_dir = "helicorder_plots"
    os.makedirs(output_dir, exist_ok=True)
    setup_logging()

    # Read configuration and fetch data
    stations = read_station_config(config_file)
    events = fetch_earthquake_events()

    # Generate plots
    plots = process_stations(base_url, stations, output_dir, events)

    if plots:
        # Generate HTML and copy static files
        generate_html(plots, output_dir)
        copy_static_files(output_dir)
        
        # Generate station data JSON for the map
        generate_station_data_json(base_url, stations, output_dir)
        
        # Copy map view HTML
        copy_map_view_html(output_dir)
        
        logging.info(f"Successfully created {len(plots)} out of {len(stations)} possible plots.")
    else:
        logging.error("No plots were generated. Check your data source and configuration.")

if __name__ == "__main__":
    main()
