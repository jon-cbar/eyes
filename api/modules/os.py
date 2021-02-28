""" Use this module to interact with the operating system. """

import logging
import subprocess
import shutil
import os
import uuid


def createRandomName() -> str:
    # This function creates a random name.
    logging.info("Creating a name.")
    NAME = str(uuid.uuid4())[:8]
    logging.debug("Name: %s.", NAME)
    return NAME


def createDirectory(directory: str):
    # This function creates a directory.
    logging.info("Creating a directory·")
    try:
        os.mkdir(directory)
    except OSError as error:
        logging.error("The directory %s has not been created.")
        logging.error(error)
    else:
        logging.debug("%s created.", directory)


def removeAll(directory: str):
    # This function removes a directory.
    logging.info("Remove a directory.")
    try:
        shutil.rmtree(directory)
    except OSError as error:
        logging.error("The directory %s has not been removed.")
        logging.error(error)
    else:
        logging.debug("%s removed.", directory)


def clearDirectory(directory: str):
    # This function clear a directory.
    logging.info("Clearing the directory.")
    removeAll(directory)
    createDirectory(directory)
    logging.debug("%s cleaned up.", directory)


def runCommand(command: str):
    # This function runs a command.
    logging.info("Creating an OS subprocess.")
    subprocess.run(command)
