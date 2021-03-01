""" Use this module to work with video streaming. """

import logging
from modules import operatingsystem


def createRtspUrl(ip: str, user: str, password: str) -> str:
    # This function creates URL to connect with RTSP.
    logging.info("Creating a RTSP URL.")
    URL_FORMAT = "rtsp://{user}:{password}@{ip}/live/mpeg4"
    URL = URL_FORMAT.format(user=user, password=password, ip=ip)
    logging.debug("RTSP URL: %s.", URL)
    return URL


def createHlsCommand(rtspUrl: str, directory: str) -> list:
    # This function is a wrapper that converts
    # Real-Time Streaming Protocol (RTSP) to
    # HTTP Live Streaming (HLS) using an FFMPEG command.
    # It returns an array: the first element is the name of the
    # command to be executed; any following elements are command-line options.
    logging.info("Creating an HLS streaming with FFMPEG.")
    HLS_TIME = 5
    HLS_LIST_SIZE = 5
    PLAYLIST = directory + "/playlist.m3u8"
    COMMAND = ["ffmpeg", "-i", rtspUrl,
               "-hls_time", str(HLS_TIME),
               "-hls_list_size", str(HLS_LIST_SIZE),
               PLAYLIST]
    logging.debug("HLS command: %s.", " ".join(COMMAND))
    return COMMAND


def startHlsStreaming(rtspUrl: str, mediaDirectory: str):
    # This function starts an HLS streaming from a RTSP url.
    CAMERA_ID = operatingsystem.createRandomName()
    logging.info("Starting a streaming to camera %s.", CAMERA_ID)
    STREAM_PATH = mediaDirectory + "/" + CAMERA_ID
    operatingsystem.createDirectory(STREAM_PATH)
    COMMAND = createHlsCommand(rtspUrl, STREAM_PATH)
    operatingsystem.runCommand(COMMAND)
    logging.debug("Streaming started with '%s'.", COMMAND)


def start(cameras: list, user: str, password: str, directory: str):
    # This function creates workers to process each camera individually
    # and starts HLS streaming for each of them.
    logging.info("Starting HLS streaming for %i cameras.", len(cameras))
    workers = []
    FUNCTION = startHlsStreaming
    for camera in cameras:
        rtspUrl = createRtspUrl(camera, user, password)
        args = (rtspUrl, directory)
        worker = operatingsystem.Worker(FUNCTION, args)
        workers.append(worker)
    operatingsystem.multiprocess(workers)
