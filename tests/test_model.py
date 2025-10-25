#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: To-Do List (Tkinter)
File: tests/test_model.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================
"""
from __future__ import annotations

from todo_list_tk.model import Task


def test_toggle():
    t = Task(id="1", title="x")
    assert t.done is False
    t2 = t.toggle()
    assert t2.done is True


def test_rename():
    t = Task(id="1", title="old")
    t2 = t.rename(" new ")
    assert t2.title == "new"
