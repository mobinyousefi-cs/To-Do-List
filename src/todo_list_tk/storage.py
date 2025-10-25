#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: To-Do List (Tkinter)
File: storage.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================

Description:
Persistent JSON storage for tasks with simple schema versioning.

===========================================================================
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, List

from .model import Task

SCHEMA_VERSION = 1

DEFAULT_DIR = Path(os.environ.get("TODO_LIST_TK_HOME", Path.home() / ".todo_list_tk"))
DEFAULT_PATH = Path(os.environ.get("TODO_LIST_TK_PATH", DEFAULT_DIR / "tasks.json"))


def ensure_storage(path: Path = DEFAULT_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps({"version": SCHEMA_VERSION, "tasks": []}, ensure_ascii=False, indent=2), "utf-8")
    return path


def load_tasks(path: Path = DEFAULT_PATH) -> List[Task]:
    ensure_storage(path)
    data = json.loads(path.read_text("utf-8"))
    _ = data.get("version", 1)
    tasks = [Task(**t) for t in data.get("tasks", [])]
    return tasks


def save_tasks(tasks: Iterable[Task], path: Path = DEFAULT_PATH) -> None:
    ensure_storage(path)
    data = {"version": SCHEMA_VERSION, "tasks": [asdict(t) for t in tasks]}
    tmp_path = path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    tmp_path.replace(path)
