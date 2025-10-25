#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: To-Do List (Tkinter)
File: theming.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================

Description:
Minimal ttk theme setup with light & dark variants.

===========================================================================
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class Theme(str):
    LIGHT = "light"
    DARK = "dark"


def setup_theme(root: tk.Tk, initial: str = Theme.LIGHT) -> str:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # Base styles
    style.configure("TLabel", padding=2)
    style.configure("TButton", padding=6)
    style.configure("TEntry", padding=4)
    style.configure("TMenubutton", padding=6)

    apply_theme(style, initial)
    return initial


def apply_theme(style: ttk.Style, variant: str) -> None:
    if variant == Theme.DARK:
        bg = "#202225"
        fg = "#e6e6e6"
        acc = "#4f46e5"
        style.configure(".", background=bg, foreground=fg)
        style.map("TButton", background=[("active", acc)])
        style.configure("Task.TFrame", background=bg)
    else:
        bg = "#ffffff"
        fg = "#222222"
        acc = "#2563eb"
        style.configure(".", background=bg, foreground=fg)
        style.map("TButton", background=[("active", acc)])
        style.configure("Task.TFrame", background=bg)
