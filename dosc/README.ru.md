# 🔄 Авто-обновлятор

Этот Python-скрипт предназначен для автоматического обновления EXE-файла с GitHub. Он идеально подходит для проектов, где требуется функция автообновления.

---

## 📋 Возможности скрипта

1. Получение ссылки на последний релиз с GitHub.
2. Поиск нужного файла по имени (например, `WindowsScriptHost.exe`).
3. Загрузка файла с временным расширением `.exe.new`.
4. Удаление старой версии EXE (если загрузка прошла успешно).
5. Переименование загруженного файла в основной.
6. Запуск обновлённого EXE.
7. Обработка ошибок:
    - Удаление `.new`-файла при ошибке.
    - Запуск старой версии с аргументом `updatefail`.
8. Поддержка аргументов `updated` и `updatefail`.

Пример обработки аргументов:

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

## 📁 Структура скрипта

1. **base_path**: путь к текущей директории скрипта.
2. **main_name**: имя файла, который нужно обновить.

```python
base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
main_name = "WindowsScriptHost.exe"
```

3. **API GitHub** для получения информации о последнем релизе:

```python
GITHUB_API_URL = 'https://api.github.com/repos/Имя-На-Гитхабе/Имя-Репозитория/releases/latest'
```

4. Возможность передать имя файла через аргумент командной строки:

```python
if len(sys.argv) > 1:
     original_name = sys.argv[1]
else:
     original_name = main_name
```

5. Пути к файлам:
    - **NAME_SCRIPT**: текущая версия EXE.
    - **NAME_NEW_SCRIPT**: новая скачиваемая версия.

```python
NAME_SCRIPT = os.path.join(base_path, original_name)
NAME_NEW_SCRIPT = os.path.join(base_path, original_name + '.new')
```

---

## 🚀 Как запустить

### Обычный запуск (по умолчанию)
```bash
python updater.py
```

### С указанием имени EXE-файла
```bash
python updater.py CustomName.exe
```

---

## 🔍 Пошаговая работа скрипта

1. **Проверка последнего релиза**  
    Используется `requests.get()` для обращения к GitHub API.

2. **Поиск нужного файла в релизе**  
    Скрипт ищет asset, имя которого совпадает с `WindowsScriptHost.exe` или указанным аргументом.

3. **Загрузка файла**  
    Скачивается по `browser_download_url` и сохраняется с расширением `.new`.

4. **Удаление старого EXE**  
    Проверяется наличие старого файла, и он удаляется.

5. **Переименование `.new` → оригинальное имя**  
    Новый файл переименовывается в имя оригинала.

6. **Запуск обновлённого файла**  
    Выполняется через `subprocess.Popen([NAME_SCRIPT, 'updated'])`.

7. **Обработка ошибок**  
    Если произошла ошибка:
    - Удаляется `.new`.
    - Запускается старая версия EXE с аргументом `updatefail`.

--- 

Этот скрипт упрощает процесс обновления и обеспечивает стабильность работы вашего приложения.