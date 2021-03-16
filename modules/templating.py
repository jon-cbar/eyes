""" Use this class to work with HTML Templating. """

import re
from modules import operatingsystem


class Template:

    def __init__(self,
                 templateFilePath: str = "template.html",
                 html: str = "",
                 script: str = "",
                 mediaDirectory: str = "media"):
        self.templateFilePath = templateFilePath
        self.html = html
        self.script = script
        self.mediaDirectory = mediaDirectory

    def createFile(self, filename: str):
        # Creates a file from template and content.
        content = operatingsystem.readFile(self.templateFilePath)
        content = re.sub("{html}", self.html, content)
        content = re.sub("{script}", self.script, content)
        operatingsystem.writeFile(filename, content)

    def includeCamera(self, cameraID: str):
        self.html += self.__createDiv(cameraID)
        self.script += self.__createScript(cameraID)

    def __createDiv(self, cameraID: str) -> str:
        template = '<div id="c{cameraID}" class="camera"></div>'
        content = template.format(cameraID=cameraID)
        return content

    def __createScript(self, cameraID: str) -> str:
        content = 'var c' + cameraID + ' = new Clappr.Player({ '
        content += 'source: "{0}/{1}'.format(self.mediaDirectory, cameraID)
        content += '/playlist.m3u8", parentId: "#c{0}", '.format(cameraID)
        content += 'autoPlay: true, muted: true });'
        return content
