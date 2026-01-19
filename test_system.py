#!/usr/bin/env python3
"""
Fall Detection System - Diagnostic Test Script
Tests all components and verifies the system is ready to run.
"""

import sys
import os
from pathlib import Path

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def print_header(self):
        print("\n" + "="*60)
        print("Fall Detection System - Diagnostic Tests")
        print("="*60 + "\n")
    
    def print_test(self, name, status, message=""):
        status_str = "✓" if status else "✗"
        color = "\033[92m" if status else "\033[91m"
        reset = "\033[0m"
        
        if status:
            self.passed += 1
        else:
            self.failed += 1
        
        print(f"{color}{status_str}{reset} {name:<40} {message}")
    
    def print_warning(self, name, message=""):
        self.warnings += 1
        print(f"⚠ {name:<40} {message}")
    
    def print_summary(self):
        print("\n" + "="*60)
        print(f"Results: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        print("="*60 + "\n")
        return self.failed == 0


def test_python_version():
    """Test Python version."""
    required = (3, 8)
    current = sys.version_info[:2]
    status = current >= required
    return status, f"Python {current[0]}.{current[1]} (require {required[0]}.{required[1]}+)"


def test_import(module_name, pip_name=None):
    """Test if module can be imported."""
    try:
        __import__(module_name)
        return True, f"✓ {module_name} available"
    except ImportError:
        return False, f"✗ Install with: pip install {pip_name or module_name}"


def test_opencv():
    """Test OpenCV installation."""
    try:
        import cv2
        return True, f"OpenCV {cv2.__version__}"
    except ImportError:
        return False, "Install with: pip install opencv-python"


def test_ultralytics():
    """Test YOLOv8 installation."""
    try:
        from ultralytics import YOLO
        return True, "YOLOv8 available"
    except ImportError:
        return False, "Install with: pip install ultralytics"


def test_numpy():
    """Test NumPy installation."""
    try:
        import numpy as np
        return True, f"NumPy {np.__version__}"
    except ImportError:
        return False, "Install with: pip install numpy"


def test_picamera():
    """Test Pi Camera support."""
    try:
        from picamera2 import Picamera2
        return True, "Picamera2 available"
    except ImportError:
        return False, "Not available (optional, install with: pip install picamera2)"


def test_gpio():
    """Test GPIO support."""
    try:
        import RPi.GPIO
        return True, "RPi.GPIO available"
    except ImportError:
        return False, "Not available (optional, install with: pip install RPi.GPIO)"


def test_model_file():
    """Test if YOLOv8 model is downloaded."""
    model_path = Path("yolov8n-pose.pt")
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        return True, f"Model found ({size_mb:.1f}MB)"
    else:
        return False, "Model not found (will download on first run)"


def test_project_files():
    """Test if all project files exist."""
    required_files = ["main.py", "config.py", "utils.py", "README.md", "pyproject.toml"]
    missing = []
    for f in required_files:
        if not Path(f).exists():
            missing.append(f)
    
    if not missing:
        return True, f"All {len(required_files)} files found"
    else:
        return False, f"Missing: {', '.join(missing)}"


def test_camera_presence():
    """Test if camera device exists (Pi-specific)."""
    import platform
    if "arm" not in platform.machine().lower():
        return None, "Not running on Raspberry Pi (using alternative camera)"
    
    camera_files = ["/dev/video0", "/dev/video1"]
    for cam in camera_files:
        if Path(cam).exists():
            return True, f"Camera device found: {cam}"
    
    return False, "No camera device found"


def test_disk_space():
    """Test available disk space."""
    import shutil
    stat = shutil.disk_usage("/")
    free_gb = stat.free / (1024**3)
    
    if free_gb > 5:
        return True, f"{free_gb:.1f}GB free"
    elif free_gb > 1:
        return None, f"{free_gb:.1f}GB free (recommend 5GB+)"
    else:
        return False, f"{free_gb:.1f}GB free (need at least 1GB)"


def test_memory():
    """Test available memory."""
    try:
        import psutil
        memory = psutil.virtual_memory()
        total_gb = memory.total / (1024**3)
        available_gb = memory.available / (1024**3)
        
        if available_gb > 1:
            return True, f"{available_gb:.1f}GB available ({total_gb:.1f}GB total)"
        else:
            return None, f"{available_gb:.1f}GB available (recommend 2GB+)"
    except ImportError:
        return None, "psutil not available (memory info skipped)"


def test_permissions():
    """Test if we have write permissions."""
    try:
        test_file = ".test_write_permission"
        Path(test_file).write_text("test")
        Path(test_file).unlink()
        return True, "Write permissions OK"
    except PermissionError:
        return False, "No write permissions in current directory"


def test_virtual_env():
    """Test if running in virtual environment."""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        return True, f"Using venv: {sys.prefix}"
    else:
        return None, "Not in virtual environment (recommended)"


def main():
    results = TestResults()
    results.print_header()
    
    print("📋 System Requirements\n")
    
    # Python version
    status, msg = test_python_version()
    results.print_test("Python Version", status, msg)
    
    print("\n📦 Required Dependencies\n")
    
    # OpenCV
    status, msg = test_opencv()
    results.print_test("OpenCV", status, msg)
    
    # NumPy
    status, msg = test_numpy()
    results.print_test("NumPy", status, msg)
    
    # YOLOv8
    status, msg = test_ultralytics()
    results.print_test("YOLOv8 (ultralytics)", status, msg)
    
    print("\n🔧 Optional Dependencies\n")
    
    # Pi Camera
    status, msg = test_picamera()
    if status is None:
        results.print_warning("Pi Camera Support", msg)
    else:
        results.print_test("Pi Camera Support", status, msg)
    
    # GPIO
    status, msg = test_gpio()
    if status is None:
        results.print_warning("GPIO Support", msg)
    else:
        results.print_test("GPIO Support", status, msg)
    
    print("\n📁 Project Files\n")
    
    # Project files
    status, msg = test_project_files()
    results.print_test("Project Files", status, msg)
    
    # Model file
    status, msg = test_model_file()
    if status is None:
        results.print_warning("YOLOv8 Model", msg)
    else:
        results.print_test("YOLOv8 Model", status, msg)
    
    print("\n💻 System Resources\n")
    
    # Permissions
    status, msg = test_permissions()
    results.print_test("Write Permissions", status, msg)
    
    # Disk space
    status, msg = test_disk_space()
    if status is None:
        results.print_warning("Disk Space", msg)
    else:
        results.print_test("Disk Space", status, msg)
    
    # Memory
    status, msg = test_memory()
    if status is None:
        results.print_warning("Memory", msg)
    else:
        results.print_test("Memory", status, msg)
    
    # Virtual environment
    status, msg = test_virtual_env()
    if status is None:
        results.print_warning("Virtual Environment", msg)
    else:
        results.print_test("Virtual Environment", status, msg)
    
    print("\n🎥 Hardware Detection\n")
    
    # Camera
    status, msg = test_camera_presence()
    if status is None:
        results.print_warning("Camera Device", msg)
    else:
        results.print_test("Camera Device", status, msg)
    
    # Print summary
    success = results.print_summary()
    
    # Print recommendations
    if results.failed > 0:
        print("❌ Issues detected - Please fix before running:\n")
        print("1. Install missing dependencies:")
        print("   pip install opencv-python ultralytics numpy pillow picamera2 RPi.GPIO\n")
        print("2. Download YOLOv8 model:")
        print("   python3 -c \"from ultralytics import YOLO; YOLO('yolov8n-pose.pt')\"\n")
        print("3. Enable camera in raspi-config (Raspberry Pi)")
        print("   sudo raspi-config → Interface Options → Camera → Enable\n")
        return 1
    
    if results.warnings > 0:
        print("⚠️  Warnings found - System may have reduced functionality\n")
        print("Recommendations:")
        print("- Install picamera2 for better Pi Camera support")
        print("- Install RPi.GPIO for buzzer alerts")
        print("- Use in virtual environment")
        print("- Ensure 5GB+ free disk space\n")
    
    print("✅ System is ready! You can now run:\n")
    print("   python3 main.py                    # Normal mode")
    print("   python3 main.py --headless --gpio  # Production mode\n")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
