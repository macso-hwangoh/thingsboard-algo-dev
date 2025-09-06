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
        (list): each entry is of form [{'ts': , 'value: }] where 'ts'
                is incremented matching device_data_daily_sum and
                'value' represents the finite difference between
                the last value and first value of the window
    """
    # # Convert to milliseconds
    # one_hour_in_milliseconds = 60 * 60 * 1000
    # drv_window_length_ms = drv_window_length_hours * one_hour_in_milliseconds

    # derivatives = [];
    # for item in device_data_moving_average:
    #     # Find the moving average value at beginning of window
    #     previous_ts
    #     flag_previous_data_point_too_early = True
    #     while flag_previous_data_point_too_early:
    #         if (item['ts'] - previous_ts >= drv_window_length_ms) {
    #             previous = movingAverageData[j];
    #             break;
    #         }

    #         # If we found a valid data point from 3 hours ago, calculate the derivative
    #         if (previous)
    #             const previousValue = Object.values(previous.values)[0];
    #             const currentValue = Object.values(current.values)[0];

    #             const rateOfChange = currentValue - previousValue;
    #             derivatives.push({
    #                 ts: current.ts,
    #                 values: { [`${deviceName}-derivative-${label}`]: rateOfChange },
    #             });

    # return derivatives;
