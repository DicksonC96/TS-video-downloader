import requests
import sys

url = "https://abcd.voxzer.org/stream/608bd4cc0b8bd18237c8fc6d/1080/index"
title = "Tom Clancy's Without Remorse"

with open(title+".ts", 'wb') as f:
    for i in range(5000):
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