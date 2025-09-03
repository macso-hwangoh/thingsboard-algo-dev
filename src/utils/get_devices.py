import requests

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