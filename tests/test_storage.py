#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: To-Do List (Tkinter)
File: tests/test_storage.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================
"""
from __future__ import annotations

from pathlib import Path

from todo_list_tk.model import Task
from todo_list_tk.storage import ensure_storage, load_tasks, save_tasks


def test_roundtrip(tmp_path: Path):
    path = tmp_path / "tasks.json"
    ensure_storage(path)
    tasks = [Task(id="1", title="Alpha"), Task(id="2", title="Beta", done=True)]
    save_tasks(tasks, path)
    loaded = load_tasks(path)
    assert [t.title for t in loaded] == ["Alpha", "Beta"]
    assert loaded[1].done is True
