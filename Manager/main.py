import sys
import asyncio
import time

# Add the directory containing the modules you want to import to sys.path
sys.path.append('Upgrader/py')
sys.path.append('Launcher/py')

# Now you can import the modules
import upgrader
import launcher

update_semaphore = asyncio.Semaphore(1)

async def main():
    print("Checking for updates..")
    repo_url = "https://github.com/sharl16/HCLauncher"   
    # Acquire the semaphore to ensure exclusive access
    async with update_semaphore:
        await upgrader.update_launcher(repo_url)

#asyncio.run(main())
