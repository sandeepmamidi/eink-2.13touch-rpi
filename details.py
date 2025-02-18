#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
import socket
import logging
import psutil  # For memory and disk usage
from PIL import Image, ImageDraw, ImageFont

# Paths for fonts and libraries
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from TP_lib import epd2in13_V4

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Function to get the IP address
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return "No IP"

# Function to get CPU temperature
def get_cpu_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000.0
            return f"{temp:.1f}°C"
    except Exception as e:
        return "N/A"

# Function to get memory usage
def get_memory_usage():
    try:
        mem = psutil.virtual_memory()
        return f"{mem.percent}%"
    except Exception as e:
        return "N/A"

# Function to get disk usage
def get_disk_usage():
    try:
        disk = psutil.disk_usage('/')
        return f"{disk.percent}%"
    except Exception as e:
        return "N/A"

# Initialize the display
epd = epd2in13_V4.EPD()
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)

# Load fonts
font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

# Create a blank image
image = Image.new("1", (epd.height, epd.width), 255)
draw = ImageDraw.Draw(image)

# Main loop
try:
    while True:
        # Clear the image
        draw.rectangle((0, 0, epd.height, epd.width), fill=255)

        # Get system metrics
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        ip_address = get_ip_address()
        cpu_temp = get_cpu_temperature()
        mem_usage = get_memory_usage()
        disk_usage = get_disk_usage()

        # Draw the metrics on the display
        draw.text((10, 10), f"Time: {current_time}", font=font15, fill=0)
        draw.text((10, 30), f"IP: {ip_address}", font=font15, fill=0)
        draw.text((10, 50), f"CPU Temp: {cpu_temp}", font=font15, fill=0)
        draw.text((10, 70), f"Mem Usage: {mem_usage}", font=font15, fill=0)
        draw.text((10, 90), f"Disk Usage: {disk_usage}", font=font15, fill=0)

        # Display the image
        epd.displayPartial(epd.getbuffer(image))

        # Wait for 1 second before updating
        time.sleep(1)

except KeyboardInterrupt:
    logging.info("Exiting...")
    epd.sleep()
    epd.Dev_exit()