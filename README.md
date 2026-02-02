# Camera Alarm System

A real-time camera monitoring system with alarm capabilities, designed to work with Raspberry Pi cameras using picamera2.

## Features

- 4 camera feeds displayed in a grid layout
- Real-time MJPEG streaming from Raspberry Pi cameras
- Visual alarms (flashing red camera names)
- Audio alarms (siren sound)
- REST API for triggering/clearing alarms
- Responsive web interface

## Setup

### Main Server Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python server.py
```

3. Open your browser to `http://localhost:5000`

### Raspberry Pi Camera Setup

See [PI_SETUP.md](PI_SETUP.md) for detailed instructions on setting up Raspberry Pi cameras.

Quick steps:
1. Install picamera2 and dependencies on each Pi
2. Run `python3 pi_camera_stream.py` on each Pi
3. Update camera stream URLs in `camera_website.html` with your Pi IP addresses

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

Using PowerShell:
```powershell
# Use curl.exe to avoid PowerShell alias
curl.exe -X POST http://localhost:5000/api/trigger_alarm_1
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

## Camera Stream Configuration

Update the camera stream URLs in `camera_website.html`:

```javascript
const cameraStreams = {
    1: 'http://192.168.1.100:5001/video_feed',  // Pi 1 IP
    2: 'http://192.168.1.101:5001/video_feed',  // Pi 2 IP
    3: 'http://192.168.1.102:5001/video_feed',  // Pi 3 IP
    4: 'http://192.168.1.103:5001/video_feed'   // Pi 4 IP
};
```

## How It Works

1. **Camera Streaming**: Each Raspberry Pi runs `pi_camera_stream.py` which streams MJPEG video on port 5001
2. **Web Interface**: The HTML page displays all 4 camera streams
3. **Alarm System**: When you send a POST request to trigger an alarm, the server stores the command
4. **Polling**: The webpage polls the server every 500ms for new commands
5. **Visual/Audio Feedback**: When an alarm is triggered, the camera name flashes red and a siren sound plays

## File Structure

```
cam_test/
├── camera_website.html    # Web interface
├── server.py             # Main Flask server (alarm API)
├── pi_camera_stream.py   # Raspberry Pi camera streamer
├── requirements.txt      # Python dependencies (main server)
├── pi_requirements.txt   # Python dependencies (Raspberry Pi)
├── PI_SETUP.md          # Detailed Pi setup instructions
└── README.md            # This file
```

