# -*- coding: utf-8 -*-

# Disclaimer! I don't know Python, this script is hacked together.

# FFMPEG must be installed on your machine to run this script.

import os
import subprocess
import re
import sys
import shutil

# setup output folders
directory = "./"
source_dir = directory + "source"
output_dir = directory + "output"
thumbnail_dir = directory + "thumbnails"
if not os.path.isdir(output_dir):
	os.mkdir(output_dir) # make folder for output
else:
	shutil.rmtree(output_dir) # if exists, delete it
	os.mkdir(output_dir) # and re-create it fresh

if not os.path.isdir(thumbnail_dir):
	os.mkdir(thumbnail_dir) # make folder for thumbnails
else:
	shutil.rmtree(thumbnail_dir) # if exists, delete it
	os.mkdir(thumbnail_dir) # and re-create it fresh

# ------------------------
# rename non ascii characters in file names

for file in os.listdir(u"./source"):
    if os.path.isfile(file) and file.endswith(u'.mp4'):
		new_file = "".join(i for i in file if ord(i)<128)
		if (file != new_file):
			print u"Renaming", file.encode('utf8'),u" to ", new_file.encode('utf8')
			os.rename(file, new_file)

# ------------------------
# generate mp3's with thumbnails using FFMPEG

FNULL = open(os.devnull, 'w')

# create a thumbnail for adding to mp3 file, suppresses all FFMPEG output
def create_thumbnail(filename):
	video_path = os.path.join(source_dir, filename)
	thumbnail_path = thumbnail_dir + "/" + filename.replace(".mp4", ".jpg")
	subprocess.call(["ffmpeg", "-i", video_path, "-ss", "00:00:10.000", "-vframes", "1", thumbnail_path], stdout=FNULL, stderr=subprocess.STDOUT)
	return thumbnail_path

# convert a mp4 to and mp3 with a thumbnail.
def create_audio(filename, thumbnail_path):
	video_path = os.path.join(source_dir, filename)
	audio_path = output_dir + "/" + filename.replace(".mp4", ".mp3")
	subprocess.call(["ffmpeg", "-i", video_path, "-i", thumbnail_path, "-acodec", "libmp3lame", "-b:a", "128k", "-c:v", "copy", "-map", "0:a:0", "-map", "1:v:0", audio_path], stdout=FNULL, stderr=subprocess.STDOUT)

# loop all source files and create mp3s
for filename in os.listdir(source_dir):
		try:
			if filename.endswith(".mp4"):
				thumbnail_path = create_thumbnail(filename)
				create_audio(filename, thumbnail_path)
				print "success"
			else:
				continue
		except:
			print "ERROR"
			continue
