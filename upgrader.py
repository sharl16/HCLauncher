import os
import sys
import requests
import shutil
import zipfile
import time
import configparser
import importlib
import subprocess
import tkinter
import multiprocessing
import threading
import keyboard

print("Upgrader Version: 2.0")

import Launcher.py.winmgr as winmgr # type: ignore

root_dir = os.path.join(os.getenv('APPDATA'), 'HCLauncher')
if os.path.exists(root_dir):
    print("Integrity OK!")
    print("Installed at: "+root_dir)
else:
    print("Application cannot be started. Unfinished installation.")

time.sleep(1)

def download_repo():
    print("Downloading latest version from GitHub..")
    repo = "https://github.com/sharl16/HCLauncher"
    image_path = r'Launcher\py\Resources\HCDownloadUPD.png'
    winmgr.close_window(image_path)
    response = requests.get(repo + "/archive/main.zip")
    if response.status_code == 200:
        with open("temp_repo.zip", "wb") as zip_file:
            zip_file.write(response.content)
        with zipfile.ZipFile("temp_repo.zip", "r") as zip_ref:
            image_path = r'Launcher\py\Resources\HCExtractUPD.png'
            winmgr.close_window(image_path)
            print("Download proccess finished.")
            zip_ref.extractall(root_dir)
            print("Archive extracted from .zip")
        zip_ref.close()  
        os.remove("temp_repo.zip") 
    else:
        print(f"Failed to download repository: {response.status_code} - {response.reason}")
        image_path = r'Launcher\py\Resources\HCLaunchGitFail.png'
        winmgr.close_window(image_path)
        time.sleep(5)
        winmgr.close_windowr()
        raise SystemError

def update_app():
    download_repo()
    image_path = r'Launcher\py\Resources\HCPatch.png'
    winmgr.close_window(image_path)
    existing_launcher_dir = 'Launcher'
    if os.path.exists(existing_launcher_dir):
        shutil.rmtree(existing_launcher_dir)
        print("Removed outdated Launcher.")
    downloaded_launcher_dir = os.path.join(root_dir, "HCLauncher-main", "Launcher")
    print(downloaded_launcher_dir)
    print("Patching files..")
    shutil.move(downloaded_launcher_dir, root_dir)
    downloaded_repo = os.path.join(root_dir, "HCLauncher-main")
    shutil.rmtree(downloaded_repo)
    check_for_updates()

def check_for_updates():   
    image_path = r'Launcher\py\Resources\HCCheckUPD.png'
    winmgr.close_window(image_path)
    repo = "https://raw.githubusercontent.com/sharl16/HCLauncher/main/Launcher/py/HCLaunch.ini"
    response = requests.get(repo)
    if response.status_code == 200:
        localconfig = configparser.ConfigParser()
        local_config_path = r'Launcher\py\HCLaunch.ini'
        localconfig.read(local_config_path)
        app_local_version = localconfig['APPVersion']['version']
        print("local version:"+app_local_version)
        remote_config = configparser.ConfigParser()
        remote_config.read_string(response.text)
        app_github_version = remote_config['APPVersion']['version']
        print("github version:"+app_github_version)
        if app_local_version == app_github_version:
            image_path = r'Launcher\py\Resources\HCLaunchUpdated.png'
            winmgr.close_window(image_path)
            image_path2 = r'Launcher\py\Resources\HCLaunching.png'
            winmgr.close_window(image_path2)
            print("Up to date!")
            print(local_config_path)
            launcher_dir = 'Launcher.py.launcher'  # corrected path
            launcher = importlib.import_module(launcher_dir) 
            launcher.open_game()
        else:
            print("Updating")
            image_path = r'Launcher\py\Resources\HCUpdateInProgress.png'
            winmgr.close_window(image_path)
            update_app()

check_for_updates()
        