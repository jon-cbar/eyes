import logging
import os
from modules import ipcamera
from modules import streaming


# Log configuration.
LOG_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)

# Using default values: depthMask=27, port=554, timeout=1.
CAMERAS = ipcamera.findRtspCameras()

# Since these values are sensitives,
# they must be set as OS environment variables.
# On Ubuntu, it is possible add in /etc/environment file, for example.cmd
CAMERA_USER = os.getenv('IP_CAMERA_USER')
CAMERA_PASSWORD = os.getenv('IP_CAMERA_PASSWORD')

for CAMERA_IP in CAMERAS:
    print(streaming.createRtspUrl(CAMERA_IP, CAMERA_USER, CAMERA_PASSWORD))
