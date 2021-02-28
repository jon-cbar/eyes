import logging
from modules import streaming
from modules import os

# Log configuration.
LOG_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)

MEDIA_DIRECTORY = "media"
os.clearDirectory(MEDIA_DIRECTORY)

RTSP_URL = streaming.createRtspUrl('192.168.1.14', 'admin', 'ANJO9876')
streaming.startHlsStreaming(RTSP_URL, MEDIA_DIRECTORY)
