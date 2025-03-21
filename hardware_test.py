#!/usr/bin/env python

import cv2
import os
import time
import RPi.GPIO as GPIO
from hx711 import HX711
import requests

# GPIO Pins for HX711
DOUT_PIN = 20
PD_SCK_PIN = 21

def check_camera():
    print("\n[TEST] Checking Camera...")
    for port in range(5):  
        camera = cv2.VideoCapture(port)
        if camera.isOpened():
            ret, frame = camera.read()
            if ret:
                print(f"✅ Camera found at port {port}")
                camera.release()
                return
        camera.release()
    print("❌ No camera detected. Check your connections.")

def check_gpio():
    print("\n[TEST] Checking GPIO...")
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        test_pin = 18
        GPIO.setup(test_pin, GPIO.OUT)
        GPIO.output(test_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(test_pin, GPIO.LOW)
        GPIO.cleanup()
        print("✅ GPIO is working fine.")
    except Exception as e:
        print(f"❌ GPIO Error: {e}")

def check_hx711():
    print("\n[TEST] Checking HX711 Weight Sensor...")
    try:
        GPIO.setmode(GPIO.BCM)
        hx = HX711(dout_pin=DOUT_PIN, pd_sck_pin=PD_SCK_PIN)
        err = hx.zero()
        if err:
            raise ValueError("Tare unsuccessful")
        weight = hx.get_weight_mean(5)
        print(f"✅ Weight sensor detected, sample weight: {weight} g")
    except Exception as e:
        print(f"❌ HX711 Error: {e}")

def check_internet():
    print("\n[TEST] Checking Internet Connection...")
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            print("✅ Internet is working.")
        else:
            print("❌ Internet issue. Status Code:", response.status_code)
    except Exception as e:
        print(f"❌ No internet connection: {e}")

if __name__ == "__main__":
    print("=== Running Hardware Diagnostic Test ===")
    check_camera()
    check_gpio()
    check_hx711()
    check_internet()
    print("\n=== Test Completed ===")
