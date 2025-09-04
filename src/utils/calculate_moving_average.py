import time
from datetime import datetime, timedelta

def calculate_moving_average(
        data,
        start_timestamp_ms, end_timestamp_ms,
        window_length_hours, window_step_hours
    ):

    # Convert to milliseconds
    one_hour_in_milliseconds = 60 * 60 * 1000
    window_length_ms = window_length_hours * one_hour_in_milliseconds
    window_step_ms = window_step_hours * one_hour_in_milliseconds

    # Compute average
    result = []
    ts = start_timestamp_ms
    while ts <= end_timestamp_ms:
        cough_count = 0

        # Calculate the window boundaries
        window_start = ts - window_length_ms
        window_end = ts

        # Count "Cough" occurrences within the window
        for item in data:
            item_ts = int(item['ts'])
            if window_start <= item_ts <= window_end:
                cough_count += 1

        result.append({
            'ts': ts,
            'value': cough_count
        })

        # Increment window
        ts += window_step_ms

    return result
