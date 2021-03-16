""" Use this module to interact with the operating system. """

import logging
import subprocess
import shutil
import os
import multiprocessing


def emptyDirectory(directory: str):
    # This function empties a directory.
    logging.debug("Emptying a directory.")
    removeDirectory(directory)
    createDirectory(directory)
    logging.debug("%s emptied.", directory)


def startWorkers(workers: list):
    # This function runs workers.
    logging.debug("Creating and running workers as processes.")
    jobs = []
    for worker in workers:
        process = multiprocessing.Process(
            target=worker.function, args=worker.args)
        jobs.append(process)
        process.start()
    logging.debug("%i workers started.", len(workers))


def createDirectory(directory: str):
    # This function creates a directory.
    logging.debug("Creating a directory·")
    try:
        os.mkdir(directory)
    except OSError as error:
        logging.error("The directory %s has not been created.")
        logging.error(error)
    else:
        logging.debug("%s created.", directory)


def removeDirectory(directory: str):
    # This function removes a directory.
    logging.debug("Removing a directory.")
    try:
        shutil.rmtree(directory)
    except OSError as error:
        logging.error("The directory %s has not been removed.")
        logging.error(error)
    else:
        logging.debug("%s removed.", directory)


def writeFile(filename: str, content: str):
    # This function overrides the content of a file.
    with open(filename, "w") as file:
        file.write(content)


def readFile(filename: str) -> str:
    # This function reads the content of a file.
    content = ""
    with open(filename, "r") as file:
        content = file.read()
    return content


def runCommand(command: list):
    # This function runs a command.
    logging.debug("Running a command as an OS subprocess.")
    try:
        if (logging.getLogger().getEffectiveLevel() == logging.DEBUG):
            subprocess.run(command, check=True)
        else:
            # If the logging level is different from DEBUG,
            # the output generated by the command is not printed.
            subprocess.run(command, check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        logging.error("Command %s was not executed.", command[0])


# This is a class to use with multiprocessing.
class Worker:
    def __init__(self, function: object, args: list):
        self.function = function
        self.args = args