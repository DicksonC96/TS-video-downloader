import requests
for i in range(868, 3000):
    url = "https://abcd.voxzer.org/stream/5fe6f2323fac5933e1e4b85b/1080/index"+str(i)+".ts"
    try:
        r = requests.get(url, stream=True)
        with open(str(i)+".ts","wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    print("Downloading "+str(i)+".ts ...")
        r.close()
    except:
        print("Download stopped at "+str(i))
        break