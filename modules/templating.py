""" Use this class to work with HTML Templating. """

import re
from modules import operatingsystem


class Template:

    def __init__(self,
                 templateFile: str = "template.html",
                 html: str = "",
                 script: str = ""):
        self.templateFile = templateFile
        self.html = html
        self.script = script

    def createFile(self, filename: str):
        # Creates a file from template and content.
        content = operatingsystem.readFile(self.templateFile)
        content = re.sub("{html}", self.html, content)
        content = re.sub("{script}", self.script, content)
        operatingsystem.writeFile(filename, content)
