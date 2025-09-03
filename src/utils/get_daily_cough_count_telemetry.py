import requests
import datetime

# Function to get the telemetry data for a device
def get_daily_cough_count_telemetry(auth_token, device_id, start_ts, end_ts, limit=10000, is_barn=False):
    if is_barn:
        device_telemetry_url = f"https://thingsboard.cloud:443/api/plugins/telemetry/ASSET/{device_id}/values/timeseries"
    else:
        device_telemetry_url = f"https://thingsboard.cloud:443/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
    params = {
        'keys': 'totalCoughCount' if is_barn else 'dailyCoughCount',
        'startTs': start_ts,
        'endTs': end_ts,
        'limit': limit
    }
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = requests.get(device_telemetry_url, headers=headers, params=params)
    response_data = response.json()
    telemetry = response_data.get('totalCoughCount', []) if is_barn else response_data.get('dailyCoughCount', [])
    return telemetry