import sys
import asyncio

# Add the directory containing the modules you want to import to sys.path
sys.path.append('Upgrader/py')
sys.path.append('Launcher/py')

# Now you can import the modules
from Upgrader.py import upgrader
from Launcher.py import launcher


async def main():
    print("Checking for updates..")
    repo_url = "https://github.com/sharl16/HCLauncher"   
    # Call the update_launcher function from upgrader module
    upgrader.update_launcher(repo_url)
    launcher.open_game()

asyncio.run(main())
