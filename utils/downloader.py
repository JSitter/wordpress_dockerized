#! /usr/bin/env python3

import tarfile
import os
import os.path as path
import shutil
import hashlib
import sys
import time
import math
import urllib.request as req

wordpress_download_url = "https://wordpress.org/latest.tar.gz"
home_dir = os.path.dirname(os.path.realpath(__file__))
temp_dir = home_dir + '/.tempdir'
forbidden_folders = {''}
forbidden_files = {'.htaccess'}

def check_dir(directory):
    if not path.exists(directory):
        os.mkdir(directory)

def remove_directory(source):
    print("Removing {}".format(source))
    shutil.rmtree(source)

def remove_file(source):
    print("Removing {}".format(source))
    os.remove(source)

def replace_item(source, destination):
    if path.isdir(destination):
        remove_directory(destination)
    else:
        remove_file(destination)
    
    shutil.move(source, destination)

def update_file(temp_location, file, destination, replace=False):
    file_destination = "{}/{}".format(destination, file)
    temp_file_location = "{}/{}".format(temp_location, file)

    if not path.exists(file_destination):
        shutil.move(temp_file_location, destination)
    elif replace:
        replace_item(temp_file_location, file_destination)
    else:
        if file in forbidden_folders or file in forbidden_files:
            print("Skipping {}. File already exists.".format(file))
        else:
            try:
                replace_item(temp_file_location, file_destination)
                print("Replaced {}".format(file))
            except:
                print("{} locked".format(file))

def unpack_gz_into(source, destination, replace=False, save_extract=False):
    tar = tarfile.open(source, 'r:gz')
    allfiles = tar.getnames()
    print(allfiles)
    temp_source_dir = "{}/{}".format(temp_dir, allfiles[0])

    check_dir(temp_dir)
    check_dir(destination)
    
    tarball = tarfile.open(source, 'r:gz')
    tarball.extractall(path=temp_dir)
    files = os.listdir(temp_source_dir)

    for file in files:
        update_file(temp_source_dir, file, destination, replace)

    if not save_extract:
        shutil.rmtree(temp_source_dir)
    print("Done")

def download_report_hook(count, chunk_size, total_size):
    global start_time
    global progress
    current_time = time.time()
    if count == 0:
        start_time = current_time
        progress = int(chunk_size)
        return
    duration = current_time - start_time
    progress += int(chunk_size)
    speed = int(progress / (1024 * duration))
    if speed > 799:
        speed = speed / 1000
        speed_scale = "MB/s"
    else:
        speed_scale = "KB/s"
    percent = progress * 100 / total_size
    progress_mb = progress / (1024 * 1024)
    percent_scale = int(math.floor(percent)/4)
    vis_downloaded = "=" * percent_scale
    vis_remaining = "." * (25 - percent_scale) + '|'
    CURSOR_UP = '\x1b[1A'
    CLEAR_LINE = '\x1b[2k'

    sys.stdout.write("{}{}\r{}>{}               \n".format(CURSOR_UP, CLEAR_LINE, vis_downloaded, vis_remaining))
    sys.stdout.write("\r{}{} {:.2f}% -- {:.2f}MB out of {:.2f}MB {:.0f}s          ".format(speed, speed_scale, percent, progress_mb, total_size/1000000, duration))
    sys.stdout.flush()

def download_wp_version(download_url, destination):
    print("Downloading from {}".format(download_url))
    retry = True
    user_affirmative = {"Y", "y"}
    while retry:
        retry = False
        try:
            print("Downloading {}".format(destination.split('/')[-1]))
            req.urlretrieve(download_url, destination, download_report_hook)
        except:
            user_retry = input("Failed to complete download. Retry? [Y/n] ")
            if user_retry in user_affirmative:
                retry = True
            else:
                sys.exit(1)
        else:
            time_completed = time.time() - start_time
            sys.stdout.write("\rDownload Complete in {:.1f} seconds.                                \n".format(time_completed))
            sys.stdout.flush()

def handle_wp_download(download_url, filename, source_hash=""):
    check_dir(temp_dir)
    user_affirmative = {"Y", "y"}
    destination = "{}/{}".format(temp_dir, filename)
    # Allow user to retry if package fails to download

    if path.exists(destination):
        use_cached_file = input("Use cached Wordpress download? Y/n?")
        print(use_cached_file)
        if use_cached_file not in user_affirmative:
            download_wp_version(download_url, destination)
        else:
            print("Using cached file.")
    else:
        download_wp_version(download_url, destination)
    
    retry = True
    while retry:
        retry = False
        f = open(destination, 'rb')
        # print("Verifying package authenticity.")
        # if source_hash == "":
        #     print("No hash provided. Unable to authenticate.")
        file_hash = hashlib.md5(f.read()).hexdigest()
        f.close()
        if source_hash != "" and file_hash != source_hash:
            user_retry_download = input("Warning! Hash Mismatch. Retry download? [Y/n] ")
            remove_file(destination)
            if user_retry_download in user_affirmative:
                download_wp_version(download_url, destination)
                retry = True
            else:
                sys.exit(1)

if __name__ == '__main__':
    handle_wp_download(wordpress_download_url, 'latest.tar.gz')
    unpack_gz_into(temp_dir+'/latest.tar.gz', "wp-core" )