import obspy
from obspy import UTCDateTime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import os
import logging
import traceback
from .data_fetcher import get_waveforms

def create_helicorder(st, output_file, thumbnail_file, starttime, endtime, events):
    try:
        fig = plt.figure(figsize=(10, 7))  # Adjust size as needed
        
        st.plot(type="dayplot", interval=60, right_vertical_labels=False,
                vertical_scaling_range=5e3, one_tick_per_line=True,
                color=['k', 'r', 'b', 'g'], show_y_UTC_label=True,
                events=events, number_of_ticks=5, tick_format='%H:%M',
                vertical_plotting_method='mean', data_unit='mm/s',
                linewidth=0.5, x_labels_size=8, y_labels_size=8, fig=fig)

        ax = fig.gca()
        for event in events:
            if starttime <= event['time'] <= endtime:
                x_pos = (event['time'] - starttime) / (endtime - starttime)
                y_pos = 1 - (event['time'].hour + event['time'].minute / 60) / 24
                ax.annotate(f"{event['description'][:20]}, M{event['magnitude']:.1f}",
                            xy=(x_pos, y_pos), xytext=(5, 5), textcoords='offset points',
                            fontsize=7, color='blue', alpha=0.7,
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7))

        title = (f"{st[0].stats.network}.{st[0].stats.station}.{st[0].stats.location}.{st[0].stats.channel}\n"
                 f"UTC: {starttime.strftime('%Y-%m-%d %H:%M:%S')} to {endtime.strftime('%Y-%m-%d %H:%M:%S')}")
        fig.suptitle(title, fontsize=10, y=1.02)
        fig.savefig(output_file, dpi=300, bbox_inches='tight')
        
        # Create thumbnail
        img = Image.open(output_file)
        img.thumbnail((200, 200))  # Adjust size to match CSS
        img.save(thumbnail_file)
        
        plt.close(fig)
        return True
    except Exception as e:
        logging.error(f"Error creating helicorder plot for {output_file}: {str(e)}")
        logging.error(traceback.format_exc())
        return False

def process_station(base_url, station_info, output_dir, starttime, endtime, events):
    network = station_info['network']
    station = station_info['station']
    location = station_info['location']
    channel = station_info['stream']
    
    st = get_waveforms(base_url, network, station, location, channel, starttime, endtime)
    if st is not None and len(st) > 0:
        output_file = os.path.join(output_dir, f"{network}.{station}.{location}.{channel}.png")
        thumbnail_file = os.path.join(output_dir, f"{network}.{station}.{location}.{channel}_thumb.png")
        if create_helicorder(st, output_file, thumbnail_file, starttime, endtime, events):
            return {
                'id': f"{network}.{station}.{location}.{channel}",
                'network': network,
                'station': station,
                'location': location if location else "--",
                'channel': channel,
                'filename': os.path.basename(output_file),
                'thumbnail': os.path.basename(thumbnail_file),
                'starttime': starttime.isoformat(),
                'endtime': endtime.isoformat()
            }
    return None

def process_stations(base_url, stations, output_dir, events):
    now = UTCDateTime.now()
    endtime = now
    starttime = endtime.replace(minute=0, second=0, microsecond=0) - 24 * 3600

    plots = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_station = {executor.submit(process_station, base_url, station_info, output_dir, starttime, endtime, events): station_id
                             for station_id, station_info in stations.items()}
        for future in as_completed(future_to_station):
            station_id = future_to_station[future]
            try:
                result = future.result()
                if result:
                    plots.append(result)
                    logging.info(f"Successfully processed {station_id}")
                else:
                    logging.warning(f"Failed to process {station_id}")
            except Exception as e:
                logging.error(f"Error processing {station_id}: {str(e)}")
                logging.error(traceback.format_exc())
    
    return plots
