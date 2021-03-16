# [Eyes](https://github.com/jon-cbar/eyes/)

<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/jon-cbar/eyes?style=flat-square"> <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/jon-cbar/eyes?style=flat-square">

## Context, Problem and Solution

I have some iC3 and iC4 [Intelbras](https://intelbras.com/en) Mibo IP cameras.
The company makes a mobile application available for [Android](https://play.google.com/store/apps/details?id=com.intelbras) and [iPhone](https://apps.apple.com/app/mibo/id1221971306) to access the cameras using its private cloud.

It works, but I wanted to go further.
I needed to watch my cameras on the Smart TV, without using a Digital Video Recorder (DVR) for that.

Well, I decided to run a web server and access the cameras through the TV browser.
I believed it would be more useful than creating an application for Smart TV, as it could also access the cameras on my computer.

The default camera protocol is [Real-Time Streaming Protocol (RTSP)](https://en.wikipedia.org/wiki/Real_Time_Streaming_Protocol), but I needed to use [HTTP Live Streaming (HLS)](https://en.wikipedia.org/wiki/HTTP_Live_Streaming) to access via a web browser.

Then, I had two things to do:

1. Translate, for each camera, RTSP streaming into an HLS streaming; and
2. Run a web server to make the videos available.

I realized that I can make this easy with Python.

## Architecture

![Architecture Diagram](architecture.png)


