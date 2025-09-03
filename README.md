# ThingsBoard Cough Data Visualization

## Setup

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure ThingsBoard credentials**:

   Update your ThingsBoard username and password in:

   ```
   src/utils/get_thingsboard_auth_token.py
   ```

## Usage

### Run the Main Script

```bash
python run.py
```

This will:

1. Authenticate with ThingsBoard
2. Retrieve all devices (with pagination)
3. Filter for Virbac devices only
4. Fetch cough telemetry data for the last X days
5. Generate interactive plots
6. Save data to CSV files

### Configure Time Range

Edit the `history_in_days` variable in `run.py`:

```python
# Configuration - adjust this to change how many days back to look
history_in_days = 200  # Change this number
```

## Output Files
- **`device_data/{device_name}_cough_telemetry.csv`**: Raw telemetry data for each device
- Format: `ts,value` (timestamp in milliseconds, cough count)
