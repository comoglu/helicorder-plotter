import os
import logging
import shutil
from jinja2 import Environment, FileSystemLoader

def copy_static_files(output_dir):
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    output_static_dir = os.path.join(output_dir, 'static')
    if os.path.exists(static_dir):
        shutil.copytree(static_dir, output_static_dir, dirs_exist_ok=True)
    logging.info(f"Copied static files to {output_static_dir}")

def copy_map_view_html(output_dir):
    map_view_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Helicorder Stations Map</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.css" />
        <style>
            body, html {
                height: 100%;
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }
            .container {
                display: flex;
                flex-direction: column;
                height: 100%;
            }
            header {
                background-color: #f8f9fa;
                padding: 1rem;
                text-align: center;
            }
            #map {
                flex-grow: 1;
            }
            footer {
                background-color: #f8f9fa;
                padding: 1rem;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Helicorder Stations Map</h1>
            </header>
            <div id="map"></div>
            <footer>
                <p><a href="index.html">Back to All Stations</a></p>
            </footer>
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const map = L.map('map').setView([0, 0], 2);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }).addTo(map);

                fetch('station_data.json')
                    .then(response => response.json())
                    .then(stations => {
                        stations.forEach(station => {
                            const marker = L.marker([station.latitude, station.longitude]).addTo(map);
                            const popupContent = `
                                <strong>${station.id}</strong><br>
                                Network: ${station.network}<br>
                                Station: ${station.station}<br>
                                <a href="${station.network}.${station.station}.${station.location}.${station.channel}.html" target="_blank">View Helicorder</a>
                            `;
                            marker.bindPopup(popupContent);
                        });
                        
                        if (stations.length > 0) {
                            const bounds = L.latLngBounds(stations.map(s => [s.latitude, s.longitude]));
                            map.fitBounds(bounds);
                        }
                    })
                    .catch(error => {
                        console.error('Error loading station data:', error);
                        alert('Failed to load station data. Please try refreshing the page.');
                    });
            });
        </script>
    </body>
    </html>
    '''
    with open(os.path.join(output_dir, 'map_view.html'), 'w') as f:
        f.write(map_view_html)
    logging.info(f"Generated map_view.html in {output_dir}")

def generate_html(plots, output_dir):
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates')))
    
    # Generate index.html (formerly all_stations.html)
    index_template = env.get_template('all_stations.html')
    index_content = index_template.render(plots=plots)
    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w') as f:
        f.write(index_content)
    logging.info(f"Generated index.html at {index_path}")

    # Generate individual station pages
    station_template = env.get_template('station.html')
    for plot in plots:
        station_filename = f"{plot['id']}.html"
        station_path = os.path.join(output_dir, station_filename)
        station_content = station_template.render(plot=plot)
        with open(station_path, 'w') as f:
            f.write(station_content)
        logging.info(f"Generated station page for {plot['id']} at {station_path}")

    logging.info(f"Generated HTML files in {output_dir}")
