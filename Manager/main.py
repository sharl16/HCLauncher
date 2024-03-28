import sys
import asyncio
import time

# Add the directory containing the modules you want to import to sys.path
sys.path.append('Upgrader/py')
sys.path.append('Launcher/py')

# Now you can import the modules
import upgrader
import launcher

async def check_for_updates():
    print("Checking for updates..")
    repo_url = "https://github.com/sharl16/HCLauncher"
    await upgrader.update_launcher(repo_url)

async def main():
    await check_for_updates()  # Wait for check_for_updates coroutine to finish
    print("Launching..")
    time.sleep(5)
    launcher.open_game()

asyncio.run(main())
