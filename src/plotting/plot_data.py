import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz

def plot_detections_daily_count(device_detections_daily_count, time_zone, save_path):
    # Convert to DataFrame
    df = pd.DataFrame(device_detections_daily_count)

   # Convert ts (milliseconds) to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(time_zone)

    # Plot
    fig, ax = plt.subplots(figsize=(12,6))
    plt.title(f"Daily cough counts at time of detection")
    ax.plot(df['ts'], df['value'], color='orchid', linewidth=2)

    # Axis formatting
    ax.set_ylabel("Coughs in past 24 hours")
    ax.set_xlabel("Date")
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%b %d, %Y\n%H:%M", tz=pytz.timezone(time_zone))
    )
    plt.xticks(rotation=30)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Plot of daily counts at time of detection saved")

def plot_time_series_hourly(device_time_series_hourly, time_zone, save_path):
    # Convert to DataFrame
    df = pd.DataFrame(device_time_series_hourly)

    # Convert ms to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(time_zone)

    # Plot
    fig, ax = plt.subplots(figsize=(12,6))
    plt.title(f"Time series of cough counts per hour")
    ax.plot(df['ts'], df['value'], color='orchid', linewidth=2)

    # Axis formatting
    ax.set_ylabel("Coughs per hour")
    ax.set_xlabel("Date")
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%b %d, %Y\n%H:%M", tz=pytz.timezone(time_zone))
    )
    plt.xticks(rotation=30)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Plot of time series of hourly counts saved")

def plot_detections_moving_average(device_detections_moving_average, time_zone, window_length_hours, window_step_hours, save_path):
    # Convert to DataFrame
    df = pd.DataFrame(device_detections_moving_average)

    # Convert ms to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(time_zone)

    # Plot
    fig, ax = plt.subplots(figsize=(12,6))
    plt.title(f"Moving average at time of detection.\n Window length: {window_length_hours} hours. Window step: {window_step_hours} hours.")
    ax.plot(df['ts'], df['value'], color='orchid', linewidth=2)

    # Axis formatting
    ax.set_ylabel(f"Moving average of cough counts")
    ax.set_xlabel("Date")
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%b %d, %Y\n%H:%M", tz=pytz.timezone(time_zone))
    )
    plt.xticks(rotation=30)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Plot of moving averages at time of detection saved")

def plot_detections_derivatives(
        device_detections_derivatives,
        time_zone,
        drv_window_length_hours,
        ma_window_length_hours, ma_window_step_hours,
        save_path):
    # Convert to DataFrame
    df = pd.DataFrame(device_detections_derivatives)

    # Convert ms to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(time_zone)

    # Plot
    fig, ax = plt.subplots(figsize=(12,6))
    plt.title(f"Derivatives at time of detection.\n Window length: {drv_window_length_hours} hours.\n Moving average. Window length: {ma_window_length_hours} hours.  Window step: {ma_window_step_hours} hours.")
    ax.plot(df['ts'], df['value'], color='orchid', linewidth=2)

    # Axis formatting
    ax.set_ylabel(f"Derivatives of cough counts")
    ax.set_xlabel("Date")
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%b %d, %Y\n%H:%M", tz=pytz.timezone(time_zone))
    )
    plt.xticks(rotation=30)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Plot of derivatives at time of detection saved")
