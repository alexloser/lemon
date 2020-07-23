#!/usr/bin/env python
# coding: utf-8
import os 
import sys
import shutil


def remove_pycache(path):
    folders = []
    for root, _, _, in os.walk(path):
        if root.endswith("__pycache__"):
            if os.path.isdir(root):
                folders.append(root)
    for name in folders:   
        print(f"Remove {name}")
        shutil.rmtree(name)

remove_pycache(sys.argv[1])










