import os
import requests
import shutil
import zipfile

def download_repo(repo_url, output_dir):
    response = requests.get(repo_url + "/archive/main.zip")
    with open("temp_repo.zip", "wb") as zip_file:
        zip_file.write(response.content)
    with zipfile.ZipFile("temp_repo.zip", "r") as zip_ref:
        # Extract the 'Launcher' folder from the ZIP file to the output directory
        zip_ref.extract("HCLauncher-main/Launcher", output_dir)
    os.remove("temp_repo.zip")

def update_launcher(repo_url):
    download_repo(repo_url, "temp_repo")
    # Move the entire 'Launcher' folder to the 'Setup' folder
    src_dir = os.path.join("temp_repo", "HCLauncher-main", "Launcher")  # Source directory
    dest_dir = "Launcher"  # Destination directory
    shutil.move(src_dir, dest_dir)  # Move the folder to the Setup directory
    shutil.rmtree("temp_repo")

if __name__ == "__main__":
    # URL of the GitHub repository
    repo_url = "https://github.com/sharl16/HCLauncher"
    update_launcher(repo_url)
