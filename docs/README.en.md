# 🔄 Auto-Updater

This Python script is designed to automatically update EXE files from specified GitHub repositories. It is ideal for projects requiring an auto-update feature with repository selection.

---

## 📋 Script Features

1. **Support for Multiple Repositories**:  
   Selects a repository for updating via command-line argument (e.g., `PCGuardControl` or `BinDrop`).  
2. **Fetching the Latest Release**:  
   Uses the GitHub API to retrieve information about the latest release from the specified repository.  
3. **File Detection and Download**:  
   - Automatically determines the file name from the release or uses a name provided via argument.  
   - Downloads the file with a temporary `.exe.new` extension.  
4. **File Update Process**:  
   - Deletes the old EXE version (if it exists).  
   - Renames the downloaded file to the original name.  
   - Launches the updated EXE with the `updated` argument.  
5. **Error Handling**:  
   - Deletes the `.new` file in case of download errors.  
   - Launches the old EXE version with the `updatefail` argument.  
6. **Flexible Arguments**:  
   Supports passing the repository key and file name via command-line arguments.

Example of argument handling:

```python
if len(sys.argv) > 1 and sys.argv[1] in REPOS:
    repo_key = sys.argv[1]
    repo_name = REPOS[repo_key]
    print(f"Updating from repo: {repo_name}")
else:
    print("No valid repo argument, exiting")
    os._exit(1)
```

---

## 📁 Script Structure

1. **base_path**:  
   Path to the script's current directory.

   ```python
   base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
   ```

2. **REPOS**:  
   Dictionary of supported repositories.

   ```python
   REPOS = {
       "PCGuardControl": "Farmerok/Telegram-Remote-Control-PC",
       "BinDrop": "Farmerok/BinDrop",
   }
   ```

3. **GitHub API**:  
   Constructs the URL to fetch the latest release information.

   ```python
   GITHUB_API_URL = f'https://api.github.com/repos/{repo_name}/releases/latest'
   ```

4. **File Name Handling**:  
   File name is determined from the release or provided via argument.

   ```python
   if len(sys.argv) > 2:
       original_name = sys.argv[2]
   else:
       original_name = release_file_name
   ```

5. **File Paths**:  
   - **NAME_SCRIPT**: Current EXE version.  
   - **NAME_NEW_SCRIPT**: Newly downloaded version.

   ```python
   NAME_SCRIPT = os.path.join(base_path, original_name)
   NAME_NEW_SCRIPT = os.path.join(base_path, original_name + '.new')
   ```

---

## 🚀 How to Run

### Standard Run (with repository specified)
```bash
python updater.py PCGuardControl
```

### With Repository and Custom EXE Name
```bash
python updater.py PCGuardControl CustomName.exe
```

---

## 🔍 Step-by-Step Workflow

1. **Argument Validation**:  
   Checks if a valid repository key (`PCGuardControl`, `BinDrop`) is provided. Exits if invalid.

2. **Fetching Release Data**:  
   Uses `requests.get()` to query the GitHub API for the latest release.

3. **File Identification**:  
   Determines the file name from the first asset in the release or from the command-line argument.

4. **File Download**:  
   Downloads the file via `browser_download_url` and saves it with a `.new` extension.

5. **Removing Old File**:  
   Deletes the existing EXE file, if present.

6. **Renaming New File**:  
   Renames the downloaded file to the original name.

7. **Launching Updated File**:  
   Executes the updated file using `subprocess.Popen([NAME_SCRIPT, 'updated'])`.

8. **Error Handling**:  
   In case of errors:  
   - Deletes the `.new` file (if created).  
   - Launches the old EXE version with the `updatefail` argument.  
   - Exits with code `0`.

---

## 🛠️ Example Error Handling Code

```python
try:
    response = requests.get(URL_DOWNLOADS_FILE, stream=True)
    response.raise_for_status()
    with open(NAME_NEW_SCRIPT, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
except requests.exceptions.RequestException as e:
    print(f"Error downloading or running {NAME_NEW_SCRIPT}: {e}")
    if os.path.exists(NAME_NEW_SCRIPT):
        os.remove(NAME_NEW_SCRIPT)
        print(f"Deleted damaged file: {NAME_NEW_SCRIPT}")
    if os.path.exists(NAME_SCRIPT):
        Popen([NAME_SCRIPT, 'updatefail'])
```

---

This script provides a flexible and reliable way to update EXE files from multiple repositories, minimizing risks of failures and simplifying the update process.