
# 📋 Script Features

1. Fetching the latest release link from GitHub.
2. Searching for the required file by name (e.g., `WindowsScriptHost.exe`).
3. Downloading the file with a temporary `.exe.new` extension.
4. Deleting the old EXE version (if the download is successful).
5. Renaming the downloaded file to the main file.
6. Launching the updated EXE.
7. Error handling:
    - Deleting the `.new` file in case of an error.
    - Launching the old version with the `updatefail` argument.
8. Support for `updated` and `updatefail` arguments.

Example of argument handling:

```python
def checkArgs(message):
     try:
          if sys_argv[1] in ['updated', 'updatefail']:
                msg = '✅ Script updated' if sys_argv[1] == 'updated' else '🚫 Error script updated'
                bot.send_message(message.chat.id, msg)
                
                file_path = checkPathToFile(nameUPDfile)
                if os.path.exists(file_path):
                     os.remove(file_path)
     except Exception:
          pass
```

---

## 📁 Script Structure

1. **base_path**: path to the script's current directory.
2. **main_name**: name of the file to be updated.

```python
base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
main_name = "WindowsScriptHost.exe"
```

3. **GitHub API** for fetching the latest release information:

```python
GITHUB_API_URL = 'https://api.github.com/repos/YOURNAMEGIT/NAMEREPOSITORY/releases/latest'
```

4. Ability to pass the file name via a command-line argument:

```python
if len(sys.argv) > 1:
     original_name = sys.argv[1]
else:
     original_name = main_name
```

5. File paths:
    - **NAME_SCRIPT**: current version of the EXE.
    - **NAME_NEW_SCRIPT**: new downloaded version.

```python
NAME_SCRIPT = os.path.join(base_path, original_name)
NAME_NEW_SCRIPT = os.path.join(base_path, original_name + '.new')
```

---

## 🚀 How to Run

### Default Run
```bash
python updater.py
```

### Specifying the EXE File Name
```bash
python updater.py CustomName.exe
```

---

## 🔍 Step-by-Step Script Workflow

1. **Check the Latest Release**  
    Uses `requests.get()` to query the GitHub API.

2. **Search for the Required File in the Release**  
    The script searches for an asset whose name matches `WindowsScriptHost.exe` or the specified argument.

3. **Download the File**  
    Downloads the file using `browser_download_url` and saves it with a `.new` extension.

4. **Delete the Old EXE**  
    Checks for the existence of the old file and deletes it.

5. **Rename `.new` → Original Name**  
    Renames the new file to the original name.

6. **Launch the Updated File**  
    Executes the updated file using `subprocess.Popen([NAME_SCRIPT, 'updated'])`.

7. **Error Handling**  
    If an error occurs:
    - Deletes the `.new` file.
    - Launches the old EXE version with the `updatefail` argument.

---

This script simplifies the update process and ensures the stability of your application.