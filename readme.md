# Helicorder Plotter

Helicorder Plotter is a Python-based tool that fetches seismic waveform data from FDSN web services, generates 24-hour helicorder (dayplot) images with earthquake event annotations, and produces a self-contained static website for browsing the results — including an interactive Leaflet map of all station locations.

## How It Works

```
config.ini          FDSN dataselect         IRIS event service
     │                    │                        │
     ▼                    ▼                        ▼
read_station_config  get_waveforms         fetch_earthquake_events
     │                    │                        │
     │                    ▼                        │
     │              ObsPy Stream ──────────────────┘
     │                    │
     │                    ▼
     │           create_helicorder()
     │            ├─ full-res PNG
     │            └─ thumbnail PNG
     │                    │
     ▼                    ▼
generate_html()    copy_static_files()
     │
     ▼
helicorder_plots/
 ├── index.html
 ├── map_view.html
 ├── station_data.json
 ├── <station>.html  (one per station)
 ├── <station>.png
 ├── <station>_thumb.png
 └── static/
      ├── css/styles.css
      └── js/main.js
```

### Pipeline Steps

1. **Configuration** — Station definitions (network, station, channel, location) are read from `config.ini`.
2. **Earthquake events** — Recent significant earthquakes (M5.5+, last 24 hours) are fetched from the IRIS FDSN event service to annotate the plots.
3. **Waveform retrieval** — For each station, 24 hours of waveform data is requested from a local (or remote) FDSN dataselect service. Requests are parallelised across stations using a process pool.
4. **Plot generation** — Each waveform stream is rendered as a helicorder dayplot via ObsPy, with earthquake events overlaid as annotations. A thumbnail is generated alongside the full-resolution image.
5. **HTML generation** — Jinja2 templates produce an index page with thumbnail grid, individual station detail pages, and an interactive Leaflet map that plots each station's geographic coordinates.

## Requirements

- Python 3.7+
- A running FDSN dataselect web service (e.g. [SeisComP fdsnws](https://www.seiscomp.de/), [ringserver](https://github.com/iris-edu/ringserver), or any FDSN-compliant server)

### Python Dependencies

Listed in `requirements.txt`:

| Package    | Purpose                                    |
|------------|--------------------------------------------|
| ObsPy      | Waveform I/O, dayplot rendering, UTCDateTime |
| matplotlib | Plotting backend (used by ObsPy)           |
| Pillow     | Thumbnail generation                       |
| requests   | HTTP requests to FDSN services             |
| Jinja2     | HTML template rendering                    |

## Installation

```bash
git clone https://github.com/comoglu/helicorder-plotter.git
cd helicorder-plotter

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Configuration

### Station List (`config.ini`)

Each section defines a station to plot. The section name is `Network.Station`:

```ini
[AU.CNB]
detecstream = BHZ
deteclocid = 00

[AU.CTA]
detecstream = BHZ
deteclocid =
```

| Key           | Description                                              |
|---------------|----------------------------------------------------------|
| `detecstream` | SEED channel code (e.g. `BHZ`, `SHZ`, `HHZ`, `EHZ`)    |
| `deteclocid`  | SEED location code (e.g. `00`, `01`, or empty for `--`) |

### Service URLs (`run.py`)

Edit the constants at the top of `run.py` to point at your data sources:

```python
BASE_URL = "http://127.0.0.1:18081"                           # FDSN dataselect + station service
EVENT_SERVICE_URL = "http://service.iris.edu/fdsnws/event/1/query"  # Earthquake event service
```

`BASE_URL` should point to a server that exposes both `/fdsnws/dataselect/1/query` and `/fdsnws/station/1/query` endpoints.

## Usage

```bash
python run.py
```

The script will:

1. Validate the station configuration
2. Fetch M5.5+ earthquake events from the last 24 hours
3. Download waveforms for each configured station (in parallel)
4. Generate helicorder dayplots with event annotations
5. Build a static HTML site in the `helicorder_plots/` directory

Open `helicorder_plots/index.html` in a browser to view the results.

### Output Structure

```
helicorder_plots/
├── index.html                 # Thumbnail grid of all stations
├── map_view.html              # Interactive Leaflet map
├── station_data.json          # Station coordinates for the map
├── AU.CNB.00.BHZ.html         # Individual station detail page
├── AU.CNB.00.BHZ.png          # Full-resolution helicorder plot
├── AU.CNB.00.BHZ_thumb.png    # Thumbnail
├── static/
│   ├── css/styles.css
│   └── js/main.js
└── ...
```

### Logs

Log files are written to `logs/` with timestamps (e.g. `logs/helicorder_plotter_20260318_120000.log`). Both file and console logging are enabled.

## Project Structure

```
helicorder-plotter/
├── run.py                  # Entry point and configuration constants
├── config.ini              # Station definitions
├── requirements.txt        # Python dependencies
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py     # Config parsing, FDSN requests, station info
│   ├── plot_generator.py   # Helicorder plot creation, parallel processing
│   ├── html_generator.py   # Jinja2 HTML generation, static file copying
│   └── utils.py            # Logging setup, timing decorator
├── templates/
│   ├── all_stations.html   # Index page template
│   ├── station.html        # Individual station page template
│   └── map_view.html       # Leaflet map template
└── static/
    ├── css/styles.css      # Shared stylesheet
    └── js/main.js          # Map initialisation script
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
