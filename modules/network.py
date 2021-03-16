""" Use this module to work with Network. """

import logging
import socket
import ipaddress


def findHostsInNetwork(depth: int = 27, port: int = 80, timeout: float = 1.0) -> list:
    # This function finds hosts running in the network with a specific port open.
    # Default values:
    # - depth: 27, looking for the 30 first IP addresses in a subnet (192.168.0.0/27).
    # - port: 80.
    # - Timeout: 1 second.
    logging.debug("Searching hosts with port %i opened.", port)
    ip = getLocalIpAddress()
    mask = getSubnetMask(ip, depth)
    logging.debug("Looking for hosts in %s.", mask)
    logging.debug("Please wait, this can take a little time...")
    foundHosts = []
    hosts = ipaddress.IPv4Network(mask).hosts()
    for host in hosts:
        if (isPortOpen(str(host), port)):
            foundHosts.append(str(host))
    logging.debug("Found %i hosts.", len(foundHosts))
    return foundHosts


def getLocalIpAddress() -> str:
    # This function finds the local IP address.
    logging.debug("Finding local IP address.")
    ip = '127.0.0.1'
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
            SOME_HOST = "1.2.3.4"
            SOME_PORT = 10
            someAddress = (SOME_HOST, SOME_PORT)
            connection.connect(someAddress)
            ip = connection.getsockname()[0]
    except:
        logging.debug("Getting a default IP address.")
        ip = socket.gethostbyname(socket.gethostname())
    logging.debug("Local IP address: %s.", ip)
    return ip


def getSubnetMask(ip: str, depth: int) -> str:
    # This function creates a subnet mask from an IP and a depth.
    logging.debug("Creating a subnet mask.")
    splittedIp = ip.split('.')
    subnet = '0.0.0.0'
    if (depth >= 24):
        subnet = splittedIp[0] + '.' + \
            splittedIp[1] + '.' + splittedIp[2] + '.0'
    elif (depth >= 16):
        subnet = splittedIp[0] + '.' + splittedIp[1] + '.0.0'
    elif (depth >= 8):
        subnet = splittedIp[0] + '.0.0.0'
    mask = subnet + '/' + str(depth)
    logging.debug("Subnet mask: %s.", mask)
    return mask


def isPortOpen(host: str, port: int, timeout: float = 0.1) -> bool:
    # This function says if a port is open in a host.
    logging.debug("Checking if port %i is open in host %s.", port, host)
    isOpen = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        connection.settimeout(timeout)
        address = (host, port)
        try:
            connection.connect(address)
            logging.debug("%s:%i is open.", host, port)
            isOpen = True
        except:
            # logging.debug(error)
            pass
    return isOpen
