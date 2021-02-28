""" Use this module to work with IP cameras. """

import logging
import socket
import ipaddress


def isPortOpen(host: str, port: int, timeout: float = 0.1) -> bool:
    # This function says if a port is open in a host.
    logging.debug("Checking if port %i is open in host %s.", port, host)
    isOpen = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET:
        SOCKET.settimeout(timeout)
        ADDRESS = (host, port)
        try:
            SOCKET.connect(ADDRESS)
            logging.debug("%s:%i is open.", host, port)
            isOpen = True
        except:
            # logging.debug(error)
            pass
    return isOpen


def findHostsWithPortOpen(mask: str, port: int, timeout: float = 0.1) -> list:
    # This function finds hosts running in the network with a specific port open.
    # Param 'mask' is a subnet mask like '192.168.1.0/27'
    # to represent the range where will be looking for.
    logging.info("Searching hosts on port %i in %s.", port, mask)
    logging.info("Please wait, this can take a little time...")
    hosts = []
    NETWORK_HOSTS = ipaddress.IPv4Network(mask).hosts()
    for HOST in NETWORK_HOSTS:
        if (isPortOpen(str(HOST), port)):
            hosts.append(str(HOST))
    logging.debug("Found %i hosts on port %i.", len(hosts), port)
    return hosts


def getLocalIpAddress() -> str:
    # This function finds the local IP address.
    logging.info("Finding local IP address.")
    ip = '127.0.0.1'
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as SOCKET:
            SOME_HOST = "1.2.3.4"
            SOME_PORT = 10
            SOME_ADDRESS = (SOME_HOST, SOME_PORT)
            SOCKET.connect(SOME_ADDRESS)
            ip = SOCKET.getsockname()[0]
    except:
        ip = socket.gethostbyname(socket.gethostname())
    logging.debug("Local IP address: %s.", ip)
    return ip


def getSubnetMask(ip: str, depth: int) -> str:
    # This function creates a subnet mask from an IP and a depth.
    logging.info("Creating a subnet mask.")
    BROKEN_IP = ip.split('.')
    subnet = '0.0.0.0'
    if (depth >= 24):
        subnet = BROKEN_IP[0] + '.' + \
            BROKEN_IP[1] + '.' + BROKEN_IP[2] + '.0'
    elif (depth >= 16):
        subnet = BROKEN_IP[0] + '.' + BROKEN_IP[1] + '.0.0'
    elif (depth >= 8):
        subnet = BROKEN_IP[0] + '.0.0.0'
    MASK = subnet + '/' + str(depth)
    logging.debug("Subnet mask: %s.", MASK)
    return MASK


def findRtspCameras(depthMask: int = 27, rtspPort: int = 554, timeout: int = 1) -> list:
    # This function finds IP cameras connected to the network using
    # Real-Time Streaming Protocol (RTSP).
    # Default values:
    # - Depth Mask: 27, looking for the 32 first IP addresses in a subnet (192.168.0.0/27).
    # - Port: 554, default RTSP streaming port.
    # - Timeout: 1 second.
    logging.info("Searching for IP cameras with RTSP.")
    IP = getLocalIpAddress()
    SUBNET_MASK = getSubnetMask(IP, depthMask)
    CAMERAS = findHostsWithPortOpen(
        SUBNET_MASK, rtspPort, timeout)
    logging.debug("Found %i cameras using RTSP.",
                  len(CAMERAS))
    return CAMERAS
