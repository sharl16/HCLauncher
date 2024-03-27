import requests
import os

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
    "https://mediafilez.forgecdn.net/files/4590/487/TerraBlender-forge-1.20.1-3.0.0.164.jar"
    # Add more URLs here if needed
]

# Specify the relative path to the Minecraft mods directory
relative_output_directory = ".minecraft\\mods"

# Get the user's AppData directory and create the full output directory path
appdata_directory = os.getenv('APPDATA')
output_directory = os.path.join(appdata_directory, relative_output_directory)

# Ensure the output directory exists, create if it doesn't
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Download each modpack in the list to the output directory
for modpack_url in modpack_urls:
    downloaded_file_path = download_file(modpack_url, output_directory)
    print("File downloaded to:", downloaded_file_path)
