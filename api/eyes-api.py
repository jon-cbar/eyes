import ipaddress
import logging
import socket
from camera import Camera


# Log configuration.
LOG_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)

CAMERAS = Camera.findCameras()
USER = 'user'
PASSWORD = 'password'
for CAMERA in CAMERAS:
    print(Camera.createRtspUrl(CAMERA, USER, PASSWORD))
