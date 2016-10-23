#!usr/bin/env python
#coding=utf-8

import pyaudio
import wave

#define stream chunk
chunk = 1024

#open a wav format music
f = wave.open(r"/home/pi/Desktop/SD2Project/MusicPlay/FTT.wav","rb")
#instantiate PyAudio
p = pyaudio.PyAudio()
#open stream
stream = p.open(format = p.get_format_from_width(f.getampwidth()),
		channels = f.getnchannels(),
		rate =f.getframerate(),
		output = True)

#read data
data = f.readframes(chunk)

#play stream
while data != '':
	stream.write(data)
	data = f.readframes(chunk)

#stop stream
stream.stop_stream()
stream.close()

#close PYaudio
p.terminate()
