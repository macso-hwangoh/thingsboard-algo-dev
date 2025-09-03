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

    # Configuration - adjust this to change how many days back to look
    history_in_days = 30

    print(f"Retrieving cough data for the last {history_in_days} days...")

    # Get thingsboard auth token for all future requests
    thingsboard_auth_token = get_thingsboard_auth_token()

    # Get all thingsboard devices
    devices = get_devices(thingsboard_auth_token)

    # Calculate time range
    current_timestamp = int(time.time() * 1000)
    one_day_in_milliseconds = 24 * 60 * 60 * 1000
    time_back_in_milliseconds = current_timestamp - history_in_days * one_day_in_milliseconds

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
                time_back_in_milliseconds,
                current_timestamp
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
