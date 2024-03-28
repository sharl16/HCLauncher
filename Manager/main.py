import sys
import asyncio
import time

# Add the directory containing the modules you want to import to sys.path
sys.path.append('Upgrader/py')
sys.path.append('Launcher/py')

# Now you can import the modules
import upgrader
import launcher

async def main():
    print("Checking for updates..")
    repo_url = "https://github.com/sharl16/HCLauncher"   
    # Acquire the semaphore to ensure exclusive access
    upgrader.update_launcher(repo_url)
    launcher.open_game()

asyncio.run(main())
