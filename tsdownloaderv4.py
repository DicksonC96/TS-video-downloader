import requests
import sys
import subprocess

def main(url, fname, mini=0, maxi=5000):
    with open(fname+".ts", 'wb') as f:
        if not mini==0:
            for i in range(mini):
                r = requests.get(url+str(i)+".ts", stream=True)
                sys.stdout.write("Downloading "+str(i)+".ts ...\n")
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
                sys.stdout.write("Downloading "+str(i)+".ts ...\n")
                sys.stdout.flush()
                for chunk in r.iter_content(chunk_size=None):
                    if chunk:
                        f.write(chunk)
            r.close()

def mp4convert(ts, mp4):
    subprocess.run(['ffmpeg', '-i', ts, mp4])

url = "https://abcd.voxzer.org/stream/5fa56f253fac5933e1e4b589/1080/index"
filename = "The New Mutants"
### main(url, filename, minimum_iteration, maximum_iteration)
main(url, filename, 1600, 1700)
mp4convert(filename+".ts", filename+".mp4")