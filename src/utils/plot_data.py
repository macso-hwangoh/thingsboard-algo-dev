import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz

def plot_data_daily(daily_data, save_path):
    # Load CSV
    df = pd.DataFrame(daily_data)

    # Convert ts (milliseconds) to datetime with Europe/Madrid timezone
    df['ts'] = pd.to_datetime(df['ts'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Europe/Madrid')

    # Plot
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df['ts'], df['value'], color='orchid', linewidth=2)

    # Axis formatting (screenshot style)
    ax.set_ylabel("Coughs in past 24 hours")
    ax.set_xlabel("Date")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d, %Y\n%H:%M", tz=pytz.timezone('Europe/Madrid')))
    plt.xticks(rotation=30)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Plot of daily counts saved")


def plot_data_hourly(hourly_data, save_path):
    # Convert to DataFrame
    df = pd.DataFrame(hourly_data)

    # Convert ms to datetime (Europe/Madrid)
    df['ts'] = pd.to_datetime(df['ts'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Europe/Madrid')

    # Plot
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df['ts'], df['value'], color='orchid', linewidth=2)

    # Axis formatting (hourly ticks)
    ax.set_ylabel("Coughs per hour")
    ax.set_xlabel("Date")
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%b %d, %Y\n%H:%M", tz=pytz.timezone('Europe/Madrid'))
    )
    plt.xticks(rotation=30)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Plot of hourly counts saved")
