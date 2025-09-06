import time
from datetime import datetime, timedelta

def calculate_moving_average(
        device_data_daily_sum,
        start_timestamp_ms, end_timestamp_ms,
        ma_window_length_hours, ma_window_step_hours
    ):
    """
    Calculates the moving average of cough counts detected by a device within a
    window that is shifted along a time interval. Note that as the window length
    is constant, there is no need to divide by anything since each shift shares
    a common denominator.

    The production AWS Lambda function code can be found at:
    https://github.com/MACSO-AI/thingsboard-preemptive-alarm/

    Argument/s:
        device_data_daily_sum (list): each entry is a dictionary of form
                                      [{'ts': , 'value: }] where 'ts' and
                                      'value' are explained in the function header of
                                      src/data/generate_cough_count_csv.py
        start_timestamp_ms (int): interval start time in milliseconds using Unix Epoch
        end_timestamp_ms (int): interval end time in milliseconds using Unix Epoch
        ma_window_length_hours (int): window length in hours
        ma_window_step_hours (int): window step size in hours

    Returns:
        (list): each entry is a dictionary of the form
                {'ts': , 'value: } where 'ts'
                is incremented every ma_window_step_hours and
                'value' represents the total cough count
                in the last ma_window_length_hours hours
    """

    # Convert to milliseconds
    one_hour_in_milliseconds = 60 * 60 * 1000
    ma_window_length_ms = ma_window_length_hours * one_hour_in_milliseconds
    ma_window_step_ms = ma_window_step_hours * one_hour_in_milliseconds

    # Compute average
    result = []
    ts = start_timestamp_ms
    while ts <= end_timestamp_ms:
        cough_count = 0

        # Calculate the window boundaries
        window_start = ts - ma_window_length_ms
        window_end = ts

        # Count "Cough" occurrences within the window
        for item in device_data_daily_sum:
            item_ts = int(item['ts'])
            if window_start <= item_ts <= window_end:
                cough_count += 1

        result.append({
            'ts': ts,
            'value': cough_count
        })

        # Increment window
        ts += ma_window_step_ms

    return result
