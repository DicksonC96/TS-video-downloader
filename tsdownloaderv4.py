import requests
import sys
import subprocess

def main(url, fname, mini=0, maxi=5000):
    with open(fname+".ts", 'wb') as f:
        if not mini==0:
            for i in range(mini):
                r = requests.get(url+str(i)+".ts", stream=True)
                sys.stdout.write("Downloading "+str(i)+".ts ... ("+str(round((i/maxi*100),4))+"% in <"+str(maxi)+" iterations)\n")
                sys.stdout.flush()
                for chunk in r.iter_content(chunk_size=None):
                    if chunk:
                        f.write(chunk)
            r.close()
        for i in range(mini, maxi):
            r = requests.get(url+str(i)+".ts", stream=True)
            if len(r.content) < 179:
                print("Download finished with "+str(i+1)+" iterations.")
                break
            else:
                sys.stdout.write("Downloading "+str(i)+".ts ... ("+str(round((i/maxi*100),4))+"% in <"+str(maxi)+" iterations)\n")
                sys.stdout.flush()
                for chunk in r.iter_content(chunk_size=None):
                    if chunk:
                        f.write(chunk)
            r.close()

def mp4convert(ts, mp4):
    subprocess.run(['ffmpeg', '-i', ts, mp4])

url = "https://abcd.voxzer.org/stream/6082ef4d0b8bd18237c8fc11/1080/index"
filename = "Mortal Kombat"
### main(url, filename, minimum_iteration, maximum_iteration)
main(url, filename, 3200, 3300)
mp4convert(filename+".ts", filename+".mp4")