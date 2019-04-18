#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import os
import sys

import ntfsutils.junction


def list_directories(base):
    """List directories in the base directory.

    >>> list_directories(r"D:\SSD\Games")
    ["Adventure", "Pong", "Zork"]

    """
    try:
        directories = os.walk(base).next()[1]
    except StopIteration:
        directories = []
    return directories

def create_junction(src, dst):
    """Create a junction from the source directory to destination directory.
    If the destination directory exists and is a junction, remove it first.

    >>> create_junction(r"D:\SSD\Games\Zork", r"C:\Games\Zork")

    """
    try:
        ntfsutils.junction.unlink(dst)
    except Exception as e:
        if str(e).strip().endswith(" does not exist or is not a junction"):
            pass
        else:
            raise e
    try:
        ntfsutils.junction.create(src, dst)
    except Exception as e:
        if str(e).strip().endswith(": junction link name already exists"):
            pass
        else:
            raise e

def create_junction_all(drives, src, dst):
    """Create a junction for all directories in the source directory on each
    drive into the destination directory.

    >>> create_junction_all(["D:", "E:"], r"\SSD\Games", r"C:\Games")

    """
    for drive in drives:
        for d in list_directories(drive + src):
            src_fqn = drive + src + "\\" + d
            dst_fqn = dst + "\\" + d
            create_junction(src_fqn, dst_fqn)


def main():
    DRIVES = ["D:", "E:"]
    HOME = os.path.expanduser("~")

    create_junction_all(DRIVES,
                        r"\SSD\Roaming",
                        HOME + r"\AppData\Roaming")

    create_junction_all(DRIVES,
                        r"\SSD\Program Files (x86)",
                        r"C:\Program Files (x86)")

    create_junction_all(DRIVES,
                        r"\SSD\Program Files",
                        r"C:\Program Files")

    create_junction_all(DRIVES,
                        r"\SSD\Steam\common",
                        r"C:\Program Files (x86)\Steam\steamapps\common")

    create_junction_all(DRIVES,
                        r"\SSD\Steam\sourcemods",
                        r"C:\Program Files (x86)\Steam\steamapps\sourcemods")

    create_junction_all(DRIVES,
                        r"\SSD\Origin Games",
                        r"C:\Program Files (x86)\Origin Games")


if __name__ == "__main__":
    main()
