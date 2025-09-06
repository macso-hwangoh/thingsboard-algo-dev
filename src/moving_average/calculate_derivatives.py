from datetime import datetime, timedelta

def calculate_derivatives(device_data_moving_average, drv_window_length_hours):
    """
    Calculates the finite difference of the moving average of cough counts
    in a window of specified length.
    Specifically, it subtracts the values of the end of the window
    from the beginning. Since this function increments along the entries of
    device_data_daily_sum, it inherits the window shift from
    config.ma_window_step_hours. Therefore, this function computes the
    difference of the value at the end of the moving average window
    and some intermediate value within the moving average window specified by
    the argument window_length in this function.

    The production AWS Lambda function code can be found at:
    https://github.com/MACSO-AI/thingsboard-preemptive-alarm/

    Argument/s:
        device_data_moving_average (list): each entry is a dictionary of the form
                                           {'ts': , 'value: } where 'ts' and
                                           'value' are explained in the function header of
                                           src/data/calculate_moving_average.py
        drv_window_length_hours (int): window length in hours

    Returns:
        (list): each entry is a dictionary of form
                [{'ts': , 'value: }] where 'ts'
                is incremented matching device_data_daily_sum and
                'value' represents the finite difference between
                the last value and first value of the window
    """
    # Convert to milliseconds
    one_hour_in_milliseconds = 60 * 60 * 1000
    drv_window_length_ms = drv_window_length_hours * one_hour_in_milliseconds

    derivatives = [];
    for i, item in enumerate(device_data_moving_average[:-1]):
        # Find the moving average value at beginning of window.
        # Note that device_data_moving_average is ordered backwards in time.
        j=i
        previous_ts = device_data_moving_average[j+1]['ts']
        previous_value = device_data_moving_average[j+1]['value']
        while (item['ts'] - previous_ts >= drv_window_length_ms):
            print(item['ts'] - previous_ts)
            j += 1
            previous_ts = device_data_moving_average[j]['ts']
            previous_value = device_data_moving_average[j]['value']

        # calculate the derivative
        finite_difference = item['value'] - previous_value
        derivatives.append({
            'ts': item['ts'],
            'value': finite_difference
        })

    return derivatives
