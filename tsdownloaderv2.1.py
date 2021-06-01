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
import argparse
import copy

def downloader(iter):
    #print("Downloading "+str(f'{(pointer/end*100):04d}')+"% ("+str(pointer)+"/"+str(end)+")... ", end='\r', flush=True)
    with open(str(iter)+'.ts', 'wb') as file:
        req = requests.get(url+'index'+str(iter)+'.ts', stream=True)
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

def create_tempdir():
    num = 1
    while os.path.exists(os.getcwd()+'/~temp'+str(num)):
        num += 1
    os.mkdir('~temp'+str(num))
    os.chdir('~temp'+str(num))

def remove_tempdir():
    temp_path = os.getcwd()
    os.chdir('../')
    shutil.rmtree(temp_path)

def check_iteration_limit(url):
    start = 0
    stop = 10000
    step = 1000
    while step >= 1:
        print('Testing range between '+str(start)+' and '+str(stop)+' ... ', end='\r', flush=True)
        points = np.linspace(start, stop, num=11)
        for pt in points:
            req = requests.get(url+'index'+str(int(pt))+'.ts', stream=True)
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
        with requests.get(url+'index0.ts', stream=True) as req:
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
            reply = input("\nWARNING! YOU WILL USE ALL THE CORES AVALIABLE! (running other processes may cause computer lag)\n   Continue? [y/N]... ")
            if reply.lower() == 'n':
                core = input('\nValid input range: '+str(list(range(1, os.cpu_count()+1)))+'\nEnter the number of cores for the process (you have '+str(os.cpu_count())+' total cores): ')
            elif reply.lower() == 'y':
                break
        elif int(core)>os.cpu_count():
            core = input('\nYou don\'t have so many cores. Valid input range: '+str(list(range(1, os.cpu_count()+1)))+'\nEnter the number of cores for the process (you have '+str(os.cpu_count())+' total cores): ')
    return core

def section_line():
    print('\n=============================================\n')

def argparser():
    parser = argparse.ArgumentParser(description='TS Video Downloader Version 2.0 (Creator: DicksonC96)')
    parser.add_argument('url', metavar='URL', help='URL of the link (without \'index[number].ts\')')
    parser.add_argument('filename', metavar='Filename', nargs='?', help='Output mp4 file name')
    parser.add_argument('core', metavar='Core(s)', nargs='?', help='Number of core processor(s) to be used') #, nargs='?'
    arguments = parser.parse_args()
    '''
    global url, filename, core
    url = arguments.url
    filename = arguments.filename
    core = arguments.core
    '''
    return arguments.url, arguments.filename, arguments.core #"https://abcd.voxzer.org/stream/5fa56f253fac5933e1e4b589/1080/index"

def input_gui(url, filename=None, core=None):
    section_line()
    print('   TS Video Downloader\n   Version 2.1\n   Creator: DicksonC96')
    section_line()
    launch_run = 'n'
    while launch_run.lower()=='n':
        #if url==None:
        #    url = input('URL of the video link: ')
        while not check_file_connection(url):
            print('Invalid URL. Please check your URL and try again. \n')
            sys.exit()
        if filename==None:
            filename = input('Enter your filename (without format eg. .mp4): ')
        while os.path.exists(os.getcwd()+'\\'+filename+'.mp4'):
            filename = input('File \"'+filename+'.mp4\" already exists. Try another filename (without format eg. .mp4): ')
        if core==None:
            core = input('Enter the number of cores for the process (You have '+str(os.cpu_count())+' total cores; the higher the faster!): ')
        core = check_cores(core)
        print('All checks passed.')
        section_line()
        launch_run = input('Video to be downloaded: \"'+filename+'.mp4\"\nURL: \"'+url+'[index].ts/\"\nTotal core processor(s) to be used: '+str(core)+'\nFile location: '+os.getcwd()+'\\ (current directory)\n\n   Continue? [y/N]... ')
        if launch_run.lower() == 'n':
            filename = core = None
            section_line()
            print('Change the parameters as followed or press \"CTRL+C\" to exit.')
        while launch_run.lower() not in ['y', 'n']:
            launch_run = input('   Continue? Please enter [y/N]... ')
    return filename, core


### Program starts here
#url, filename, core = 
url, filename, core = argparser()

#url = copy.deepcopy(url)
#url, filename, core = input_gui(a, b, c)

'''
print(url)
print(filename)
print(core)

url = 'https://abcd.voxzer.org/stream/5fa56f253fac5933e1e4b589/1080/index'
filename = 'test1'
core = 4
'''
if __name__ == "__main__":
    filename, core = input_gui(url, filename, core)
    section_line()
    print('Checking iteration limits at \"'+url+'index[number].ts\"... ', flush=True)
    end = check_iteration_limit(url)
    print('\nDownloading TS Video \"'+filename+'\" from \"'+url+'index[number].ts\"... ', flush=True)
    create_tempdir()
    pool = Pool(int(core))
    list(tqdm.tqdm(pool.imap_unordered(downloader, range(end)), total=end, ncols=100, position=0, leave=True))
    print('\nFormatting .ts files into .mp4... ', flush=True)
    list(tqdm.tqdm(pool.imap_unordered(mp4converter, range(end)), total=end, ncols=100, position=0, leave=True))
    print('\nMerging .mp4 chunks into \"'+filename+'.mp4\" ... ', flush=True)
    mp4merger(end)
    pool.close()
    pool.join()
    remove_tempdir()
    print('\nDownload done! \"'+filename+'.mp4\" saved to '+os.getcwd()+'\\\nEnjoy the video!\n')
    '''
    multiproc = time.time() - v
    sys.stdout.write('map: '+str(map_time)+'\n imap: '+str(multiproc))
    sys.stdout.flush()
    '''