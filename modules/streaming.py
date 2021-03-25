""" Use this class to work with video streaming. """

import logging
from modules import operatingsystem


def createRtspUrl(ip: str, user: str, password: str) -> str:
    logging.debug("Creating a RTSP URL.")
    urlFormat = "rtsp://{user}:{password}@{ip}/live/mpeg4"
    url = urlFormat.format(user=user, password=password, ip=ip)
    logging.debug("RTSP URL: %s.", url)
    return url


def startHlsStreaming(rtspUrl: str, streamPath: str):
    logging.debug("Starting a streaming in %s.", streamPath)
    operatingsystem.createDirectory(streamPath)
    command = createHlsCommand(rtspUrl, streamPath)
    operatingsystem.runCommand(command)
    logging.debug("Streaming started with '%s'.", command)


def createHlsCommand(rtspUrl: str, directory: str) -> list:
    # This function is a wrapper that converts
    # Real-Time Streaming Protocol (RTSP) to
    # HTTP Live Streaming (HLS) using an FFMPEG command.
    # It returns an array: the first element is the name of the
    # command to be executed; any following elements are command-line options.
    logging.debug("Creating an HLS streaming with FFMPEG.")
    HLS_TIME = 5
    HLS_LIST_SIZE = 5
    HLS_FLAGS = "delete_segments"
    PLAYLIST_FILE = directory + "/playlist.m3u8"
    command = ["ffmpeg", "-i", rtspUrl,
               "-hls_time", str(HLS_TIME),
               "-hls_list_size", str(HLS_LIST_SIZE),
               "-hls_flags", HLS_FLAGS,
               PLAYLIST_FILE]
    logging.debug("HLS command: %s.", " ".join(command))
    return command
