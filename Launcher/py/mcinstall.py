import os

appdata_directory = os.getenv('APPDATA')
tlproperties = r".tlauncher\tlauncher-2.0.properties"  
tlconfig = os.path.join(appdata_directory, tlproperties)

def verifyMCVersion(version):
    found_key = False
    with open(tlconfig, "r") as file: 
        lines = file.readlines()
    with open(tlconfig, "w") as file:
        for line in lines:
            if line.strip() == "" or line.strip().startswith("#"):
                file.write(line)
                continue
            key, value = line.strip().split("=") 
            key = key.strip()
            if key == "login.version.game":
                found_key = True
                file.write(f"{key}={version}\n")
                print(f"Login Version Game updated to: {version}")
            else:
                file.write(line)
        if not found_key:
            file.write(f"login.version.game={version}\n")
            print(f"New key 'login.version.game' added with value: {version}")