# Helicorder Plotter

## Description

Helicorder Plotter is a Python-based tool for generating and visualizing helicorder plots from seismic data. It fetches data from seismic stations, creates helicorder plots, and generates an interactive web interface for viewing the plots.

## Features

- Fetch seismic data from multiple stations
- Generate helicorder plots with earthquake event annotations
- Create an interactive web interface for viewing plots
- Display station locations on an interactive map

## Requirements

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/comoglu/helicorder-plotter.git
   cd helicorder-plotter
   ```

2. Create a virtual environment (optional but recommended): (optional)
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages: (If you haven't already)
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Open `config.ini` and add or modify station configurations as needed. Each station should have the following format:
   ```
   [NetworkCode.StationCode]
   detecstream = ChannelCode
   deteclocid = LocationCode
   ```

2. Adjust the base URL in `run.py` if necessary:
   ```python
   base_url = "http://127.0.0.1:8081"  
   ```

## Usage

Run the main script:
```
python run.py
```

This will:
1. Fetch seismic data for the configured stations
2. Generate helicorder plots
3. Create HTML pages for viewing the plots
4. Generate a station map

After running, you can view the results by opening `helicorder_plots/index.html` in a web browser.

## Output

The script generates the following in the `helicorder_plots` directory:
- PNG images of helicorder plots
- Thumbnail images
- HTML pages for each station
- An index page (index.html)
- An all stations page (all_stations.html)
- A map view page (map_view.html)
- JSON file with station data (station_data.json)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

