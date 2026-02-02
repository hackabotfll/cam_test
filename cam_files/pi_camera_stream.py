#!/usr/bin/env python3
"""
Raspberry Pi Camera Streaming Server using picamera2
Run this on your Raspberry Pi to stream camera feed
"""

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from flask import Flask, Response, stream_with_context
import io
import threading

app = Flask(__name__)

# Global variables
output_frame = None
lock = threading.Lock()
picam2 = None

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

def initialize_camera():
    global picam2
    picam2 = Picamera2()
    
    # Configure camera for streaming
    config = picam2.create_video_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
    picam2.configure(config)
    
    # Start camera
    picam2.start()
    print("Camera initialized and started")

def generate_frames():
    """Generate frames from camera"""
    global picam2
    
    while True:
        # Capture frame
        frame = picam2.capture_array()
        
        # Convert to JPEG
        import cv2
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        # Yield frame in multipart format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/status')
def status():
    """Camera status endpoint"""
    return {'status': 'running', 'camera': 'active'}

if __name__ == '__main__':
    initialize_camera()
    
    # Run Flask server
    # Access via http://PI_IP_ADDRESS:5001/video_feed
    app.run(host='0.0.0.0', port=5001, threaded=True)
