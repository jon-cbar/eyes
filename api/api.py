import logging
import os
from modules import ipcamera
from modules import streaming
from modules import operatingsystem
from modules import server


# Log configuration.
LOG_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)

logging.info("Starting API...")

# Clear 'media' directory.
MEDIA_DIRECTORY = "media"
logging.info("Clearing the directory %s.", MEDIA_DIRECTORY)
operatingsystem.clearDirectory(MEDIA_DIRECTORY)
logging.info("Directory emptied.")

# Look for IP cameras running in the network.
# Use default values: depthMask=27, port=554, timeout=1.
logging.info("Looking for IP cameras...")
CAMERAS = ipcamera.findRtspCameras()
logging.info("%i cameras found.", len(CAMERAS))

if len(CAMERAS) > 0:

    # Since user and password are sensitives data,
    # they must be set as OS environment variables.
    # On Ubuntu, it is possible add in /etc/environment file, for example.
    CAMERA_USER = os.getenv('IP_CAMERA_USER')
    CAMERA_PASSWORD = os.getenv('IP_CAMERA_PASSWORD')

    # Create workers to start an HTTP Server and HTS Streaming cameras.
    workers = []

    HOST_NAME = ""
    HOST_PORT = 80
    HTTP_SERVER_FUNCTION = server.start
    HTTP_SERVER_FUNCTION_ARGS = (HOST_NAME, HOST_PORT)
    logging.info("Creating an HTTP Server worker on port %i.", HOST_PORT)
    worker = operatingsystem.Worker(
        HTTP_SERVER_FUNCTION, HTTP_SERVER_FUNCTION_ARGS)
    workers.append(worker)

    logging.info(
        "Creating an HLS streaming worker for each camera.")
    HLS_STREAMING_FUNCTION = streaming.startHlsStreaming
    for camera in CAMERAS:
        rtspUrl = streaming.createRtspUrl(camera, CAMERA_USER, CAMERA_PASSWORD)
        hls_streaming_function_args = (rtspUrl, MEDIA_DIRECTORY)
        worker = operatingsystem.Worker(
            HLS_STREAMING_FUNCTION, hls_streaming_function_args)
        workers.append(worker)

    # Start workers.
    logging.info(
        "Starting OS subprocesses from the %i created workers.", len(workers))
    operatingsystem.startWorkers(workers)
