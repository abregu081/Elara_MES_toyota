#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from cx_Freeze import setup, Executable

includes = []
includefiles = []
excludes = ['Tkinter']
packages = ['os', 'socket']

setup(
 name="MESxLog",
 version="1.1",
 description="MESxLog version 1.1",
 options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}}, 
 executables = [Executable("MESxLog.py")],
 )

build_exe_options = {
                 "includes":      includes,
}
