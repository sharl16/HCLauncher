import os
import requests
import shutil
import zipfile
import time

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
    print("Downloading updates..")
    response = requests.get(repo_url + "/archive/main.zip") 
    if response.status_code == 200: # error handling
        with open("temp_repo.zip", "wb") as zip_file:
            zip_file.write(response.content)
        with zipfile.ZipFile("temp_repo.zip", "r") as zip_ref:
            # Extract the entire contents of the ZIP file to the output directory
            zip_ref.extractall(output_dir)
            print("Extracting updates..")
        os.remove("temp_repo.zip")
    else:
        print(f"Failed to download repository: {response.status_code} - {response.reason}")

# Function to execute download_repo() and to apply all the changes
def update_launcher(repo_url):
    script_dir = os.path.dirname(os.path.realpath(__file__)) # to find the real parent
    parent_dir = os.path.dirname(script_dir)
    grandparent_dir = os.path.dirname(parent_dir) # which is the ServerSetup folder in the workspace.
    # Delete the existing Launcher folder if it exists
    print("Clearing up outdated files..")
    existing_launcher_dir = os.path.join(grandparent_dir, "Launcher")
    if os.path.exists(existing_launcher_dir):
        shutil.rmtree(existing_launcher_dir) 

    # download repo
    download_repo(repo_url, grandparent_dir)
    downloaded_launcher_dir = os.path.join(grandparent_dir, "HCLauncher-main", "Launcher")
    print("Verifying update files..")
    print("Patching Launcher..")
    shutil.move(downloaded_launcher_dir, grandparent_dir) # moves Launcher to ServerSetup, or whatever the name of the workspace would be.
    #delete cache
    print("Clearing up..")
    extracted_repo_dir = os.path.join(grandparent_dir, "HCLauncher-main")
    shutil.rmtree(extracted_repo_dir) # deletes extracted zip from the workspace.
    time.sleep(1)
    print("Launcher up to date!")
    print(downloaded_launcher_dir)
    # imports the launcher.py script from the updated launcher directory
    launcher_script_path = os.path.join(grandparent_dir, "Launcher", "py")
    if os.path.exists(launcher_script_path):
        try:
            import sys
            sys.path.append(os.path.join(grandparent_dir, "Launcher", "py")) # self explanatory
            print("Launching..")
            time.sleep(3)
            import launcher
            # Call the desired function from your_script
            launcher.open_game()
        except Exception as e: #error reports. {e} is the error message. this error results when launcher.py cannot be run. Maybe it can be resolved without a new .exe
            print(f"{Colors.CYAN}Report the following errors to developers: {Colors.RESET}")
            print(f"{Colors.RED}(Report this error to developers!) - Error on running launcher.py: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}Upgrader could not finish updating successfully. Download launcher again from Discord {Colors.RESET}")
            print("Terminal exiting in (120)s.")
            time.sleep(120)
    else:
        #error reports. happens when the Launcher directory is not found. Usually requires a new .exe
        print(f"{Colors.RED}Upgrader could not finish updating successfully. Download launcher again from Discord. {Colors.RESET}")
        print("Terminal exiting in (120)s.")
        time.sleep(120)

update_launcher(repo_url="https://github.com/sharl16/HCLauncher")
