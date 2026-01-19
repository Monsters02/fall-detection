# Raspberry Pi 4 Installation Guide - Step by Step

This guide will help you set up the fall detection system on your Raspberry Pi 4 from scratch.

## Prerequisites Checklist

Before starting, ensure you have:
- [ ] Raspberry Pi 4 (2GB minimum, 4GB+ recommended)
- [ ] Raspberry Pi Camera Module v2 or v3
- [ ] Micro SD Card (32GB+ Class 10)
- [ ] Power supply (5V 3A minimum)
- [ ] Computer with SD card reader
- [ ] Internet connection (Wi-Fi or Ethernet)
- [ ] Optional: Passive buzzer and resistor

---

## Phase 1: Prepare Raspberry Pi OS

### Step 1.1: Flash OS to SD Card

1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Insert SD card into computer
3. Open Raspberry Pi Imager
4. Choose:
   - Device: Raspberry Pi 4
   - OS: Raspberry Pi OS (64-bit) - Bullseye or Bookworm
   - Storage: Your SD card
5. Click "Write" and wait for completion

### Step 1.2: First Boot Configuration

1. Insert SD card into Raspberry Pi
2. Connect monitor, keyboard, mouse, and power
3. Go through initial setup wizard
4. Set timezone, language, password
5. Connect to Wi-Fi

### Step 1.3: Update System

Open Terminal and run:

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y git python3-pip python3-dev build-essential
```

This may take 5-10 minutes. Don't interrupt!

---

## Phase 2: Enable Camera Interface

### Step 2.1: Enable Camera in raspi-config

```bash
sudo raspi-config
```

Navigate using arrow keys:
1. **Interface Options**
2. **Camera** 
3. **Yes** to enable
4. **Finish**
5. **Yes** to reboot

### Step 2.2: Verify Camera

```bash
# After reboot, test camera
libcamera-hello --list-cameras

# Output should show your camera
```

---

## Phase 3: Create Project Directory

### Step 3.1: Clone Repository

```bash
cd ~
mkdir -p projects
cd projects
git clone <your-repository-url> fall-detection
cd fall-detection
```

Or manually create the files:

```bash
cd ~
mkdir fall-detection
cd fall-detection
# Copy main.py, config.py, utils.py, README.md files here
```

### Step 3.2: Verify Project Files

```bash
ls -la
# You should see:
# main.py, config.py, utils.py, pyproject.toml, README.md
```

---

## Phase 4: Install Python Dependencies

### Step 4.1: Create Virtual Environment (Recommended)

```bash
cd ~/fall-detection

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Verify (should show (venv) in terminal)
```

### Step 4.2: Install Core Dependencies

```bash
# Install OpenCV via apt (faster, smaller)
sudo apt-get install -y python3-opencv

# Install other dependencies
pip install --upgrade pip numpy pillow

# Verify OpenCV
python3 -c "import cv2; print(f'✓ OpenCV {cv2.__version__} installed')"
```

### Step 4.3: Install YOLOv8

```bash
# Install ultralytics (YOLOv8)
echo "⏳ Installing YOLOv8..."
pip install ultralytics

# Verify YOLOv8
python3 -c "from ultralytics import YOLO; print('✓ YOLOv8 installed')"
```

### Step 4.4: Install Pi Camera Support

```bash
# Install picamera2 (already included in latest Pi OS)
pip install --upgrade picamera2

# Verify
python3 -c "from picamera2 import Picamera2; print('✓ Picamera2 installed')"
```

### Step 4.5: Install GPIO Support (Optional, for buzzer)

```bash
pip install RPi.GPIO

# Verify
python3 -c "import RPi.GPIO; print('✓ RPi.GPIO installed')"
```

---

## Phase 5: Download YOLOv8 Model

```bash
# Pre-download model (400MB, takes 2-5 minutes)
python3 -c "from ultralytics import YOLO; model = YOLO('yolov8n-pose.pt'); print('✓ Model downloaded')"

# Verify download
ls -lh yolov8n-pose.pt
```

---

## Phase 6: Test Camera

### Step 6.1: Test with libcamera

```bash
# 5-second camera test
libcamera-hello --timeout 5000
```

A preview window should appear briefly.

### Step 6.2: Test with Python

```bash
python3 << 'EOF'
from picamera2 import Picamera2
import time

print("Testing camera...")
camera = Picamera2()
camera.start()
print("✓ Camera started")
time.sleep(2)
camera.close()
print("✓ Camera closed - TEST PASSED")
EOF
```

---

## Phase 7: Configure GPIO Buzzer (Optional)

### Step 7.1: Hardware Setup

Connect buzzer to GPIO pin 17:

```
        Raspberry Pi GPIO Header
            
        3V3  [●●] 5V
     GPIO2  [●●] 5V
     GPIO3  [●●] GND
     GPIO4  [●●] GPIO14
        GND  [●●] GPIO15
    GPIO17  [●●] GPIO18  ← Use GPIO17
    GPIO27  [●●] GPIO22
        GND  [●●] GPIO23
    GPIO10  [●●] GPIO11
        GND  [●●] GPIO9
     GPIO5  [●●] GPIO8
        GND  [●●] GPIO7
```

Wiring:
```
GPIO 17 ──[100Ω Resistor]──┬──(+) Buzzer
                           │
                      GND ──┴──(-) Buzzer
```

### Step 7.2: Test Buzzer

```bash
python3 << 'EOF'
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

