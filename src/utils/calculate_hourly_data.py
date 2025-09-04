import time
from datetime import datetime, timedelta

def calculate_hourly(data, to_timestamp, history_in_days=80):
    one_hour_in_seconds = 60 * 60
    one_day_in_seconds = 24 * one_hour_in_seconds
    current_time = datetime.now()
    start_time = current_time - timedelta(days=history_in_days)
    result = []

    # Dictionary to hold cumulative counts for each hour
    hourly_counts = {}

    # Round each timestamp in data to the nearest hour and accumulate counts
    for item in data:
        item_ts = int(item['ts']) / 1000  # Convert milliseconds to seconds
        item_dt = datetime.fromtimestamp(item_ts)

        if start_time <= item_dt <= to_timestamp:  # Ensure the timestamp is within the desired range
            rounded_dt = item_dt.replace(minute=0, second=0, microsecond=0)

            if rounded_dt not in hourly_counts:
                hourly_counts[rounded_dt] = 0
            hourly_counts[rounded_dt] += 1

            # Print the rounded datetime and accumulated count for debugging
            print(f"Rounded datetime: {rounded_dt}, Count: {hourly_counts[rounded_dt]}")

    # Iterate over each hour in the given range and fill in missing hours with a count of 0
    current_hour = start_time.replace(minute=0, second=0, microsecond=0)
    while current_hour <= to_timestamp:
        result.append({
            'ts': int(current_hour.timestamp() * 1000),  # Convert back to milliseconds
            'value': hourly_counts.get(current_hour, 0)  # Use the accumulated count or 0 if missing
        })

        # Print out the final result entry for debugging
        print(f"Result Timestamp (ms): {int(current_hour.timestamp() * 1000)}, Value: {hourly_counts.get(current_hour, 0)}")

        current_hour += timedelta(hours=1)

    return result
