import os
import sys
import yaml
from datetime import datetime
import time
import pandas as pd

from src.utils.get_thingsboard_auth_token import get_thingsboard_auth_token
from src.utils.get_devices import get_devices
from src.utils.get_daily_cough_count_telemetry import get_daily_cough_count_telemetry

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

    # Configuration - adjust this to change how many days back to look
    history_in_days = 30

    print(f"Retrieving cough data for the last {history_in_days} days...")

    # Get thingsboard auth token for all future requests
    thingsboard_auth_token = get_thingsboard_auth_token()

    # Get all thingsboard devices
    devices = get_devices(thingsboard_auth_token)

    # Calculate time range
    start_date = datetime(start_date_year, start_date_month, start_date_day, start_date_hour, start_date_minute)
    end_date = datetime(end_date_year, end_date_month, end_date_day, end_date_hour, end_date_minute)
    start_date_timestamp = int(start_date.timestamp() * 1000)
    end_date_timestamp = int(end_date.timestamp() * 1000)

    # Dictionary to store all device data
    all_device_data = {}

    print(f"Found {len(devices)} devices. Processing...")

    for i, device in enumerate(devices):
        device_name = device["name"]
        device_id = device["id"]["id"]

        # Filter for only Virbac devices
        if "Virbac" not in device_name:
            continue

        print(f"Processing device {i+1}/{len(devices)}: {device_name}")

        try:
            # Get cough telemetry data
            cough_telemetry = get_daily_cough_count_telemetry(
                thingsboard_auth_token,
                device_id,
                start_date_timestamp,
                end_date_timestamp
            )
            all_device_data[device_name] = cough_telemetry

            print(f"  Retrieved {len(cough_telemetry)} data points")

            # Optionally save individual device data to CSV
            if cough_telemetry:
                os.makedirs("device_data", exist_ok=True)

                with open(f"device_data/{device_name}_cough_telemetry.csv", "w") as f:
                    f.write("ts,value\n")
                    for val in cough_telemetry:
                        f.write(f"{val['ts']},{val['value']}\n")

        except Exception as e:
            print(f"  Error retrieving data for {device_name}: {e}")
            all_device_data[device_name] = []

    print("\nData collection complete!")

    # Filter out devices with no data
    devices_with_data = {k: v for k, v in all_device_data.items() if v}

    print(f"Devices with data: {len(devices_with_data)}")
