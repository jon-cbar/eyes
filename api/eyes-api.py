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

'''
# Find cameras.
mask = '192.168.1.0/27'
port = 554
cameras = findCameras(mask, port)

# Find RTSP urls.
user = 'user'
password = 'password'
for ip in cameras:
    url = createRtspUrl(ip, user, password)
    logging.info(url)
'''
