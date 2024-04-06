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
import Launcher.py.winmgr as winmgr
import threading

global StepSTP
StepSTP = 0

class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

# Downloads latest build from GitHub
def download_repo(repo_url, output_dir):
    window_width = 600  # Adjust as needed
    window_height = 282  # Adjust as needed
    
    print("Downloading updates..")
    response = requests.get(repo_url + "/archive/main.zip") 
    if response.status_code == 200: # error handling
        with open("temp_repo.zip", "wb") as zip_file:
            zip_file.write(response.content)
        with zipfile.ZipFile("temp_repo.zip", "r") as zip_ref:
            # Extract the entire contents of the ZIP file to the output directory
            zip_ref.extractall(output_dir)
            print("Extracting updates..")
            window_width = 600  # Adjust as needed
            window_height = 282  # Adjust as needed
            time.sleep(1.5)
        # Close the ZipFile object to release the resources
        zip_ref.close()
        # Now it should be safe to remove the temporary zip file
        os.remove("temp_repo.zip")
    else:
        print(f"Failed to download repository: {response.status_code} - {response.reason}")
        window_width = 600  # Adjust as needed
        window_height = 282  # Adjust as needed

# Function to execute download_repo() and to apply all the changes
def update_launcher(repo_url):
    script_dir = os.path.dirname(os.path.realpath(__file__)) # to find the real parent
    parent_dir = os.path.dirname(script_dir)
    grandparent_dir = os.path.dirname(parent_dir) # which is the ServerSetup folder in the workspace.
    # Delete the existing Launcher folder if it exists
    print("Clearing up outdated files..")
    existing_launcher_dir = os.path.join(script_dir, "Launcher")
    if os.path.exists(existing_launcher_dir):
        shutil.rmtree(existing_launcher_dir) 

    # download repo
    image_path2 = r'BackupResource\HCUpdateRSC.png'
    winmgr.close_window(image_path2)
    download_repo(repo_url, grandparent_dir)
    downloaded_launcher_dir = os.path.join(grandparent_dir, "HCLauncher-main", "Launcher")
    print("Verifying update files..")
    time.sleep(1)
    shutil.move(downloaded_launcher_dir, script_dir) # moves Launcher to ServerSetup, or whatever the name of the workspace would be.
    #delete cache
    print("Clearing up..")
    image_path = r'Launcher\py\Resources\HClearUp.png'
    winmgr.close_window(image_path)
    window_width = 600  # Adjust as needed
    window_height = 282  # Adjust as needed
    extracted_repo_dir = os.path.join(grandparent_dir, "HCLauncher-main")
    shutil.rmtree(extracted_repo_dir) # deletes extracted zip from the workspace.
    time.sleep(1)
    print("Launcher up to date!")
    image_path = r'Launcher\py\Resources\HCLaunchUpdated.png'
    winmgr.close_window(image_path)
    window_width = 600  # Adjust as needed
    window_height = 282  # Adjust as needed
    
    print(downloaded_launcher_dir)
    # imports the launcher.py script from the updated launcher directory
    launcher_script_path = os.path.join(script_dir, "Launcher", "py")
    
    if os.path.exists(launcher_script_path):
        try:
            import sys
            sys.path.append(os.path.join(script_dir, "Launcher", "py")) # self explanatory
            print("Launching..")
            image_path = r'Launcher\py\Resources\HCLaunching.png'
            winmgr.close_window(image_path)         
            window_width = 600  # Adjust as needed
            window_height = 282  # Adjust as needed
            time.sleep(2)
            import launcher
            # Call the desired function from your_script
            launcher.open_game()
            winmgr.close_window(image_path)
        except Exception as e: #error reports. {e} is the error message. this error results when launcher.py cannot be run. Maybe it can be resolved without a new .exe
            print(f"{Colors.CYAN}Report the following errors to developers: {Colors.RESET}")
            print(f"{Colors.RED}(Report this error to developers!) - Error on running launcher.py: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}Upgrader could not finish updating successfully. Download launcher again from Discord {Colors.RESET}")
            image_path = r'Launcher\py\Resources\HCLaunchFailGr.png'
            winmgr.close_window(image_path)
            window_width = 600  # Adjust as needed
            window_height = 282  # Adjust as needed
            print("Terminal exiting in (120)s.")
            time.sleep(120)
    else:
        #error reports. happens when the Launcher directory is not found. Usually requires a new .exe
        print(f"{Colors.RED}Upgrader could not finish updating successfully. Download launcher again from Discord. {Colors.RESET}")
        print("Terminal exiting in (120)s.")
        time.sleep(120)

def check_for_updates():
    # Fetch the INI file from GitHub
    repo = "https://raw.githubusercontent.com/sharl16/HCLauncher/main/Launcher/py/HCLaunch.ini"
    response = requests.get(repo)
    # Check if the request was successful
    if response.status_code == 200:
        launcher_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Launcher"))
        sys.path.append(launcher_path)
        # Parse the local INI file
        config = configparser.ConfigParser()
        ini_file_path = os.path.join(launcher_path,'py', 'HCLaunch.ini')
        config.read(ini_file_path)
        appversion = config.get('APPVersion', 'version')
        print("HCLauncher, Version:", appversion)
        time.sleep(1)
        # Parse the remote INI file
        remote_config = configparser.ConfigParser()
        remote_config.read_string(response.text)
        
        # Get the version from both INI files
        local_ver = config['APPVersion']['version']
        remote_ver = remote_config['APPVersion']['version']
        print("Checking for updates.")
        image_path = r'Launcher\py\Resources\HCCheckUPD.png'
        winmgr.close_window(image_path)
        time.sleep(0.5)
        window_width = 600  # Adjust as needed
        window_height = 282  # Adjust as needed
        # Compare versions
        if appversion == remote_ver:
            print("Application up to date!")
            image_path = r'Launcher\py\Resources\HCLaunchUpdated.png'
            winmgr.close_window(image_path)
            window_width = 600  # Adjust as needed
            window_height = 282  # Adjust as needed
            time.sleep(1)
            launcher_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Launcher", "py"))
            sys.path.append(launcher_path)
            image_path = r'Launcher\py\Resources\HCLaunching.png'
            winmgr.close_window(image_path)
            import launcher
            window_width = 600  # Adjust as needed
            window_height = 282  # Adjust as needed
            launcher.open_game()
        else:
            print("Application out of date! Updating!")
            image_path = r'Launcher\py\Resources\HCUpdateInProgress.png'
            winmgr.close_window(image_path)
            window_width = 600  # Adjust as needed
            window_height = 282  # Adjust as needed
            time.sleep(5)
            update_launcher(repo_url="https://github.com/sharl16/HCLauncher")
    else:
        print("Failed to fetch HCLaunch.ini from server.")
        image_path = r'Launcher\py\Resources\HCLaunchGitFail.png'
        winmgr.close_window(image_path)
        window_width = 600  # Adjust as needed
        window_height = 282  # Adjust as needed
        time.sleep(10)


# Continue with checking for updates concurrently
check_for_updates()