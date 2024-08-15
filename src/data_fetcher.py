import requests
import configparser
import logging
import requests
from obspy import UTCDateTime
import obspy
import json
import os
import io

def read_station_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return {section: {
        'network': section.split('.')[0],
        'station': section.split('.')[1],
        'stream': config[section]['detecstream'],
        'location': config[section]['deteclocid']
    } for section in config.sections()}

def fetch_earthquake_events(starttime=None, endtime=None, min_magnitude=5.5):
    if starttime is None:
        starttime = UTCDateTime.now() - 24 * 3600  # 24 hours ago
    if endtime is None:
        endtime = UTCDateTime.now()

    base_url = "http://service.iris.edu/fdsnws/event/1/query"
    params = {
        "starttime": starttime.strftime("%Y-%m-%dT%H:%M:%S"),
        "endtime": endtime.strftime("%Y-%m-%dT%H:%M:%S"),
        "minmagnitude": min_magnitude,
        "format": "text"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return [{
            "time": UTCDateTime(parts[1]),
            "latitude": float(parts[2]),
            "longitude": float(parts[3]),
            "depth": float(parts[4]),
            "magnitude": float(parts[10]),
            "description": parts[12].strip()
        } for parts in (line.split('|') for line in response.text.split('\n')[1:] if line.strip())]
    except requests.RequestException as e:
        logging.error(f"Error fetching earthquake events: {str(e)}")
        return []

def fetch_station_info(base_url, network, station):
    query_url = f"{base_url}/fdsnws/station/1/query?network={network}&station={station}&level=station&format=text"
    try:
        response = requests.get(query_url)
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split('|')
                return {
                    'latitude': float(parts[2]),
                    'longitude': float(parts[3]),
                    'elevation': float(parts[4])
                }
        return None
    except Exception as e:
        logging.error(f"Error fetching station info for {network}.{station}: {str(e)}")
        return None

def generate_station_data_json(base_url, stations, output_dir):
    station_data = []
    for station_id, station_info in stations.items():
        network = station_info['network']
        station = station_info['station']
        location = station_info['location']
        channel = station_info['stream']
        location_info = fetch_station_info(base_url, network, station)
        if location_info:
            station_data.append({
                'id': station_id,
                'network': network,
                'station': station,
                'location': location,
                'channel': channel,
                'latitude': location_info['latitude'],
                'longitude': location_info['longitude'],
                'elevation': location_info['elevation']
            })
    
    with open(os.path.join(output_dir, 'station_data.json'), 'w') as f:
        json.dump(station_data, f)

def get_waveforms(base_url, network, station, location, channel, starttime, endtime):
    query_url = (f"{base_url}/fdsnws/dataselect/1/query"
                 f"?network={network}&station={station}&location={location}&channel={channel}"
                 f"&starttime={starttime.strftime('%Y-%m-%dT%H:%M:%S')}"
                 f"&endtime={endtime.strftime('%Y-%m-%dT%H:%M:%S')}")
    try:
        response = requests.get(query_url)
        if response.status_code == 200:
            return obspy.read(io.BytesIO(response.content))
        elif response.status_code == 204:
            logging.info(f"No data available for {network}.{station}.{location}.{channel}")
        else:
            logging.error(f"Error fetching waveforms. Status code: {response.status_code}")
        return None
    except Exception as e:
        logging.error(f"Error fetching waveforms for {network}.{station}.{location}.{channel}: {str(e)}")
        return None
