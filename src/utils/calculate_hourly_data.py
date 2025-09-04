from datetime import datetime, timedelta

def calculate_hourly_data(data, start_timestamp_ms, end_timestamp_ms, flag_debug_hourly_data):
    # Convert boundaries to datetimes
    start_time = datetime.fromtimestamp(start_timestamp_ms / 1000.0)
    end_time   = datetime.fromtimestamp(end_timestamp_ms   / 1000.0)

    # Round the range to the top of the hour
    start_hour = start_time.replace(minute=0, second=0, microsecond=0)
    end_hour     = end_time.replace(minute=0, second=0, microsecond=0)

    # Dictionary to hold cumulative counts for each hour
    hourly_counts = {}

    # Round each timestamp in data to the nearest hour and accumulate count
    for item in data:
        item_ts = int(item['ts']) / 1000  # Convert milliseconds to seconds
        item_dt = datetime.fromtimestamp(item_ts)
        if start_time <= item_dt <= end_time: # Ensure the timestamp is within the desired range
            rounded_dt = item_dt.replace(minute=0, second=0, microsecond=0)

            if rounded_dt not in hourly_counts:
                hourly_counts[rounded_dt] = 0
            hourly_counts[rounded_dt] += 1

            # Print the rounded datetime and accumulated count for debugging
            if flag_debug_hourly_data:
                print(f"Rounded datetime: {rounded_dt}, Count: {hourly_counts[rounded_dt]}")

    # Iterate over each hour in the given range and fill in missing hours with a count of 0
    result = []
    while start_hour <= end_hour:
        result.append({
            "ts": int(start_hour.timestamp() * 1000), # Convert back to milliseconds
            "value": hourly_counts.get(start_hour, 0) # Use the accumulated or 0 if missing
        })

        # Print out the final result entry for debugging
        if flag_debug_hourly_data:
            print(f"Result Timestamp (ms): {int(start_hour.timestamp() * 1000)}, Value: {hourly_counts.get(start_hour, 0)}")

        start_hour += timedelta(hours=1)

    return result
