import requests
import sys

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

url = "https://abcd.voxzer.org/stream/608bd4cc0b8bd18237c8fc6d/1080/index"
filename = "Tom Clancy's Without Remorse"
### main(url, filename, minimum_iteration, maximum_iteration)
main(url, filename, 1300, 1400)