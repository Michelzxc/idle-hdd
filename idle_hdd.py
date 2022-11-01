#!/usr/bin/python3

"""
Objetivo: Detectar y suspender discos duros (hard disk drive) desmontados.
Diseñado para linux (Ubuntu 20.10).

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
import json
import time


def lsblk_table() -> list:
    """
    Detecta y retorna todos los /dev/sdx e información adicional:
    name: str, type: disk | part, mountpoint: str,
    model: str, rota: True | False
    """
    process_lsblk = subprocess.run(
        ["lsblk", "-o", "NAME,TYPE,MOUNTPOINT,MODEL,ROTA", "-pJ"],
        capture_output=True,
        text=True
    )

    devices = json.loads(process_lsblk.stdout)["blockdevices"]
    for block in devices.copy():
        if "/dev/sd" not in block["name"]:
            devices.remove(block)

    return devices


def check_disk_on(name: str) -> bool:
    """Comprueba si el disco está encendido."""

    process_hdparm = subprocess.run(
        ["hdparm", "-C", name],
        capture_output=True,
        text=True,
    )

    if "active" in process_hdparm.stdout:
        return True

    elif "standby" in process_hdparm.stdout:
        return False

    elif process_hdparm.stderr != "":
        raise RuntimeError(process_hdparm.stderr)


def hdd_devices() -> list:
    """Crea la tabla de discos duros."""

    hdd_devices_table = []
    for device in lsblk_table():
        if device["rota"]:
            hdd_devices_table.append(device)

    for disk in hdd_devices_table:
        disk["is_active"] = check_disk_on(disk["name"])

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
            time.sleep(0.5)
            process_hdparm = subprocess.run(
                ["hdparm", "-y", disk["name"]],
                capture_output=True,
                text=True
            )

            if process_hdparm.stderr != "":
                raise RuntimeError(process_hdparm.stderr)


if __name__ == "__main__":
    main()

