import os
import requests
import subprocess
import psutil
import time
import sys
import mcinstall
import winmgr

sys.path.append('Launcher/py')

version = "ForgeOptiFine 1.20.1" # can be updated and changed
mcinstall.verifyMCVersion(version)

verified = False
appdata_directory = os.getenv('APPDATA')

def download_file(url, output_directory):
    image_path = r'_internal\Launcher\py\Resources\HCSplash.png'
    winmgr.close_window(image_path)
    filename = url.split("/")[-1]
    output_path = os.path.join(output_directory, filename)
    with requests.get(url, stream=True) as req:
        req.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in req.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return output_path


def verify_versions(filename, output_directory):

    global verified
    mcdir = ".minecraft\\versions\\ForgeOptiFine 1.20.1"
    mcversion = os.path.join(os.getenv('APPDATA'), mcdir)
    if os.path.exists(mcversion):
        filepath = os.path.join(output_directory, filename)
        if os.path.exists(filepath):
            verified = True
    else:
        verified = False
        print("Minecraft directory does not exist.")
        return False

def process_status(process_name):
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return True
    return False


def open_game():
    image_path = r'_internal\Launcher\py\Resources\HCLaunching.png'
    winmgr.close_window(image_path)
    terminated = False
    appdata_directory = os.getenv('APPDATA')
    game_dir = ".minecraft\\TLauncher.exe"
    game_path = os.path.join(appdata_directory, game_dir)
    if not os.path.exists(game_path):
        print("Incorrect TLauncher version or TL is not installed (404). Download TLauncher 2.921")
        return
    process_name = "java.exe"
    if process_status(process_name) and terminated == False:
        print(f"{process_name} is already running. Terminating the process.")
        for proc in psutil.process_iter():
            if proc.name() == process_name:
                proc.terminate()
                print(f"{process_name} terminated.")
                terminated = True
                time.sleep(1)
                open_game()
    else:
        print(f"{process_name} is not running. Launching...")
        process = subprocess.Popen([game_path])
        winmgr.close_windowr()

# List of modpack URLs
modpack_urls = [
    "https://mediafilez.forgecdn.net/files/4835/191/create-1.20.1-0.5.1.f.jar",
    "https://mediafilez.forgecdn.net/files/5097/798/pamhc2foodcore-1.20.4-1.0.5.jar",
    "https://mediafilez.forgecdn.net/files/5147/171/pamhc2foodextended-1.20.4-1.0.1.jar",
    "https://mediafilez.forgecdn.net/files/4687/624/pamhc2crops-1.20-1.0.3.jar",
    "https://mediafilez.forgecdn.net/files/4625/518/pamhc2trees-1.20-1.0.2.jar",
    "https://mediafilez.forgecdn.net/files/5101/366/jei-1.20.1-forge-15.3.0.4.jar",
    "https://mediafilez.forgecdn.net/files/4962/610/waystones-forge-1.20-14.1.3.jar",
    "https://mediafilez.forgecdn.net/files/4764/804/BiomesOPlenty-1.20.1-18.0.0.598.jar",
    "https://mediafilez.forgecdn.net/files/5140/912/balm-forge-1.20.1-7.2.2.jar",
    "https://mediafilez.forgecdn.net/files/4590/487/TerraBlender-forge-1.20.1-3.0.0.164.jar",
    "https://mediafilez.forgecdn.net/files/5207/967/voicechat-forge-1.20.1-2.5.10.jar"
    # Add more URLs here if needed
]

relative_output_directory = ".minecraft\\mods"
appdata_directory = os.getenv('APPDATA')
output_directory = os.path.join(appdata_directory, relative_output_directory)

if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print("Created directory:", output_directory)

for modpack_url in modpack_urls:
    filename = modpack_url.split("/")[-1]
    if not verify_versions(filename, output_directory):
        if not verified: 
            downloaded_file_path = download_file(modpack_url, output_directory)
            print("File downloaded to:", downloaded_file_path)
    else:
        print(f"File {filename} is already installed.")
