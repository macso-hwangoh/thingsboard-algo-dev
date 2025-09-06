import os
import sys
import yaml
import pytz
from datetime import datetime
import attridict
import pandas as pd

from src.data.generate_cough_count_csv import generate_cough_count_csv
from src.data.calculate_hourly_data import calculate_hourly_data
from src.moving_average.calculate_moving_average import calculate_moving_average
from src.moving_average.calculate_derivatives import calculate_derivatives
from src.plotting.plot_data import plot_data_daily, plot_data_hourly, plot_data_moving_average

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
    config = attridict(config)

    # Calculate time range
    madrid_tz = pytz.timezone(config.time_zone)
    start_date = madrid_tz.localize(datetime(
        config.start_date_year,
        config.start_date_month,
        config.start_date_day,
        config.start_date_hour,
        config.start_date_minute
    ))
    end_date = madrid_tz.localize(datetime(
        config.end_date_year,
        config.end_date_month,
        config.end_date_day,
        config.end_date_hour,
        config.end_date_minute
    ))
    start_timestamp_ms = int(start_date.timestamp() * 1000)
    end_timestamp_ms = int(end_date.timestamp() * 1000)

    # Get data and create CSVs
    print(f"Retrieving cough data...")
    if config.flag_fetch_data:
        generate_cough_count_csv(start_timestamp_ms, end_timestamp_ms)

    # Compute data for specific device
    device_data_df = pd.read_csv(f"device_data/Virbac-ai-{config.device_to_plot}_cough_telemetry.csv")
    device_data_daily_sum = device_data_df.to_dict(orient="records")
    device_data_hourly = calculate_hourly_data(
            device_data_daily_sum,
            start_timestamp_ms, end_timestamp_ms,
            config.flag_debug_hourly_data
    )
    device_data_moving_average = calculate_moving_average(
            device_data_daily_sum,
            start_timestamp_ms, end_timestamp_ms,
            config.ma_window_length_hours, config.ma_window_step_hours
    )
    device_data_moving_average = calculate_derivatives(
            device_data_moving_average,
            start_timestamp_ms, end_timestamp_ms,
            config.ma_window_length_hours, config.ma_window_step_hours
    )

    # Plot data
    os.makedirs("figures", exist_ok=True)
    plot_data_daily(
            device_data_daily_sum,
            config.time_zone,
            f"figures/fig_{config.device_to_plot}_daily"
    )
    plot_data_hourly(
            device_data_hourly,
            config.time_zone,
            f"figures/fig_{config.device_to_plot}_hourly"
    )
    plot_data_moving_average(
            device_data_moving_average,
            config.time_zone,
            config.window_length_hours, config.window_step_hours,
            f"figures/fig_{config.device_to_plot}_moving_average"
    )
