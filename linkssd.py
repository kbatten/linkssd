#!/usr/bin/env python

import time
import os
import sys

try:
    from ntfsutils.junction import isjunction
    from ntfsutils.junction import create as createjunction
    from ntfsutils.junction import unlink as unlinkjunction
    _junction_data = {}
except ImportError:
    _junction_data = {}
    def isjunction(directory):
        if directory in _junction_data:
            return True
        return False

    def createjunction(directory, junction):
        if junction in _junction_data:
            raise Exception("%s: junction link name already exists" % junction)
        _junction_data[junction] = directory

    def unlinkjunction(path):
        if not isjunction(path):
            raise Exception("%s does not exist or is not a junction" % path)
        _junction_data[path]

    def walk(base):
        yield [base, ['dir1','dir2','dir3'], None]
    def join(base,d):
        return base + '\\' + d
    os.walk = walk
    os.path.join = join

    createjunction(r"E:\SSD\torrents", os.path.expanduser("~") + r"\Downloads\torrents")


def list_directories(base):
    try:
        directories = os.walk(base).next()[1]
    except StopIteration:
        directories = []
    return directories


junction_data = {}
home = os.path.expanduser("~")

# Link spinning disk steam common files
for drive in ['D', 'E']:
    for d in list_directories(drive + r":\SSD\Steam\steamapps\common"):
        directory = drive + r":\SSD\Steam\steamapps\common" + "\\" + d
        junction = r"C:\Program Files (x86)\Steam\steamapps\common" + "\\" + d
        junction_data[junction] = directory

# Link spinning disk steam sourcemods
for drive in ['D', 'E']:
    for d in list_directories(drive + r":\SSD\Steam\steamapps\sourcemods"):
        directory = drive + r":\SSD\Steam\steamapps\sourcemods" + "\\" + d
        junction = r"C:\Program Files (x86)\Steam\steamapps\sourcemods" + "\\" + d
        junction_data[junction] = directory

# Link spinning disk torrent downloads
junction_data[home + r"\Downloads\torrents"] = r"E:\SSD\torrents"

# Link spinning disk itunes music
junction_data[home + r"\Music\iTunes"] = r"E:\SSD\iTunes_music"

# Link spinning disk apple mobile backup
junction_data[home + r"\AppData\Roaming\Apple Computer\MobileSync\Backup"] = r"E:\SSD\Apple_mobile_backup"

# Link AppData\Roaming
for drive in ['D', 'E']:
    for d in list_directories(drive + r":\SSD\Roaming"):
        directory = drive + r":\SSD\Roaming" + "\\" + d
        junction = home + r"\AppData\Roaming" + "\\" + d
        junction_data[junction] = directory

# Link Origin Games
for drive in ['D', 'E']:
    for d in list_directories(drive + r":\SSD\Origin Games"):
        directory = drive + r":\SSD\Origin Games" + "\\" + d
        junction = r"C:\Program Files (x86)\Origin Games" + "\\" + d
        junction_data[junction] = directory

# Link Program Files (x86)
for drive in ['D', 'E']:
    for d in list_directories(drive + r":\SSD\Program Files (x86)"):
        directory = drive + r":\SSD\Program Files (x86)" + "\\" + d
        junction = r"C:\Program Files (x86)" + "\\" + d
        junction_data[junction] = directory

# Link Retroshare Downloads and Partials
with open(home + r"\AppData\Roaming\RetroShare" + "\\default_cert.txt") as f:
    dc = f.read().strip()
junction_data[home + r"\AppData\Roaming\RetroShare" + "\\" + dc + r"\Downloads"] = r"E:\SSD\Retroshare\Downloads"
junction_data[home + r"\AppData\Roaming\RetroShare" + "\\" + dc + r"\Partials"] = r"E:\SSD\Retroshare\Partials"

# Link Sandboxed Apps
for drive in ['D', 'E']:
    for d in list_directories(drive + r":\SSD\Sandboxed Apps"):
        directory = drive + r":\SSD\Sandboxed Apps" + "\\" + d
        junction = r"C:\Sandboxed Apps" + "\\" + d
        junction_data[junction] = directory


#######################

for junction in junction_data.keys():
    directory = junction_data[junction]
    try:
        unlinkjunction(junction)
    except Exception as e:
        if str(e).strip().endswith(' does not exist or is not a junction'):
            pass
        else:
            raise e
    try:
        createjunction(directory, junction)
    except Exception as e:
        if str(e).strip().endswith(': junction link name already exists'):
            pass
        else:
            raise e
