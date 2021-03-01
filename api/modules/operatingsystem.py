""" Use this module to interact with the operating system. """

import logging
import subprocess
import shutil
import os
import uuid
import multiprocessing


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
    logging.info("Running an OS subprocess.")
    try:
        if (logging.getLogger().getEffectiveLevel() == logging.DEBUG):
            subprocess.run(command, check=True)
        else:
            subprocess.run(command, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as error:
        logging.error("Command was not executed: %s", " ".join(command))
    else:
        logging.debug("Command executed: %s", " ".join(command))


def multiprocess(workers: list):
    # This function runs multiproscesses.
    logging.info("Creating and running multiprocess.")
    jobs = []
    for worker in workers:
        process = multiprocessing.Process(
            target=worker.function, args=worker.args)
        jobs.append(process)
        process.start()
    logging.debug("%i workers started.", len(workers))


class Worker:
    # This is a class to use with multiprocessing.
    def __init__(self, function: object, args: list):
        self.function = function
        self.args = args
