import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz

def plot_data(device_to_plot):
    # Load CSV
    df = pd.read_csv(f"device_data/Virbac-ai-{device_to_plot}_cough_telemetry.csv")

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
    plt.savefig(f"figures/{device_to_plot}", dpi=300)
    print(f"Plot saved")
