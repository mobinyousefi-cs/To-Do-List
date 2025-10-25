#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: To-Do List (Tkinter)
File: model.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================

Description:
Domain model entities for the To‑Do List app.

===========================================================================
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import Optional


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class Task:
    id: str
    title: str
    done: bool = False
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds"))
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds"))
    priority: Priority = Priority.MEDIUM
    due: Optional[str] = None  # ISO date string

    def toggle(self) -> "Task":
        return replace(self, done=not self.done, updated_at=datetime.utcnow().isoformat(timespec="seconds"))

    def rename(self, new_title: str) -> "Task":
        new_title = new_title.strip()
        if not new_title:
            raise ValueError("Title cannot be empty")
        return replace(self, title=new_title, updated_at=datetime.utcnow().isoformat(timespec="seconds"))

    def set_priority(self, p: Priority) -> "Task":
        return replace(self, priority=p, updated_at=datetime.utcnow().isoformat(timespec="seconds"))
