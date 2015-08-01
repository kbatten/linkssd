#!/usr/bin/env python

from __future__ import print_function

import time
import os
import sys

import ntfsutils.junction


def list_directories(base):
    try:
        directories = os.walk(base).next()[1]
    except StopIteration:
        directories = []
    return directories

def create_junction(directory, junction):
    try:
        ntfsutils.junction.unlink(junction)
    except Exception as e:
        if str(e).strip().endswith(' does not exist or is not a junction'):
            pass
        else:
            raise e
    try:
        ntfsutils.junction.create(directory, junction)
    except Exception as e:
        if str(e).strip().endswith(': junction link name already exists'):
            pass
        else:
            raise e

def create_junction_all(directory, junction):
    for drive in drives:
        for d in list_directories(drive + directory):
            directory_fqn = drive + directory + "\\" + d
            create_junction(directory_fqn, junction + "\\" + d)


drives = ['D', 'E']
home = os.path.expanduser("~")


def main():
    create_junction_all(r":\SSD\Steam\steamapps\common",
                        r"C:\Program Files (x86)\Steam\steamapps\common")
    create_junction_all(r":\SSD\Steam\steamapps\sourcemods",
                        r"C:\Program Files (x86)\Steam\steamapps\sourcemods")
    #create_junction(r"E:\SSD\torrents", home + r"\Downloads\torrents")
    #create_junction(r"E:\SSD\iTunes_music", home + r"\Music\iTunes")
    #create_junction(r"E:\SSD\Apple_mobile_backup", home + r"\AppData\Roaming\Apple Computer\MobileSync\Backup")
    create_junction_all(r":\SSD\Roaming", home + r"\AppData\Roaming")
    create_junction_all(r":\SSD\Origin Games", r"C:\Program Files (x86)\Origin Games")
    create_junction_all(r":\SSD\Program Files (x86)", r"C:\Program Files (x86)")
    create_junction_all(r":\SSD\Program Files", r"C:\Program Files")


if __name__ == "__main__":
    main()
