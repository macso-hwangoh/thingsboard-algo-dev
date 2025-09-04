# thingsboard-algo-dev

## Installation:

Create a Python virtual environment and install the requirements using:
```
pip install -r requirements.txt
```

## Setup:
1. Copy the `config/template_config.yaml` file using:
```
cp config/template_config.yaml config/config.yaml
```
2. Copy the `template_args.yaml` file using:
```
cp template_args.yaml args.yaml
```
3. Modify the arguments in `args.yaml` to specify the absolute path to your
   `config/config.yaml` file

4. Update your ThingsBoard username and password in:
   ```
   src/utils/get_thingsboard_auth_token.py
   ```

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

## Output Files
- **`device_data/{device_name}_cough_telemetry.csv`**: Raw telemetry data for each device
- Format: `ts,value` (timestamp in milliseconds, cough count)
