## Copyright 2019-2022-2024 Azariel Del Carmen (bronya_rand). All rights reserved.

## Patches 'wmic' environment variables with 'powershell' instead.
python early:
    import os
    os.environ['wmic process get Description'] = "powershell (Get-Process).ProcessName"
    os.environ['wmic os get version'] = "powershell (Get-WmiObject -class Win32_OperatingSystem).Version"

init -100 python:
    if renpy.windows:
        onedrive_path = os.environ.get("OneDrive")
        if onedrive_path is not None:
            if onedrive_path in config.basedir:
                raise Exception("Mod Docker cannot be run from a cloud folder. Move Mod Docker to another location and try again.")

init -1 python:
    ## Fixes a issue where some transitions (menu bg) reset themselves
    config.atl_start_on_show = False 

init 1 python:
    def patched_screenshot():
        srf = renpy.display.draw.screenshot(None)
        return srf

    screenshot_srf = patched_screenshot