print("Testing buzzer...")
for i in range(3):
    GPIO.output(17, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(17, GPIO.LOW)
    time.sleep(0.1)
    print(f"Buzz {i+1}/3")

GPIO.cleanup()
print("✓ Buzzer test complete")
EOF
```

You should hear 3 short buzzes.

---

## Phase 8: First Run

### Step 8.1: Test with Display

```bash
# Activate virtual environment if not already
source ~/fall-detection/venv/bin/activate

# Run with camera preview
cd ~/fall-detection
python3 main.py
```

Expected output:
```
==================================================
Fall Detection System - Raspberry Pi Edition
==================================================
✓ GPIO alerts enabled (if --gpio used)
✓ Headless mode (no display) (if --headless used)

Initializing Fall Detection System...
Loading YOLOv8 model...
Attempting to use Raspberry Pi Camera...
✓ Pi Camera initialized successfully

Starting video processing...
Fall Detection Started. Press 'q' to quit.
```

A window should appear showing your camera feed.

### Step 8.2: Test Fall Detection

1. Keep the application running
2. Lie down in front of the camera
3. Look for red box with "FALL DETECTED" message
4. Press 'q' to exit

### Step 8.3: Test with GPIO Buzzer

```bash
source ~/fall-detection/venv/bin/activate
cd ~/fall-detection
python3 main.py --gpio
```

When you fall in front of the camera:
- Red box appears with "FALL DETECTED"
- Buzzer sounds 3 times
- Console shows: "⚠️ FALL DETECTED!"

---

## Phase 9: Production Setup

### Step 9.1: Headless Mode (For 24/7 Monitoring)

```bash
# Test headless mode (no display needed)
source ~/fall-detection/venv/bin/activate
cd ~/fall-detection
python3 main.py --headless --gpio
```

### Step 9.2: Create Startup Script

```bash
# Create startup script
cat > ~/fall-detection/start.sh << 'EOF'
#!/bin/bash
cd ~/fall-detection
source venv/bin/activate
python3 main.py --headless --gpio
EOF

chmod +x ~/fall-detection/start.sh
```

### Step 9.3: Auto-start on Boot (Systemd)

```bash
# Create service file
sudo tee /etc/systemd/system/fall-detection.service > /dev/null << 'EOF'
[Unit]
Description=Fall Detection Service
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/home/pi/fall-detection/venv/bin/python3 /home/pi/fall-detection/main.py --headless --gpio
WorkingDirectory=/home/pi/fall-detection
StandardOutput=journal
StandardError=journal
Restart=always
User=pi
Environment="PATH=/home/pi/fall-detection/venv/bin"

[Install]
WantedBy=multi-user.target
EOF

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable fall-detection.service
sudo systemctl start fall-detection.service

# Check status
sudo systemctl status fall-detection.service

# View logs
sudo journalctl -u fall-detection.service -f
```

---

## Phase 10: Verify Everything Works

### Checklist

```bash
# 1. Virtual environment active?
echo $VIRTUAL_ENV  # Should show path to venv

# 2. Camera working?
libcamera-hello --timeout 2000

# 3. YOLOv8 model downloaded?
ls -lh yolov8n-pose.pt

# 4. Service running? (if enabled)
sudo systemctl status fall-detection.service

# 5. Buzzer working? (optional)
python3 -c "import RPi.GPIO as GPIO; import time; GPIO.setmode(GPIO.BCM); GPIO.setup(17, GPIO.OUT); GPIO.output(17, GPIO.HIGH); time.sleep(0.5); GPIO.output(17, GPIO.LOW); GPIO.cleanup()"
```

---

## Troubleshooting

### Problem: Camera Not Detected

```bash
# Solution 1: Check connection
vcgencmd get_camera
# Should show: supported=1 detected=1

# Solution 2: Enable camera interface
sudo raspi-config
# Interface Options → Camera → Yes → Reboot

# Solution 3: Check if other app is using camera
lsof /dev/video* 2>/dev/null || echo "Camera available"
```

### Problem: High CPU/Memory Usage

```bash
# Solution 1: Run headless
python3 main.py --headless

# Solution 2: Check for other processes
top -bn1 | head -20
ps aux | grep python

# Solution 3: Restart service
sudo systemctl restart fall-detection.service
```

### Problem: Buzzer Not Working

```bash
# Solution 1: Test GPIO directly
gpio readall  # Install gpio: sudo apt-get install gpiod

# Solution 2: Check wiring (GPIO17, GND, 100Ω resistor)
# Solution 3: Test with different GPIO pin (update config)
```

### Problem: Frame Rate Too Slow

```bash
# Running normally? Expected ~15 FPS headless
# Solution 1: Use smaller model (yolov8n-pose)
# Solution 2: Run headless (no display overhead)
# Solution 3: Add heatsink to Raspberry Pi (cooling)
```

---

## Performance Monitoring

```bash
# Monitor in real-time
watch -n 1 "free -h && echo '---' && ps aux | grep python3"

# Log temperature
vcgencmd measure_temp

# Expected:
# - Memory: ~450MB
# - CPU: 80-95%
# - Temp: 45-65°C (normal operation)
```

---

## Next Steps

1. **Test the system thoroughly** with different fall scenarios
2. **Adjust sensitivity** if needed (edit `_is_person_fallen()` in main.py)
3. **Add email/SMS alerts** (extend `trigger_alert()`)
4. **Deploy 24/7** using systemd service
5. **Monitor logs** regularly for issues

---

## Support Resources

- **Camera Issues**: https://www.raspberrypi.com/documentation/accessories/camera.html
- **GPIO Guide**: https://www.raspberrypi.com/documentation/computers/raspberry-pi.html
- **YOLOv8 Docs**: https://docs.ultralytics.com/
- **OpenCV Docs**: https://docs.opencv.org/

---

**Installation complete! Your fall detection system is ready to monitor. 🎉**
