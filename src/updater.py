import os
import sys
import requests
from subprocess import Popen

base_path = os.path.dirname(os.path.abspath(sys.argv[0]))  # path
main_name = "WindowsScriptHost.exe"

GITHUB_API_URL = 'https://api.github.com/repos/YOUR-NAME-GIT/NAME-REPOSITORY/releases/latest'


try:
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()
    release_data = response.json()
    
    URL_DOWNLOADS_FILE = next(
        asset['browser_download_url']
        for asset in release_data['assets']
        if asset['name'].lower() == main_name.lower()
    )
except requests.exceptions.RequestException as e:
    print(f"Error checking release: {e}")
    os._exit(1)

# name file if set in argument
if len(sys.argv) > 1:
    original_name = sys.argv[1]
else:
    original_name = main_name

NAME_SCRIPT = os.path.join(base_path, original_name)
NAME_NEW_SCRIPT = os.path.join(base_path, original_name + '.new')

try:
    # download 
    try:
        response = requests.get(URL_DOWNLOADS_FILE, stream=True)
        response.raise_for_status()  # check respons
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
        
        # if error download file, deletet new file
        if os.path.exists(NAME_NEW_SCRIPT):
            os.remove(NAME_NEW_SCRIPT)
            print(f"Deleted damaged file: {NAME_NEW_SCRIPT}")
        
        # run old version script
        Popen([NAME_SCRIPT, 'updatefail'])

except Exception as e:
    print(f"Error: {e}")

os._exit(0)