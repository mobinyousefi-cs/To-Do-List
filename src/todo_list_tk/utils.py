#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: To-Do List (Tkinter)
File: utils.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================

Description:
Utility helpers.

===========================================================================
"""
from __future__ import annotations

import uuid


def new_id() -> str:
    return uuid.uuid4().hex
