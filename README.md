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

I realized that I can make this easy with [Python](https://www.python.org/) and [FFmpeg]((https://www.ffmpeg.org/)).

## Python

Python is a versatile programming language.
It has its limitations, but also deliver a lot of things ready at a very low computational cost.
For example, I can start a web server and run commands on the operating system in parallel, using subprocesses and multiprocessing.

### Web Server

To start a web server, I used the [`http.server`](https://docs.python.org/3/library/http.server.html) module.
As mentioned in the documentation, it is not recommended for use in a production environment, because of resource limitations that ensure better application security.
For my case, with use in the home environment, it meets.

### Concurrent Execution

> [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html) package offers concurrency, using subprocesses instead of threads. Due to this, the multiprocessing module allows the programmer to fully leverage multiple processors on a given machine.

### FFmpeg

`ffmpeg` is a cross-platform video and audio converter.
It has a command line tool that makes it easy to convert between [different protocols](http://ffmpeg.org/ffmpeg-protocols.html).
For example, to translate a RTSP streaming provided by a IP Camera (`192.168.1.2`) into an HLS streaming, you can use this:

```sh
ffmpeg -i rtsp://192.168.1.2/live/mpeg4 playlist.m3u8
```

## Architecture Components

![Architecture Diagram](architecture.png)

