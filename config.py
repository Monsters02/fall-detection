"""
Configuration file for Fall Detection System
"""

# Model Configuration
MODEL_NAME = "yolov8n-pose.pt"  # Options: yolov8n-pose, yolov8s-pose, yolov8m-pose
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for detections

# Fall Detection Configuration
FALL_THRESHOLD = 0.5  # Sensitivity threshold for fall detection
ALERT_COOLDOWN = 2  # Seconds between alerts

# Video Configuration
VIDEO_SOURCE = 0  # 0 for webcam, or path to video file
OUTPUT_PATH = None  # Set to save output video, e.g., "output.mp4"

# Display Configuration
SHOW_KEYPOINTS = True  # Show body keypoints
SHOW_BOXES = True  # Show detection boxes
DISPLAY_STATS = True  # Show statistics overlay

# Alert Configuration
ENABLE_SOUND_ALERT = False  # Enable audio alert
ENABLE_EMAIL_ALERT = False  # Enable email notification
ENABLE_SMS_ALERT = False  # Enable SMS notification

# Email Configuration (if enabled)
EMAIL_RECIPIENT = "emergency@example.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# SMS Configuration (if enabled)
SMS_RECIPIENT = "+1234567890"
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
