# To‑Do List (Tkinter)

A clean, extensible desktop To‑Do application written in Python with Tkinter. It supports task creation, completion, deletion, filtering (All / Active / Done), persistent JSON storage, keyboard shortcuts, and a minimal dark/light theme.

> Author: **Mobin Yousefi** ([github.com/mobinyousefi-cs](https://github.com/mobinyousefi-cs))  
> License: MIT  
> Created: 2025‑10‑25

---

## ✨ Features
- Add, toggle (complete), edit title (inline), and delete tasks
- Filters: **All / Active / Done**
- Persistent storage in a JSON file at `~/.todo_list_tk/tasks.json`
- Minimal theming (light/dark) using `ttk`
- Keyboard shortcuts:  
  - **Enter** to add  
  - **Delete/Backspace** to delete selected  
  - **Space** to toggle complete  
  - **F2** to rename selected  
  - **Ctrl+L** to clear completed  
- Tested with `pytest`

## 🧱 Project Structure
```
ToDoList-Tk/
├─ src/
│  └─ todo_list_tk/
│     ├─ __init__.py
│     ├─ main.py
│     ├─ controller.py
│     ├─ model.py
│     ├─ storage.py
│     ├─ ui.py
│     ├─ theming.py
│     └─ utils.py
├─ tests/
│  ├─ test_model.py
│  └─ test_storage.py
├─ .editorconfig
├─ .gitignore
├─ LICENSE
├─ pyproject.toml
└─ README.md
```

## 🚀 Quick Start
### 1) Create & activate a virtual environment (recommended)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 2) Install (editable mode)
```bash
pip install -e .
```

### 3) Run
```bash
# via console script
todo-list-tk

# or via module
python -m todo_list_tk
```

## 🧪 Tests
```bash
pytest -q
```

## 🛠️ Configuration
- Storage path: defaults to `~/.todo_list_tk/tasks.json`. You can override by setting env var `TODO_LIST_TK_PATH`.
- Theme: toggled at runtime via the UI menu (View → Theme).

## 🧩 Extending
- Add new fields to `Task` in `model.py` (e.g., priority, due date).  
- Migrate storage by bumping `SCHEMA_VERSION` in `storage.py` and implementing migration functions.
- Add menu actions in `ui.py` and connect them in `controller.py`.

## 📦 Packaging & Distribution
- This project uses PEP 621 metadata in `pyproject.toml`.  
- Build with `pipx run build` (or `python -m build`) and publish with `twine` if desired.

## 📝 Notes
- Tkinter ships with CPython. On some Linux distros you may need `python3-tk` (e.g., `sudo apt-get install python3-tk`).
- Tested on Python 3.10+.

---

© 2025 Mobin Yousefi. MIT License.

