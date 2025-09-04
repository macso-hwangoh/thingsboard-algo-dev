import os
import sys
import yaml
from datetime import datetime
import time
import pandas as pd

from src.utils.generate_cough_count_csv import generate_cough_count_csv
from src.utils.plot_data import plot_data

# Retrieve project and home directory paths (required when running script without docker-compose)
file_path = os.path.realpath(__file__)
project_dir_path = file_path[
    :file_path.find("thingsboard-algo-dev") + len("thingsboard-algo-dev")
]

if __name__ == "__main__":
    # Load and prepare args and config
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path_args_yaml = os.path.join(current_directory, 'args.yaml')
    with open(file_path_args_yaml, encoding="utf-8") as f:
        args = yaml.safe_load(f)
    with open(args["file_path_config"], 'r') as file:
        config = yaml.safe_load(file)
    start_date_day = config['start_date_day']
    start_date_month = config['start_date_month']
    start_date_year = config['start_date_year']
    start_date_hour = config['start_date_hour']
    start_date_minute = config['start_date_hour']
    end_date_day = config['end_date_day']
    end_date_month = config['end_date_month']
    end_date_year = config['end_date_year']
    end_date_hour = config['end_date_hour']
    end_date_minute = config['end_date_hour']
    device_to_plot = config['device_to_plot']

    # Configuration - adjust this to change how many days back to look
    history_in_days = 30
    print(f"Retrieving cough data...")

    # Calculate time range
    start_date = datetime(start_date_year, start_date_month, start_date_day, start_date_hour, start_date_minute)
    end_date = datetime(end_date_year, end_date_month, end_date_day, end_date_hour, end_date_minute)
    start_date_timestamp = int(start_date.timestamp() * 1000)
    end_date_timestamp = int(end_date.timestamp() * 1000)

    # Get data and create CSVs
    all_device_data = generate_cough_count_csv(start_date_timestamp, end_date_timestamp)
    print(type(all_device_data))

    # Compute data for specific device

    # Plot hourly data for specific device
    # data_device = get_device_plot_data(device_number, device_dfs)
    # data_device_hourly = get_hourly_plot_data_for_device(device_dfs[1])


    os.makedirs("figures", exist_ok=True)
    plot_data(device_to_plot)
