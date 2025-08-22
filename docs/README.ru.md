# 🔄 Авто-обновлятор

Этот Python-скрипт предназначен для автоматического обновления EXE-файлов из указанных репозиториев на GitHub. Он идеально подходит для проектов, где требуется функция автообновления с поддержкой выбора репозитория.

---

## 📋 Возможности скрипта

1. **Поддержка нескольких репозиториев**:  
   Выбор репозитория для обновления через аргумент командной строки (например, `PCGuardControl` или `BinDrop`).
2. **Получение последнего релиза**:  
   Использует GitHub API для получения информации о последнем релизе из указанного репозитория.
3. **Поиск и загрузка файла**:  
   - Автоматически определяет имя файла из релиза или использует имя, переданное через аргумент.
   - Загружает файл с временным расширением `.exe.new`.
4. **Обновление файла**:  
   - Удаляет старую версию EXE (если она существует).  
   - Переименовывает загруженный файл в оригинальное имя.  
   - Запускает обновлённый EXE с аргументом `updated`.
5. **Обработка ошибок**:  
   - При ошибке загрузки удаляет `.new`-файл.  
   - Запускает старую версию EXE с аргументом `updatefail`.  
6. **Гибкость аргументов**:  
   Поддерживает передачу имени репозитория и имени файла через аргументы командной строки.

Пример обработки аргументов:

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

## 📁 Структура скрипта

1. **base_path**:  
   Путь к текущей директории скрипта.

   ```python
   base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
   ```

2. **REPOS**:  
   Словарь с поддерживаемыми репозиториями.

   ```python
   REPOS = {
       "PCGuardControl": "Farmerok/Telegram-Remote-Control-PC",
       "BinDrop": "Farmerok/BinDrop",
   }
   ```

3. **GitHub API**:  
   Формирование URL для получения информации о последнем релизе.

   ```python
   GITHUB_API_URL = f'https://api.github.com/repos/{repo_name}/releases/latest'
   ```

4. **Обработка имени файла**:  
   Имя файла определяется из релиза или передаётся через аргумент.

   ```python
   if len(sys.argv) > 2:
       original_name = sys.argv[2]
   else:
       original_name = release_file_name
   ```

5. **Пути к файлам**:  
   - **NAME_SCRIPT**: текущая версия EXE.  
   - **NAME_NEW_SCRIPT**: новая скачиваемая версия.

   ```python
   NAME_SCRIPT = os.path.join(base_path, original_name)
   NAME_NEW_SCRIPT = os.path.join(base_path, original_name + '.new')
   ```

---

## 🚀 Как запустить

### Обычный запуск (с указанием репозитория)
```bash
python updater.py PCGuardControl
```

### С указанием репозитория и имени EXE-файла
```bash
python updater.py PCGuardControl CustomName.exe
```

---

## 🔍 Пошаговая работа скрипта

1. **Проверка аргументов**:  
   Проверяется, передан ли валидный ключ репозитория (`PCGuardControl`, `BinDrop`). Если нет — завершает работу.

2. **Получение данных о релизе**:  
   Используется `requests.get()` для обращения к GitHub API и получения информации о последнем релизе.

3. **Определение файла**:  
   Имя файла берётся из первого asset релиза или из аргумента командной строки.

4. **Загрузка файла**:  
   Файл скачивается по `browser_download_url` и сохраняется с расширением `.new`.

5. **Удаление старого файла**:  
   Если старая версия EXE существует, она удаляется.

6. **Переименование файла**:  
   Новый файл переименовывается в оригинальное имя.

7. **Запуск обновлённого файла**:  
   Выполняется через `subprocess.Popen([NAME_SCRIPT, 'updated'])`.

8. **Обработка ошибок**:  
   При любой ошибке:  
   - Удаляется `.new`-файл (если он был создан).  
   - Запускается старая версия EXE с аргументом `updatefail`.  
   - Скрипт завершает работу с кодом `0`.

---

## 🛠️ Пример кода обработки ошибок

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

Этот скрипт обеспечивает гибкое и надёжное обновление EXE-файлов из нескольких репозиториев, минимизируя риски сбоев и упрощая процесс обновления.