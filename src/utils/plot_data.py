import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz

def plot_data_daily(daily_data, time_zone, save_path):
    # Convert to DataFrame
    df = pd.DataFrame(daily_data)

   # Convert ts (milliseconds) to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(time_zone)

    # Plot
    fig, ax = plt.subplots(figsize=(12,6))
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
    print(f"Plot of daily counts saved")


def plot_data_hourly(hourly_data, time_zone, save_path):
    # Convert to DataFrame
    df = pd.DataFrame(hourly_data)

    # Convert ms to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(time_zone)

    # Plot
    fig, ax = plt.subplots(figsize=(12,6))
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
    print(f"Plot of hourly counts saved")

def plot_data_moving_average(moving_average_data, time_zone, window_length_hours, window_step_hours, save_path):
    # Convert to DataFrame
    df = pd.DataFrame(moving_average_data)

    # Convert ms to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(time_zone)

    # Plot
    fig, ax = plt.subplots(figsize=(12,6))
    plt.title(f"Moving average. Window length: {window_length_hours} hours. Window step: {window_step_hours} hours.")
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
    print(f"Plot of hourly counts saved")
