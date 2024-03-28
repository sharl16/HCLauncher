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

def download_repo(repo_url, output_dir):
    print("Downloading updates..")
    response = requests.get(repo_url + "/archive/main.zip")
    if response.status_code == 200:
        with open("temp_repo.zip", "wb") as zip_file:
            zip_file.write(response.content)
        with zipfile.ZipFile("temp_repo.zip", "r") as zip_ref:
            # Extract the entire contents of the ZIP file to the output directory
            zip_ref.extractall(output_dir)
            print("Extracting updates..")
        os.remove("temp_repo.zip")
    else:
        print(f"Failed to download repository: {response.status_code} - {response.reason}")

def update_launcher(repo_url):
    # Identify the parent directory of the script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(script_dir)
    grandparent_dir = os.path.dirname(parent_dir)

    # Delete the existing "Launcher" folder if it exists
    print("Clearing up outdated files..")
    existing_launcher_dir = os.path.join(grandparent_dir, "Launcher")
    if os.path.exists(existing_launcher_dir):
        shutil.rmtree(existing_launcher_dir)

    # Download and extract the repository
    download_repo(repo_url, grandparent_dir)

    # Identify the downloaded "Launcher" folder
    downloaded_launcher_dir = os.path.join(grandparent_dir, "HCLauncher-main", "Launcher")
    print("Verifying update files..")

    # Move the downloaded "Launcher" folder to the parent directory
    print("Patching Launcher..")
    shutil.move(downloaded_launcher_dir, grandparent_dir)

    # Delete the extracted repository directory
    print("Clearing up..")
    extracted_repo_dir = os.path.join(grandparent_dir, "HCLauncher-main")
    shutil.rmtree(extracted_repo_dir)
    time.sleep(1)
    print("Launcher up to date!")
    print(downloaded_launcher_dir)

    # Import and run a function from a script in Launcher/py directory
    launcher_script_path = os.path.join(grandparent_dir, "Launcher", "py")
    if os.path.exists(launcher_script_path):
        try:
            import sys
            sys.path.append(os.path.join(grandparent_dir, "Launcher", "py"))
            print("Launching..")
            time.sleep(3)
            import launcher

            # Call the desired function from your_script
            launcher.open_game()
        except Exception as e:
            print(f"{Colors.CYAN}Report the following errors to developers: {Colors.RESET}")
            print(f"{Colors.RED}(Report this error to developers!) - Error on running launcher.py: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}Upgrader could not finish updating successfully. Download launcher again from Discord. {Colors.RESET}")
            print("Terminal exiting in (120)s.")
            time.sleep(120)
    else:
        print(f"{Colors.RED}Upgrader could not finish updating successfully. Download launcher again from Discord. {Colors.RESET}")
        print("Terminal exiting in (120)s.")
        time.sleep(120)

update_launcher(repo_url="https://github.com/sharl16/HCLauncher")
