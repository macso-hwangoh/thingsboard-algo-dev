import plotly.graph_objs as go
from datetime import datetime, timedelta

def calculate_derivative(data, threshold, threshold_barn, interval_hours=3):
    new_data = []

    for trace in data.copy():
        print(trace)
        total_threshold_triggers = 0
        y_diff = []  # We'll calculate differences for all points
        y_values = list(trace['y'])
        x_values = list(trace['x'])
        interval = timedelta(hours=interval_hours)

        # Ensure that x_values are datetime objects
        if isinstance(x_values[0], str):
            x_values = [datetime.fromisoformat(x) for x in x_values]
        elif not isinstance(x_values[0], datetime):
            raise TypeError("x_values must be in datetime format or ISO string format.")

        # Lists for special markers
        special_x = []
        special_y = []

        # Calculate the derivative using the value from interval_hours earlier
        for i in range(len(y_values)):
            # Look for the point that is interval_hours before the current one
            target_time = x_values[i] - interval
            previous_value = None

            # Find the value at target_time, if it exists
            for j in range(i):
                if x_values[j] <= target_time:
                    previous_value = y_values[j]

            deriv_val = 0

            # If we found a previous value, calculate the difference
            if previous_value is not None:
                deriv_val = y_values[i] - previous_value

            y_diff.append(deriv_val)

            threshold_val = threshold
            if "barn_a" in trace["name"] or "barn_b" in trace["name"]:
                threshold_val = threshold_barn

            if deriv_val >= threshold_val:
                total_threshold_triggers += 1
                # Save this point for the special marker trace
                special_x.append(x_values[i])
                special_y.append(deriv_val)

        derivative_trace = go.Scatter(
            x=[x.isoformat() for x in x_values],
            y=y_diff,
            mode='lines+markers',
            name=f"{trace['name']} (Derivative)"
        )

        special_marker_trace = go.Scatter(
            x=[x.isoformat() for x in special_x],
            y=special_y,
            mode='markers',
            marker=dict(color='red', size=10, symbol='star'),
            name=f"{trace['name']} (Threshold Exceeded)"
        )

        new_data.append(derivative_trace)
        new_data.append(special_marker_trace)

        print("Threshold for " + trace["name"] + ": " + str(total_threshold_triggers))

    return new_data
