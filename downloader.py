import requests

url = "https://abcd.voxzer.org/stream/604391840b8bd18237c8f91f/1080/index"
for i in range(1300):
    try:
        r = requests.get(url+str(i)+".ts", stream=True)
        with open(str(i)+".ts","wb") as f:
            for chunk in r.iter_content(chunk_size=None):
                print("Downloading "+str(i)+".ts ...")
                if chunk:
                    f.write(chunk)
        r.close()
    except:
        print(r.raise_for_status())
        break