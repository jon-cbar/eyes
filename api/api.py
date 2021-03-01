import logging
import os
from modules import ipcamera
from modules import streaming
from modules import operatingsystem


# Log configuration.
LOG_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)

# Clear 'media' directory.
MEDIA_DIRECTORY = "media"
operatingsystem.clearDirectory(MEDIA_DIRECTORY)

# Look for IP cameras running in the network.
# Use default values: depthMask=27, port=554, timeout=1.
CAMERAS = ipcamera.findRtspCameras()

# Since user and password are sensitives data,
# they must be set as OS environment variables.
# On Ubuntu, it is possible add in /etc/environment file, for example.cmd
CAMERA_USER = os.getenv('IP_CAMERA_USER')
CAMERA_PASSWORD = os.getenv('IP_CAMERA_PASSWORD')

if len(CAMERAS) > 0:
    # Start HLS streaming for each camera found.
    streaming.start(CAMERAS, CAMERA_USER, CAMERA_PASSWORD, MEDIA_DIRECTORY)
