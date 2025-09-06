import requests
import os

def get_thingsboard_auth_token():
    auth_response = requests.post(
        "https://thingsboard.cloud:443/api/auth/login",
        json={
            "username": "philippe.rivard@macso.ai",
            "password": "ceRh7tTaa@UEjv4"
        }
    )
    auth_token = auth_response.json()['token']\

    return auth_token

def get_devices(auth_token):
    all_devices = []
    page = 0
    page_size = 100

    while True:
        print(f"  Fetching devices page {page + 1}...")

        devices_response = requests.get(
            f"https://thingsboard.cloud:443/api/user/devices?pageSize={page_size}&page={page}&type=Pig%20Cough%20Sensors",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

        if devices_response.status_code != 200:
            print(f"  Error fetching devices page {page + 1}: {devices_response.status_code}")
            break

        response_data = devices_response.json()
        devices_on_page = response_data.get('data', [])

        if not devices_on_page:
            # No more devices on this page, we're done
            break

        all_devices.extend(devices_on_page)
        print(f"  Found {len(devices_on_page)} devices on page {page + 1}")

        # Check if we have more pages to fetch
        # If we got fewer devices than the page size, we're on the last page
        if len(devices_on_page) < page_size:
            break

        # Also check if there's a hasNext field in the response
        if 'hasNext' in response_data and not response_data['hasNext']:
            break

        page += 1

    print(f"  Total devices found: {len(all_devices)}")
    return all_devices

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

def generate_cough_count_csv(start_timestamp_ms, end_timestamp_ms):
    """
    Pulls device telemetry from Thingsboard and saves as .csv file for each
    device. The telemetry is pulled backwards in time from most current to least
    current.

    The generated .csv file has two columns: "ts" and "value":
        ts - represents the time in milliseconds using Unix Epoch;
             that is time since 1st of January 1970 UTC time.

        value - represents the accumulated number of coughs detected within a day.
                The summation is performed whenever a cough is detected by a device in a
                field: therefore "value" will be decremented by one.
                The first value per day equals the number of coughs detected
                that day. Also, the number of rows within a day equals the
                number of coughs detected that day. The "ts"
                associated to "value=0" represents the beginning of each day.

    For example the following snippet of a .csv file represents two days worth
    of cough data where the first day has 7 coughs and the second has 11 coughs.

    ts,value
    1752072703742,7
    1752059457290,6
    1752059031662,5
    1752059015247,4
    1752056288636,3
    1752052139826,2
    1752029304185,1
    1752019210208,0
    1752018381352,11
    1751993041060,10
    1751989834591,9
    1751984302526,8
    1751962409446,7
    1751956188060,6
    1751944783737,5
    1751939229706,4
    1751937546044,3
    1751935876273,2
    1751933367335,1
    1751932810221,0

    Argument/s:
        start_timestamp_ms (int): start time in milliseconds using Unix Epoch
        end_timestamp_ms (int): end time in milliseconds using Unix Epoch
    """

    # Get thingsboard auth token for all future requests
    thingsboard_auth_token = get_thingsboard_auth_token()

    # Get all thingsboard devices
    devices = get_devices(thingsboard_auth_token)

    # Dictionary to store all device data
    all_device_data = {}
    print(f"Found {len(devices)} devices. Processing...")

    for i, device in enumerate(devices):
        device_name = device["name"]
        device_id = device["id"]["id"]
        # Filter for only Virbac devices
        if "Virbac" not in device_name:
            continue
        print(f"Processing device {i+1}/{len(devices)}: {device_name}")
        try:
            # Get cough telemetry data
            cough_telemetry = get_daily_cough_count_telemetry(
                thingsboard_auth_token,
                device_id,
                start_timestamp_ms,
                end_timestamp_ms
            )
            all_device_data[device_name] = cough_telemetry
            print(f"  Retrieved {len(cough_telemetry)} data points")

            # Optionally save individual device data to CSV
            if cough_telemetry:
                os.makedirs("device_data", exist_ok=True)
                with open(f"device_data/{device_name}_cough_telemetry.csv", "w") as f:
                    f.write("ts,value\n")
                    for val in cough_telemetry:
                        f.write(f"{val['ts']},{val['value']}\n")
        except Exception as e:
            print(f"  Error retrieving data for {device_name}: {e}")
            all_device_data[device_name] = []
    print("\nData collection complete!")

    # Filter out devices with no data
    devices_with_data = {k: v for k, v in all_device_data.items() if v}
    print(f"Devices with data: {len(devices_with_data)}")
