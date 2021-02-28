""" Use this module to work with video streaming. """

import subprocess


def createRtspUrl(ip: str, user: str, password: str) -> str:
    # This function creates URL to connect with RTSP.
    URL_FORMAT = "rtsp://{user}:{password}@{ip}/live/mpeg4"
    URL = URL_FORMAT.format(user=user, password=password, ip=ip)
    return URL


def createHlsCommand(rtspUrl: str) -> str:
    # This function is a wrapper that converts
    # Real-Time Streaming Protocol (RTSP) to
    # HTTP Live Streaming (HLS) using an FFMPEG command.
    # It returns an array: the first element is the name of the
    # command to be executed; any following elements are command-line options.
    HLS_COMMAND = ["ffmpeg", "-i", rtspUrl, "playlist.m3u8"]
    return HLS_COMMAND


def runHls(hlsCommand: str):
    # This function runs an FFMPEG instance with an HLS video.
    subprocess.run(hlsCommand)
