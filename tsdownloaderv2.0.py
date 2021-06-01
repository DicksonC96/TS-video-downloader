import requests
import sys
import subprocess
from multiprocessing import Pool
import time
import os
import shutil
import numpy as np
from requests.models import MissingSchema
import tqdm
from itertools import product


def downloader(iter):
    #print("Downloading "+str(f'{(pointer/end*100):04d}')+"% ("+str(pointer)+"/"+str(end)+")... ", end='\r', flush=True)
    with open(str(iter)+'.ts', 'wb') as file:
        req = requests.get(url+str(iter)+'.ts', stream=True)
        for chunk in req.iter_content(chunk_size=None):
            file.write(chunk)
        req.close()
    #pbar.update(1)
    #sys.stdout.write("Downloaded "+str(iter)+'.ts ... \n')
    #sys.stdout.flush()

def mp4converter(iter):
    tsfile = str(iter)+'.ts'
    mp4file = f'{iter:04n}'+'.mp4'
    subprocess.run(['ffmpeg', '-i', tsfile, mp4file, '-hide_banner', '-loglevel', 'warning'])

def mp4merger(end):
    with open('files.txt', 'w') as files:
        for i in tqdm.tqdm(range(end), total=end, ncols=100):
            files.write('file \''+str(f'{i:04n}')+'.mp4\'\n')
    subprocess.call('ffmpeg -f concat -safe 0 -i files.txt -c copy ../'+filename+'.mp4'+' -hide_banner -loglevel warning')

def create_tempdir(filename):
    os.mkdir(filename+'~temp')
    os.chdir(filename+'~temp')

def remove_tempdir(filename):
    os.chdir('../')
    shutil.rmtree(filename+'~temp')

def check_iteration_limit(url):
    start = 0
    stop = 10000
    step = 1000
    while step >= 1:
        print('Testing range between '+str(start)+' and '+str(stop)+' ... ', end='\r', flush=True)
        points = np.linspace(start, stop, num=11)
        for pt in points:
            req = requests.get(url+str(int(pt))+'.ts', stream=True)
            bitsize = len(req.content)
            req.close()
            if bitsize < 179:
                stop = int(pt)
                start = int(stop - step)
                step = step/10
                break
    print(str(stop)+' files to be downloaded.                     ', flush=True)
    return stop

def check_file_connection(url):
    try:
        with requests.get(url+'0.ts', stream=True) as req:
            bitsize = len(req.content)
    except MissingSchema:
        return False
    if bitsize < 179:
        return False
    return True

def check_cores(core):
    cores = map(str, range(1, os.cpu_count()))
    while core not in cores:
        if not core.isnumeric() or int(core)<1:
            core = input('\nInvalid input. Valid input range: '+str(list(range(1, os.cpu_count()+1)))+'\nEnter the number of cores for the process (you have '+str(os.cpu_count())+' total cores): ')
        elif int(core)==os.cpu_count():
            reply = input("\nWARNING! YOU WILL USE ALL THE CORES AVALIABLE! (running other processes may cause computer lag)\nContinue? [y/N]... ")
            if reply.lower() == 'n':
                core = input('\nValid input range: '+str(list(range(1, os.cpu_count()+1)))+'\nEnter the number of cores for the process (you have '+str(os.cpu_count())+' total cores): ')
            elif reply.lower() == 'y':
                break
        elif int(core)>os.cpu_count():
            core = input('\nYou don\'t have so many cores. Valid input range: '+str(list(range(1, os.cpu_count()+1)))+'\nEnter the number of cores for the process (you have '+str(os.cpu_count())+' total cores): ')
    return core

def section_line():
    print('\n=============================================\n')

def main():
    global url
    url = sys.argv[1] #"https://abcd.voxzer.org/stream/5fa56f253fac5933e1e4b589/1080/index"
    #filename = sys.argv[2]
#core = 4
main()

if __name__ == "__main__":
    section_line()
    print('   TS Video Downloader\n   Version 2.0\n   Creator: DicksonC96')
    launch_run = 'n'
    while launch_run.lower()=='n':
        section_line()
        '''
        url = input('URL of the video link: ')
        while not check_file_connection(url):
            url = input('Invalid URL. Please check your URL again: ')
        '''
        filename = input('Enter your filename (without format name eg. .mp4): ')
        input_core = input('Enter the number of cores for the process (You have '+str(os.cpu_count())+' total cores; the higher the faster!): ')
        core = check_cores(input_core)
        section_line()
        launch_run = input('   Video to be downloaded: '+filename+'.mp4\n   URL: '+url+'[index].ts\n   Total cores to be used: '+str(core)+'\n\n   Continue? [y/N]... ')
        while launch_run.lower() not in ['y', 'n']:
            launch_run = input('   Continue? Please enter [y/N]... ')

    section_line()
    print('Checking iteration limits at '+url+'[index].ts\'... ', flush=True)
    end = 1 #check_iteration_limit(url)
    print('\nDownloading TS Video \''+filename+'\' from \''+url+'[index].ts\'... ', flush=True)
    create_tempdir(filename)
    pool = Pool(int(core))
    list(tqdm.tqdm(pool.imap_unordered(downloader, range(end)), total=end, ncols=100, position=0, leave=True))
    print('\nFormatting .ts files into .mp4... ', flush=True)
    list(tqdm.tqdm(pool.imap_unordered(mp4converter, range(end)), total=end, ncols=100, position=0, leave=True))
    print('\nMerging .mp4 chunks into '+filename+'.mp4 ... ', flush=True)
    mp4merger(end)
    pool.close()
    pool.join()
    remove_tempdir(filename)
    print('\n   Download done! '+filename+'.mp4 saved to '+os.getcwd()+'\\\n   Enjoy the video!')
    '''
    multiproc = time.time() - v
    sys.stdout.write('map: '+str(map_time)+'\n imap: '+str(multiproc))
    sys.stdout.flush()
    '''