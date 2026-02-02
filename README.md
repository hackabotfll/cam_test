# Camera Alarm System

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python server.py
```

3. Open your browser to `http://localhost:5000`

## API Endpoints

All endpoints accept POST requests:

### Trigger Alarms
- `POST /api/trigger_alarm_1` - Trigger alarm on Camera 1
- `POST /api/trigger_alarm_2` - Trigger alarm on Camera 2
- `POST /api/trigger_alarm_3` - Trigger alarm on Camera 3
- `POST /api/trigger_alarm_4` - Trigger alarm on Camera 4

### Clear Alarms
- `POST /api/clear_alarm_1` - Clear alarm on Camera 1
- `POST /api/clear_alarm_2` - Clear alarm on Camera 2
- `POST /api/clear_alarm_3` - Clear alarm on Camera 3
- `POST /api/clear_alarm_4` - Clear alarm on Camera 4

### Clear All Alarms
- `POST /api/clear_all_alarms` - Clear all alarms

## Example Usage

Using curl:
```bash
# Trigger alarm on camera 1
curl -X POST http://localhost:5000/api/trigger_alarm_1

# Clear alarm on camera 1
curl -X POST http://localhost:5000/api/clear_alarm_1

# Clear all alarms
curl -X POST http://localhost:5000/api/clear_all_alarms
```

Using Python:
```python
import requests

# Trigger alarm
requests.post('http://localhost:5000/api/trigger_alarm_1')

# Clear alarm
requests.post('http://localhost:5000/api/clear_alarm_1')

# Clear all alarms
requests.post('http://localhost:5000/api/clear_all_alarms')
```

## How It Works

The webpage polls the server every 500ms for new commands. When you send a POST request to any of the API endpoints, the server stores the command and the webpage picks it up on the next poll, triggering the appropriate alarm action.
