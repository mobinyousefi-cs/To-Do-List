#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: To-Do List (Tkinter)
File: ui.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================

Description:
Tkinter UI for the To‑Do List application.

===========================================================================
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from typing import Dict, List, Literal, Optional

from .controller import Controller
from .model import Task, Priority
from .theming import setup_theme, apply_theme, Theme

Filter = Literal["all", "active", "done"]


class App(ttk.Frame):
    def __init__(self, master: tk.Tk | tk.Toplevel | None = None) -> None:
        self.root = master or tk.Tk()
        super().__init__(self.root, padding=10, style="Task.TFrame")
        self.root.title("To‑Do List — Tkinter")
        self.controller = Controller()
        self.filter: Filter = "all"
        self.theme = setup_theme(self.root, Theme.LIGHT)
        self._task_widgets: Dict[str, ttk.Checkbutton] = {}

        self._build_menu()
        self._build_header()
        self._build_list()
        self._build_footer()
        self._bind_keys()
        self.pack(fill="both", expand=True)
        self.refresh()

    # --- UI ---
    def _build_menu(self) -> None:
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.destroy, accelerator="Alt+F4")
        menubar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Light Theme", command=lambda: apply_theme(ttk.Style(self.root), Theme.LIGHT))
        view_menu.add_command(label="Dark Theme", command=lambda: apply_theme(ttk.Style(self.root), Theme.DARK))
        menubar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def _build_header(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))

        self.entry = ttk.Entry(header)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.focus_set()

        add_btn = ttk.Button(header, text="Add", command=self._on_add)
        add_btn.pack(side="left", padx=(8, 0))

        # Filters
        filters = ttk.Frame(header)
        filters.pack(side="right")
        for name in ["all", "active", "done"]:
            b = ttk.Radiobutton(filters, text=name.capitalize(), value=name, command=lambda n=name: self._set_filter(n))
            b.configure(variable=tk.StringVar(value=self.filter))
            # We manage filter state manually in _set_filter

    def _build_list(self) -> None:
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.list_frame = ttk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

        self.canvas_window = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.list_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _build_footer(self) -> None:
        footer = ttk.Frame(self)
        footer.pack(fill="x", pady=(10, 0))

        self.stats_label = ttk.Label(footer, text="0 items")
        self.stats_label.pack(side="left")

        clear_btn = ttk.Button(footer, text="Clear Completed", command=self._on_clear_completed)
        clear_btn.pack(side="right")

    # --- events ---
    def _bind_keys(self) -> None:
        self.root.bind("<Return>", lambda e: self._on_add())
        self.root.bind("<KP_Enter>", lambda e: self._on_add())
        self.root.bind("<Delete>", lambda e: self._on_delete())
        self.root.bind("<BackSpace>", lambda e: self._on_delete())
        self.root.bind("<space>", lambda e: self._on_toggle())
        self.root.bind("<F2>", lambda e: self._on_rename())
        self.root.bind("<Control-l>", lambda e: self._on_clear_completed())

    def _on_canvas_resize(self, event: tk.Event) -> None:
        self.canvas.itemconfigure(self.canvas_window, width=event.width)

    def _on_add(self) -> None:
        title = self.entry.get().strip()
        if not title:
            return
        try:
            self.controller.add_task(title)
        except ValueError as ex:
            messagebox.showerror("Invalid title", str(ex))
            return
        self.entry.delete(0, "end")
        self.refresh()

    def _on_delete(self) -> None:
        task = self._selected_task()
        if not task:
            return
        self.controller.delete_task(task.id)
        self.refresh()

    def _on_toggle(self) -> None:
        task = self._selected_task()
        if not task:
            return
        self.controller.toggle_task(task.id)
        self.refresh()

    def _on_rename(self) -> None:
        task = self._selected_task()
        if not task:
            return
        new_title = simpledialog.askstring("Rename task", "New title:", initialvalue=task.title, parent=self.root)
        if new_title is None:
            return
        try:
            self.controller.rename_task(task.id, new_title)
        except ValueError as ex:
            messagebox.showerror("Invalid title", str(ex))
        self.refresh()

    def _on_clear_completed(self) -> None:
        removed = self.controller.clear_completed()
        if removed:
            messagebox.showinfo("Cleared", f"Removed {removed} completed task(s)")
        self.refresh()

    def _set_filter(self, f: Filter) -> None:
        self.filter = f
        self.refresh()

    def _about(self) -> None:
        messagebox.showinfo(
            "About",
            "To‑Do List — Tkinter\n\n"
            "Author: Mobin Yousefi (github.com/mobinyousefi-cs)\n"
            "License: MIT",
        )

    # --- render ---
    def refresh(self) -> None:
        # Clear existing widgets
        for child in self.list_frame.winfo_children():
            child.destroy()
        self._task_widgets.clear()

        tasks = self._filtered(self.controller.tasks)
        for t in tasks:
            self._render_task(t)

        total = len(self.controller.tasks)
        active = len([t for t in self.controller.tasks if not t.done])
        self.stats_label.config(text=f"{active} active / {total} total")

    def _render_task(self, t: Task) -> None:
        row = ttk.Frame(self.list_frame, padding=(4, 6, 4, 6), style="Task.TFrame")
        row.pack(fill="x")

        var = tk.BooleanVar(value=t.done)
        cb = ttk.Checkbutton(row, text=t.title, variable=var, command=lambda i=t.id: (self.controller.toggle_task(i), self.refresh()))
        cb.pack(side="left", fill="x", expand=True)
        self._task_widgets[t.id] = cb

        menu_btn = ttk.Menubutton(row, text="⋮")
        menu = tk.Menu(menu_btn, tearoff=0)
        menu.add_command(label="Rename", command=lambda i=t.id: (self._select(i), self._on_rename()))
        menu.add_command(label="Set Priority → Low", command=lambda i=t.id: (self.controller.set_priority(i, Priority.LOW), self.refresh()))
        menu.add_command(label="Set Priority → Medium", command=lambda i=t.id: (self.controller.set_priority(i, Priority.MEDIUM), self.refresh()))
        menu.add_command(label="Set Priority → High", command=lambda i=t.id: (self.controller.set_priority(i, Priority.HIGH), self.refresh()))
        menu.add_separator()
        menu.add_command(label="Delete", command=lambda i=t.id: (self._select(i), self._on_delete()))
        menu_btn["menu"] = menu
        menu_btn.pack(side="right")

    # --- helpers ---
    def _filtered(self, tasks: List[Task]) -> List[Task]:
        if self.filter == "active":
            return [t for t in tasks if not t.done]
        if self.filter == "done":
            return [t for t in tasks if t.done]
        return tasks

    def _selected_task(self) -> Optional[Task]:
        # Choose the first visible task whose checkbutton currently has focus or last interacted
        for t_id, widget in self._task_widgets.items():
            if str(self.root.focus_get()) == str(widget):
                return next((t for t in self.controller.tasks if t.id == t_id), None)
        # Fallback: return first task under current filter
        tasks = self._filtered(self.controller.tasks)
        return tasks[0] if tasks else None

    def _select(self, task_id: str) -> None:
        widget = self._task_widgets.get(task_id)
        if widget:
            widget.focus_set()
