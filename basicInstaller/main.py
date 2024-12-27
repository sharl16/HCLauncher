import os
import requests
import time
import sys

def download_file(url, output_directory):
    filename = url.split("/")[-1]
    output_path = os.path.join(output_directory, filename)
    try:
        with requests.get(url, stream=True) as req:
            req.raise_for_status()  
            with open(output_path, 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        return output_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def verify_versions(filename, output_directory):
    mcdir = ".minecraft"
    mcversion = os.path.join(os.getenv('APPDATA'), mcdir)
    filepath = os.path.join(output_directory, filename)
    
    if os.path.exists(mcversion) and os.path.exists(filepath):
        return True
    elif not os.path.exists(mcversion):
        print("Minecraft directory does not exist.")
    return False

modpack_urls = [
    "https://mediafilez.forgecdn.net/files/5773/34/BiomesOPlenty-fabric-1.20.1-19.0.0.91.jar",
    "https://mediafilez.forgecdn.net/files/4765/724/lithium-fabric-mc1.20.1-0.11.2.jar",
    "https://mediafilez.forgecdn.net/files/5485/654/sodium-fabric-0.5.11%2Bmc1.20.1.jar",
    "https://mediafilez.forgecdn.net/files/4997/461/Croptopia-1.20.1-FABRIC-3.0.4.jar",
    "https://mediafilez.forgecdn.net/files/5862/237/Xaeros_Minimap_24.6.1_Fabric_1.20.jar",
    "https://mediafilez.forgecdn.net/files/4607/122/universal_shops-1.3.2%2B1.20.1.jar",
    "https://mediafilez.forgecdn.net/files/5383/715/fabric-api-0.92.2%2B1.20.1.jar",
    "https://mediafilez.forgecdn.net/files/5378/181/TerraBlender-fabric-1.20.1-3.0.1.7.jar",
    "https://mediafilez.forgecdn.net/files/5594/996/Botania-1.20.1-446-FABRIC.jar",
    "https://mediafilez.forgecdn.net/files/4966/124/Patchouli-1.20.1-84-FABRIC.jar",
    "https://mediafilez.forgecdn.net/files/5173/501/trinkets-3.7.2.jar",
    "https://mediafilez.forgecdn.net/files/5982/726/create-fabric-0.5.1-j-build.1631%2Bmc1.20.1.jar",
    "https://mediafilez.forgecdn.net/files/5815/864/ToughAsNails-fabric-1.20.1-9.2.0.171.jar",
    "https://mediafilez.forgecdn.net/files/5907/373/voicechat-fabric-1.20.1-2.5.26.jar",
    "https://mediafilez.forgecdn.net/files/5787/838/GlitchCore-fabric-1.20.1-0.0.1.1.jar",
    "https://mediafilez.forgecdn.net/files/5493/195/indium-1.0.34%2Bmc1.20.1.jar",
    "https://mediafilez.forgecdn.net/files/4949/797/EpheroLib-1.20.1-FABRIC-1.2.0.jar"
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
        downloaded_file_path = download_file(modpack_url, output_directory)
        if downloaded_file_path:
            print(f"File downloaded to: {downloaded_file_path}")
    else:
        print(f"File {filename} is already installed.")