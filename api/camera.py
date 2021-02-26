import logging
from network import Network


class Camera:

    # Finds IP cameras connected to the network using
    # Real Time Streaming Protocol (RTSP).
    @staticmethod
    def findCameras() -> list:
        logging.info("Searching for IP cameras with RTSP.")
        IP = Network.getLocalIpAddress()
        DEPTH = 27
        SUBNET_MASK = Network.getSubnetMask(IP, DEPTH)
        PORT = 554
        TIMEOUT = 1
        CAMERAS = Network.findHostsWithPortOpen(SUBNET_MASK, PORT, TIMEOUT)
        logging.debug("Found %i cameras using RTSP.",
                      len(CAMERAS))
        return CAMERAS

    # Creates URL to connect with RTSP.
    @staticmethod
    def createRtspUrl(ip: str, user: str, password: str) -> str:
        URL_FORMAT = "rtsp://{user}:{password}@{ip}/live/mpeg4"
        URL = URL_FORMAT.format(user=user, password=password, ip=ip)
        return URL
