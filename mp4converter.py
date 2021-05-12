import subprocess

ts = "Tom Clancy's Without Remorse.ts"
mp4 = "Tom Clancy's Without Remorse.mp4"
subprocess.run(['ffmpeg', '-i', ts, mp4])