#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: To-Do List (Tkinter)
File: controller.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================

Description:
Application controller mediating between UI and storage/model.

===========================================================================
"""
from __future__ import annotations

from typing import List

from .model import Task, Priority
from .storage import load_tasks, save_tasks
from .utils import new_id


class Controller:
    def __init__(self) -> None:
        self.tasks: List[Task] = load_tasks()

    # --- CRUD ---
    def add_task(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty")
        t = Task(id=new_id(), title=title)
        self.tasks.append(t)
        save_tasks(self.tasks)
        return t

    def toggle_task(self, task_id: str) -> Task:
        idx = self._index(task_id)
        self.tasks[idx] = self.tasks[idx].toggle()
        save_tasks(self.tasks)
        return self.tasks[idx]

    def rename_task(self, task_id: str, new_title: str) -> Task:
        idx = self._index(task_id)
        self.tasks[idx] = self.tasks[idx].rename(new_title)
        save_tasks(self.tasks)
        return self.tasks[idx]

    def delete_task(self, task_id: str) -> None:
        idx = self._index(task_id)
        del self.tasks[idx]
        save_tasks(self.tasks)

    def clear_completed(self) -> int:
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.done]
        save_tasks(self.tasks)
        return before - len(self.tasks)

    def set_priority(self, task_id: str, p: Priority) -> Task:
        idx = self._index(task_id)
        self.tasks[idx] = self.tasks[idx].set_priority(p)
        save_tasks(self.tasks)
        return self.tasks[idx]

    # --- helpers ---
    def _index(self, task_id: str) -> int:
        for i, t in enumerate(self.tasks):
            if t.id == task_id:
                return i
        raise KeyError(task_id)
