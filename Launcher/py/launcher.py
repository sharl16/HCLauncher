import os
import requests
import subprocess
import psutil
import time
import win32gui
import win32con
import sys
sys.path.append('Launcher/py')
import mcinstall
import pyautogui
import importlib

class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'


def verify_exe(pkgname):
    try:
        pkgmodule = importlib.import_module(pkgname)
        print("Executable up to date!")
        return pkgmodule
    except ImportError:
        print(f"{Colors.RED}Outdated exe! Download launcher from Discord (<2.3). {pkgname} was not found.{Colors.RESET}")
        time.sleep(1)
        print(f"{Colors.YELLOW}Gathering launcher information:{Colors.RESET}")
        time.sleep(2)
        print("Version: 2.2")
        print("Last updated: 31/3/2024")
        print("Vendor CPU: AuthenticAMD")
        print("Driver version: 24.3.1")
        print(f"{Colors.BLUE}Closing in 120s..{Colors.RESET}")
        time.sleep(120)
        raise SystemExit(f"Halting code execution..")

version = "ForgeOptiFine 1.20.1" # can be updated and changed
mcinstall.verifyMCVersion(version)

verified = False
appdata_directory = os.getenv('APPDATA')

def download_file(url, output_directory):
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
    global verified  # Declare 'verified' as a global variable
    mcdir = ".minecraft\\versions\\ForgeOptiFine 1.20.1"
    mcversion = os.path.join(os.getenv('APPDATA'), mcdir)

    # Check if the Minecraft version directory exists
    if os.path.exists(mcversion):
        # If it exists, continue to check if the specified file exists
        filepath = os.path.join(output_directory, filename)
        if os.path.exists(filepath):
            verified = True
    else:
        # If the Minecraft version directory does not exist, return False
        verified = False
        print("Minecraft directory does not exist.")
        return False

def wait_for_tlauncher(window_title, timeout=30):
    start_time = time.time()
    while True:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd != 0:
            return hwnd
        elif time.time() - start_time > timeout:
            return None
        time.sleep(1)

def set_window_position(hwnd, x, y):
    win32gui.SetWindowPos(hwnd, None, x, y, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)

def process_status(process_name):
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return True
    return False


def open_game():
    terminated = False
    appdata_directory = os.getenv('APPDATA')
    game_dir = ".minecraft\\TLauncher.exe"
    game_path = os.path.join(appdata_directory, game_dir)
    if not os.path.exists(game_path):
        print("Incorrect TLauncher version or TL is not installed (404). Download TLauncher 2.899")
        return

    process_name = "javaw.exe"
    if process_status(process_name):
        print(f"{process_name} is already running. Terminating the process.")
        for proc in psutil.process_iter():
            if proc.name() == process_name:
                proc.terminate()
                print(f"{process_name} terminated.")
                terminated = True
                time.sleep
                open_game()
    else:
        print(f"{process_name} is not running. Launching...")
        process = subprocess.Popen([game_path])
        # Wait for the window to appear
        hwnd = wait_for_tlauncher("TLauncher 2.919", timeout=30)
        if hwnd:
            print("Injected to TL Window")
            # Set initial window position to a fixed location (e.g., top-left corner)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
            # Continuously set window position every second
            loop = 0
            while True:
                loop += 1
                cursorX = 632
                cursorY = 647
                #pyautogui.click(cursorX, cursorY)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
                time.sleep(0.1)
                print(loop)
                if loop == 2:
                     break
        else:
            print("Could not inject to TLauncher window within the timeout period.")
   



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

# Specify the relative path to the Minecraft mods directory
relative_output_directory = ".minecraft\\mods"

# Get the user's AppData directory
appdata_directory = os.getenv('APPDATA')

# Create the full output directory path
output_directory = os.path.join(appdata_directory, relative_output_directory)

# Ensure the output directory exists, create if it doesn't
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print("Created directory:", output_directory)

# Download or check each modpack in the list
for modpack_url in modpack_urls:
    filename = modpack_url.split("/")[-1]
    if not verify_versions(filename, output_directory):
        if not verified:  # No need to check `verified == False`, can directly use `not verified`
            downloaded_file_path = download_file(modpack_url, output_directory)
            print("File downloaded to:", downloaded_file_path)
    else:
        print(f"File {filename} is already installed.")