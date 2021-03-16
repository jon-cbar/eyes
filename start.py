import logging
import os
import uuid
from modules import network
from modules import operatingsystem
from modules import streaming
from modules import webserver
from modules import templating


# Constant definitions.
SERVER_PORT = 80
PUBLIC_DIRECTORY = "public"
TEMPLATE_FILE = "template.html"
MEDIA_DIRECTORY = "media"
NETWORK_DEPTH_MASK = 27
RTSP_PORT = 554
TIMEOUT = 1.0
CAMERA_ID_SIZE = 8
LOGGING_LEVEL = logging.INFO

# Since user and password are sensitives data,
# they must be set as OS environment variables.
# On Ubuntu, it is possible add in /etc/environment file, for example.
CAMERA_USER = os.getenv("IP_CAMERA_USER")
CAMERA_PASSWORD = os.getenv("IP_CAMERA_PASSWORD")

# Log configuration.
logFormat = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(format=logFormat, level=LOGGING_LEVEL)
logging.info("Starting API...")

# Clean media directory.
mediaPath = PUBLIC_DIRECTORY + "/" + MEDIA_DIRECTORY
logging.info("Cleaning the directory %s.", mediaPath)
operatingsystem.emptyDirectory(mediaPath)
logging.info("Directory emptied.")

# Look for IP cameras running in the network.
logging.info("Looking for IP cameras using RTSP...")
cameras = network.findHostsInNetwork(NETWORK_DEPTH_MASK, RTSP_PORT, TIMEOUT)
logging.info("%i cameras found.", len(cameras))

# Create workers to start an HTTP Web Server and HLS Streaming Cameras.
workers = []
template = templating.Template(PUBLIC_DIRECTORY + "/" + TEMPLATE_FILE)

# HLS Streaming Cameras.
if len(cameras) > 0:
    cameraIDs = []
    logging.info("Creating an HLS streaming for each camera.")
    for camera in cameras:
        # Create a random ID to this camera.
        cameraID = str(uuid.uuid4())[:CAMERA_ID_SIZE]
        cameraIDs.append(cameraID)
        logging.debug("Camera ID: %s.", cameraID)

        # Update HTML template with camera data.
        template.html += "\n<div id=\"c" + cameraID + "\"></div>"
        template.script += "\nvar c" + cameraID + \
            " = new Clappr.Player({ source: \"/" + MEDIA_DIRECTORY + "/" + \
            cameraID + "/playlist.m3u8\", parentId: \"c" + cameraID + "\" });"

        rtspUrl = streaming.createRtspUrl(
            camera, CAMERA_USER, CAMERA_PASSWORD)
        streamPath = mediaPath + "/" + cameraID
        workerArgs = (rtspUrl, streamPath)
        worker = operatingsystem.Worker(
            streaming.startHlsStreaming, workerArgs)
        workers.append(worker)

template.createFile(PUBLIC_DIRECTORY + "/index.html")

# HTTP Web Server.
logging.info("Creating an HTTP Web Server on port %i.", SERVER_PORT)
hostName = network.getLocalIpAddress()
workerArgs = (hostName, SERVER_PORT, PUBLIC_DIRECTORY)
worker = operatingsystem.Worker(webserver.startServer, workerArgs)
workers.append(worker)

htmlContent = ""

# Start OS workers.
logging.info(
    "Starting OS subprocesses from the %i created workers.", len(workers))
operatingsystem.startWorkers(workers)
