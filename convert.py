import os
import subprocess

directory = "./"
output_dir = directory + "output"
thumbnail_dir = directory + "thumbnails"
if not os.path.isdir(output_dir):
	os.mkdir(output_dir)
if not os.path.isdir(thumbnail_dir):
	os.mkdir(thumbnail_dir)

def create_thumbnail(filename):
	video_path = os.path.join(directory, filename)
	thumbnail_path = thumbnail_dir + "/" + filename.replace(".mp4", ".jpg")
	subprocess.check_output(['ffmpeg', '-i', video_path, '-ss', '00:00:10.000', '-vframes', '1', thumbnail_path])
	return thumbnail_path

def create_audio(filename, thumbnail_path):
	video_path = os.path.join(directory, filename)
	audio_path = output_dir + "/" + filename.replace(".mp4", ".mp3")
	subprocess.check_output(["ffmpeg", "-i", video_path, "-i", thumbnail_path, "-acodec", "libmp3lame", "-b:a", "128k", "-c:v", "copy", "-map", "0:a:0", "-map", "1:v:0", audio_path])

for filename in os.listdir(directory):
	if filename.endswith(".mp4"): 
		thumbnail_path = create_thumbnail(filename)
		create_audio(filename, thumbnail_path)
	else:
		continue