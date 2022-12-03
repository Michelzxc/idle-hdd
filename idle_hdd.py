"""
Objective of project: Detect and suspend unmounted hard disk drive.
Designed for Linux (Ubuntu 20.10).

=================================================
Dependences (testing in):
        Python3 (3.10.7)
        hdparm (v9.60)
        lsblk (2.38)
"""

__author__ = "Michel"
__contact__ = "micheldarosazxc@gmail.com"
__date__ = "2022-11-01"


import subprocess
import sys
import json
import time


HDPARM_PATH = "/usr/sbin/hdparm"
LSBLK_PATH = "/usr/bin/lsblk"


def error_exit(stderr: str):
    """Print stderr and call SystemExit if stderr is not void string."""

    if stderr != "":
        print(stderr)
        sys.exit()


def lsblk_table() -> list:
    """
    Detect and return all /dev/sdx devices and param information:
    name: str, type: disk | part, mountpoint: str,
    model: str, rota: True | False
    """
    process_lsblk = subprocess.run(
        [LSBLK_PATH, "-o", "NAME,TYPE,MOUNTPOINT,MODEL,ROTA", "-pJ"],
        capture_output=True,
        text=True
    )

    error_exit(process_lsblk.stderr)

    devices = json.loads(process_lsblk.stdout)["blockdevices"]
    for block in devices.copy():
        if "/dev/sd" not in block["name"]:
            devices.remove(block)

    return devices


def check_disk_on(name: str) -> bool:
    """Check if the disk is active."""

    process_hdparm = subprocess.run(
        [HDPARM_PATH, "-C", name],
        capture_output=True,
        text=True,
    )

    error_exit(process_hdparm.stderr)

    if "active" in process_hdparm.stdout:
        return True

    elif "standby" in process_hdparm.stdout:
        return False


def hdd_devices() -> list:
    """Create table of hard disk drive."""

    hdd_devices_table = []
    for device in lsblk_table():
        if device["rota"]:
            hdd_devices_table.append(device)

    for disk in hdd_devices_table:
        try:
            disk["is_active"] = check_disk_on(disk["name"])

        except KeyError:
            error_exit("KeyError in function hdd_devices")

    return hdd_devices_table


def main():
    for disk in hdd_devices():
        try:
            partitions = disk["children"]

        except KeyError:
            continue

        any_mounted = False
        for part in partitions:
            if part["mountpoint"] is not None:
                any_mounted = True
                break

        if any_mounted:
            continue

        else:
            time.sleep(2)
            process_hdparm = subprocess.run(
                [HDPARM_PATH, "-y", disk["name"]],
                capture_output=True,
                text=True
            )

            error_exit(process_hdparm.stderr)

    print("Completed process")
    sys.exit()


if __name__ == "__main__":
    main()
