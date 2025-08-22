import os
import sys
import requests
from subprocess import Popen

base_path = os.path.dirname(os.path.abspath(sys.argv[0]))  # path

REPOS = {
    "PCGuardControl": "Farmerok/Telegram-Remote-Control-PC",
    "BinDrop": "Farmerok/BinDrop",
}

if len(sys.argv) > 1 and sys.argv[1] in REPOS:
    repo_key = sys.argv[1]
    repo_name = REPOS[repo_key]
    print(f"Updating from repo: {repo_name}")
else:
    print("No valid repo argument, exiting")
    os._exit(1)

GITHUB_API_URL = f'https://api.github.com/repos/{repo_name}/releases/latest'

try:
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()
    release_data = response.json()

    asset = release_data['assets'][0]
    URL_DOWNLOADS_FILE = asset['browser_download_url']
    release_file_name = asset['name'] 
except requests.exceptions.RequestException as e:
    print(f"Error checking release: {e}")
    os._exit(1)
except IndexError:
    print("No assets found in the release")
    os._exit(1)

if len(sys.argv) > 2:
    original_name = sys.argv[2]
else:
    original_name = release_file_name

NAME_SCRIPT = os.path.join(base_path, original_name)
NAME_NEW_SCRIPT = os.path.join(base_path, original_name + '.new')

try:
    # download 
    try:
        response = requests.get(URL_DOWNLOADS_FILE, stream=True)
        response.raise_for_status()
        with open(NAME_NEW_SCRIPT, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded new file: {NAME_NEW_SCRIPT}")

        # delete old file
        if os.path.exists(NAME_SCRIPT):
            os.remove(NAME_SCRIPT)
            print(f"Deleted old file: {NAME_SCRIPT}")

        # rename new file
        os.rename(NAME_NEW_SCRIPT, NAME_SCRIPT)
        print(f"Renamed {NAME_NEW_SCRIPT} to {NAME_SCRIPT}")

        # run updated script
        Popen([NAME_SCRIPT, 'updated'])

    except requests.exceptions.RequestException as e:
        print(f"Error downloading or running {NAME_NEW_SCRIPT}: {e}")
        if os.path.exists(NAME_NEW_SCRIPT):
            os.remove(NAME_NEW_SCRIPT)
            print(f"Deleted damaged file: {NAME_NEW_SCRIPT}")
        # run old version script
        if os.path.exists(NAME_SCRIPT):
            Popen([NAME_SCRIPT, 'updatefail'])

except Exception as e:
    print(f"Error: {e}")

os._exit(0)
