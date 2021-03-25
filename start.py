import logging
import os
import uuid
from modules import network
from modules import operatingsystem
from modules import streaming
from modules import webserver
from modules import templating


SERVER_PORT = 80
PUBLIC_DIRECTORY = "public"
TEMPLATE_FILE = "template.html"
MEDIA_DIRECTORY = "media"
NETWORK_DEPTH_MASK = 27
RTSP_PORT = 554
TIMEOUT = 1.0
CAMERA_ID_SIZE = 8
LOGGING_LEVEL = logging.INFO

CAMERA_USER = os.getenv("IP_CAMERA_USER")
CAMERA_PASSWORD = os.getenv("IP_CAMERA_PASSWORD")

logFormat = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(format=logFormat, level=LOGGING_LEVEL)
logging.info("Starting API...")

mediaPath = PUBLIC_DIRECTORY + "/" + MEDIA_DIRECTORY
logging.info("Cleaning the directory %s.", mediaPath)
operatingsystem.emptyDirectory(mediaPath)
logging.info("Directory emptied.")

logging.info("Looking for IP cameras using RTSP...")
cameras = network.findHostsInNetwork(NETWORK_DEPTH_MASK, RTSP_PORT, TIMEOUT)
logging.info("%i cameras found.", len(cameras))

templateFilePath = PUBLIC_DIRECTORY + "/" + TEMPLATE_FILE
template = templating.Template(templateFilePath=templateFilePath,
                               mediaDirectory=MEDIA_DIRECTORY)

workers = []

if len(cameras) > 0:
    cameraIDs = []
    logging.info("Creating an HLS streaming for each camera.")
    for camera in cameras:
        cameraID = str(uuid.uuid4())[:CAMERA_ID_SIZE]
        cameraIDs.append(cameraID)
        logging.debug("Camera ID: %s.", cameraID)

        template.includeCamera(cameraID)

        rtspUrl = streaming.createRtspUrl(
            camera, CAMERA_USER, CAMERA_PASSWORD)
        streamPath = mediaPath + "/" + cameraID
        workerArgs = (rtspUrl, streamPath)
        worker = operatingsystem.Worker(
            streaming.startHlsStreaming, workerArgs)
        workers.append(worker)

template.createFile(PUBLIC_DIRECTORY + "/index.html")

hostName = network.getLocalIpAddress()
logging.info("Creating an HTTP Web Server on http://%s:%i/",
             hostName, SERVER_PORT)
workerArgs = (hostName, SERVER_PORT, PUBLIC_DIRECTORY)
worker = operatingsystem.Worker(webserver.startServer, workerArgs)
workers.append(worker)

htmlContent = ""

logging.info(
    "Starting OS subprocesses from the %i created workers.", len(workers))
operatingsystem.startWorkers(workers)
