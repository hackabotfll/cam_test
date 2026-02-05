# Camera Website Server Setup

Deploy the camera monitoring website on **cam.hackabot4stem.com**

## 🌐 How It Works

The website fetches video streams through the relay server at **api.hackabot4stem.com**:

```
Camera Pi → Streams to port 5001
     ↓
Relay Server (api.hackabot4stem.com)
     ├── Receives stream registration
     ├── Proxies video at /video_feed/{camera_num}
     └── Provides alarm status via API
     ↓
Website (cam.hackabot4stem.com)
     ├── Fetches video from relay: https://api.hackabot4stem.com/video_feed/1
     ├── Polls for alarms: https://api.hackabot4stem.com/api/commands
     └── Checks status: https://api.hackabot4stem.com/status
```

## 📦 Files

- **camera_website.html** - Main web interface (static HTML)
- **server.py** - Optional Flask server (if not using Apache/Nginx)
- **requirements.txt** - Python dependencies (only if using server.py)

## 🚀 Deployment Options

### Option 1: Static Hosting (Recommended)

Simply upload `camera_website.html` to your web server:

**Apache:**
```bash
sudo cp camera_website.html /var/www/html/index.html
sudo systemctl restart apache2
```

**Nginx:**
```bash
sudo cp camera_website.html /usr/share/nginx/html/index.html
sudo systemctl restart nginx
```

**Any static host:**
- GitHub Pages
- Netlify
- Vercel
- AWS S3 + CloudFront
- Just upload the HTML file!

### Option 2: Flask Server (Development/Testing)

If you want to use the Flask server:

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python server.py
```

The Flask server will serve the HTML and can also host the API endpoints locally (though the relay server is recommended for production).

## ⚙️ Configuration

The website is **pre-configured** to use:
- **Relay API:** `https://api.hackabot4stem.com`
- **Video streams:** Fetched via relay proxy at `/video_feed/{1-4}`

No configuration changes needed unless you want to:
- Change the API URL (edit line 3 in the `<script>` section)
- Customize colors/layout (edit CSS section)

## 🔧 Advanced Configuration

### Custom API URL

If your relay server is at a different location, edit `camera_website.html`:

```javascript
const API_URL = 'https://your-relay-server.com';
```

### Direct Camera Streams (Without Relay Proxy)

If you want to fetch streams directly from cameras instead of through the relay:

```javascript
// Change this line in initializeCameras():
img.src = `${API_URL}/video_feed/${i}`;

// To this (using direct camera IPs):
const cameraStreams = {
    1: 'http://192.168.1.100:5001/video_feed',
    2: 'http://192.168.1.101:5001/video_feed',
    3: 'http://192.168.1.102:5001/video_feed',
    4: 'http://192.168.1.103:5001/video_feed'
};
img.src = cameraStreams[i];
```

**Note:** Direct streaming only works if cameras are on the same network or have public IPs.

## 🎨 Features

### Visual Interface
- ✅ 4-camera grid layout
- ✅ Real-time MJPEG video streams
- ✅ Status indicators (green = online, red = offline)
- ✅ Responsive design

### Alarm System
- ✅ **Visual alarms:** Camera name flashes red
- ✅ **Audio alarms:** Siren sound (800Hz/1000Hz alternating)
- ✅ **Auto-sync:** Polls relay every 500ms for alarm updates
- ✅ **Auto-clear:** Alarms clear when person leaves frame

### Monitoring
- ✅ Camera online/offline status
- ✅ Heartbeat monitoring (updates every 5 seconds)
- ✅ Automatic reconnection attempts

## 🔍 Testing

### 1. Open the Website
```
https://cam.hackabot4stem.com
```

### 2. Check Browser Console
Press F12 and look for:
```
Initializing camera system...
API URL: https://api.hackabot4stem.com
Camera streams: {streams: {...}}
Camera 1 stream loaded successfully
```

### 3. Manual Test Alarms

Open browser console (F12) and type:
```javascript
// Trigger alarm on camera 1
cameraDebug.triggerAlarm(1);

// Clear alarm on camera 1
cameraDebug.clearAlarm(1);

// Clear all alarms
cameraDebug.clearAll();
```

### 4. Verify Video Streams

Each camera should display live video. If you see a red 📹 icon:
- Camera is offline
- Stream URL is incorrect
- Network/firewall issue
- Relay server issue

## 🐛 Troubleshooting

### No Video Streams

