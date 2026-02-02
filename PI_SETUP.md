# Raspberry Pi Camera Setup Guide

## Setup on Each Raspberry Pi

### 1. Install Dependencies
```bash
sudo apt update
sudo apt install -y python3-pip python3-picamera2 python3-opencv
pip3 install -r pi_requirements.txt
```

### 2. Enable Camera
```bash
sudo raspi-config
# Navigate to: Interface Options -> Camera -> Enable
# Reboot if prompted
```

### 3. Run the Camera Stream Server
```bash
python3 pi_camera_stream.py
```

The camera will start streaming on port 5001.

### 4. Find Your Raspberry Pi IP Address
```bash
hostname -I
```

## Configure the Web Interface

Edit `camera_website.html` and update the camera stream URLs with your Raspberry Pi IP addresses:

```javascript
const cameraStreams = {
    1: 'http://192.168.1.100:5001/video_feed',  // Replace with Pi 1 IP
    2: 'http://192.168.1.101:5001/video_feed',  // Replace with Pi 2 IP
    3: 'http://192.168.1.102:5001/video_feed',  // Replace with Pi 3 IP
    4: 'http://192.168.1.103:5001/video_feed'   // Replace with Pi 4 IP
};
```

## Testing

### Test Single Camera Stream
Open browser and navigate to:
```
http://RASPBERRY_PI_IP:5001/video_feed
```

You should see the live camera feed.

### Test Status Endpoint
```bash
curl http://RASPBERRY_PI_IP:5001/status
```

## Running Both Servers

### On Raspberry Pi (for each camera):
```bash
python3 pi_camera_stream.py
```

### On Main Server (your computer):
```bash
python server.py
```

Then open browser to `http://localhost:5000`

## Network Configuration

Make sure:
1. All Raspberry Pis are on the same network as your main server
2. Firewall allows port 5001 on Raspberry Pis
3. You can ping each Raspberry Pi from your main server

## Troubleshooting

**Camera not detected:**
```bash
libcamera-hello
```

**Port already in use:**
```bash
sudo lsof -i :5001
# Kill process if needed
sudo kill -9 <PID>
```

**Permission denied:**
```bash
sudo usermod -a -G video $USER
# Logout and login again
```

## Running as Service (Optional)

Create a systemd service to auto-start camera streaming:

```bash
sudo nano /etc/systemd/system/picamera-stream.service
```

Add:
```ini
[Unit]
Description=Pi Camera Streaming Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/pi_camera_stream.py
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable picamera-stream.service
sudo systemctl start picamera-stream.service
sudo systemctl status picamera-stream.service
```
