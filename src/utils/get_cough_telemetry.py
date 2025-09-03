import requests
import datetime

# Function to get the telemetry data for a device
def get_cough_telemetry(auth_token, device_id, start_ts, end_ts, limit=10000):
    device_telemetry_url = f"https://thingsboard.cloud:443/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
    params = {
        'keys': 'coughDetection',
        'startTs': start_ts,
        'endTs': end_ts,
        'limit': limit
    }
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = requests.get(device_telemetry_url, headers=headers, params=params)
    response_data = response.json()
    telemetry = response_data.get('coughDetection', [])
    return telemetry