**Check relay server:**
```bash
curl https://api.hackabot4stem.com/status
```

Should return JSON with camera info.

**Check specific camera:**
```bash
curl https://api.hackabot4stem.com/video_feed/1
```

Should return video data or error.

**Check browser console:**
- Look for CORS errors
- Look for network errors
- Look for 404/503 errors

### CORS Errors

If you see: `Access-Control-Allow-Origin` errors:

The relay server needs CORS enabled. Check `relay_server.py`:
```python
from flask_cors import CORS
CORS(app)
```

### Alarms Not Triggering

**Test manually in console:**
```javascript
cameraDebug.triggerAlarm(1);
```

If this works but automatic alarms don't:
- Check camera is sending triggers to relay
- Check relay is storing alarm states
- Check website is polling correctly

**Verify relay alarm state:**
```bash
curl https://api.hackabot4stem.com/api/alarm_status
```

### Audio Not Playing

- Click anywhere on page first (browser autoplay policy)
- Check browser sound is not muted
- Check console for audio errors

### Cameras Show Offline (Red)

**Check camera status:**
```bash
curl https://api.hackabot4stem.com/status
```

Look at `cameras` object:
```json
{
  "cameras": {
    "1": {
      "online": true,
      "alarm_active": false,
      "last_seen_seconds_ago": 3.2
    }
  }
}
```

If `online: false`, the camera hasn't sent a heartbeat in 30+ seconds.

## 📊 API Endpoints Used

The website calls these relay server endpoints:

| Endpoint | Method | Purpose | Frequency |
|----------|--------|---------|-----------|
| `/api/commands` | GET | Poll for alarm commands | Every 500ms |
| `/status` | GET | Check camera online status | Every 5s |
| `/api/camera_streams` | GET | Get camera URLs | On load |
| `/video_feed/{num}` | GET | Proxy video stream | Continuous |

## 🔐 SSL/HTTPS Setup

For production, use HTTPS:

**Apache:**
```bash
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d cam.hackabot4stem.com
```

**Nginx:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d cam.hackabot4stem.com
```

## 📈 Performance Tips

### Optimize Video Quality

The cameras stream at ~30 FPS. To reduce bandwidth:

**On Raspberry Pi** (edit `integrated_camera1.py`):
```python
# Reduce frame rate
config = picam2.create_preview_configuration(
    controls={"FrameRate": 15},  # Change from 30 to 15
    buffer_count=12
)
```

### Reduce Polling Frequency

If the server is getting overloaded:

```javascript
// Change from 500ms to 1000ms
setTimeout(pollForCommands, 1000);

// Change from 5s to 10s
setTimeout(checkCameraStatus, 10000);
```

## 🎯 Production Checklist

- [ ] HTTPS/SSL certificate installed
- [ ] Domain configured: cam.hackabot4stem.com
- [ ] Firewall allows HTTPS (port 443)
- [ ] Website loads without errors
- [ ] All 4 cameras show video (or red if offline)
- [ ] Alarms trigger correctly when person detected
- [ ] Audio works (siren plays)
- [ ] Status indicators update (green/red)
- [ ] Browser console shows no errors
- [ ] Tested on multiple browsers
- [ ] Tested on mobile devices
- [ ] CDN/caching configured (optional)
- [ ] Monitoring/analytics added (optional)

## 🔄 Updates

To update the website:
1. Edit `camera_website.html`
2. Upload to web server
3. Clear browser cache or do a hard refresh (Ctrl+F5)

## 📱 Mobile Support

The website is responsive and works on:
- ✅ Desktop browsers (Chrome, Firefox, Safari, Edge)
- ✅ Mobile browsers (iOS Safari, Chrome, Android)
- ✅ Tablets

Audio alarm may require user interaction on mobile (tap screen once).

## 🆘 Support

**Common Issues:**

1. **No video:** Check relay server is running and cameras are registered
2. **CORS errors:** Enable CORS on relay server
3. **No alarms:** Check browser console, verify relay API is accessible
4. **Red cameras:** Camera is offline or not sending heartbeat

**Debug Commands:**
```bash
# Check relay status
curl https://api.hackabot4stem.com/status

# Check alarm states
curl https://api.hackabot4stem.com/api/alarm_status

# Trigger test alarm
curl -X POST https://api.hackabot4stem.com/api/trigger_alarm_1
```

---

**Ready to deploy!** Just upload `camera_website.html` to your web server at cam.hackabot4stem.com
