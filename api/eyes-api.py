import ipaddress
import logging
import socket


# It finds IP cameras running in a port.
# Mask param is something like '192.168.1.0/27'
# to represent the range where will be looking for.
def findCameras(mask, port, timeout = 0.1):
    logging.info("Searching for cameras on port %s...", str(port))
    cameras = []
    for host in ipaddress.IPv4Network(mask):
        logging.info("Trying on %s:%s.", str(host), str(port))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(timeout)
            address = (str(host), port)
            try:
                connection.connect(address)
                logging.debug("Port is open.")
                cameras.append(str(host))
            except socket.error as error:
                logging.debug(error)
    return cameras

# It creates an RTSP address to connect to the IP camera.
def createRtspUrl(ip, user, password):
    urlFormat = "rtsp://{user}:{password}@{ip}/live/mpeg4"
    url = urlFormat.format(user = user, password = password, ip = ip)
    return url

logFormat = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(format = logFormat, level = logging.INFO)

mask = '192.168.1.0/27'
port = 554
cameras = findCameras(mask, port)

user = 'user'
password = 'password'
for ip in cameras:
    url = createRtspUrl(ip, user, password)
    logging.info(url)