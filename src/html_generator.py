import os
import logging
import shutil
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')
STATIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'static')


def copy_static_files(output_dir):
    output_static_dir = os.path.join(output_dir, 'static')
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, output_static_dir, dirs_exist_ok=True)
    logging.info(f"Copied static files to {output_static_dir}")


def generate_html(plots, output_dir):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    # Generate index.html
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

    # Generate map view page
    map_template = env.get_template('map_view.html')
    map_path = os.path.join(output_dir, 'map_view.html')
    with open(map_path, 'w') as f:
        f.write(map_template.render())
    logging.info(f"Generated map_view.html at {map_path}")

    logging.info(f"Generated all HTML files in {output_dir}")
