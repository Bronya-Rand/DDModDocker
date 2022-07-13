## Copyright 2019-2022 Azariel Del Carmen (GanstaKingofSA). All rights reserved.

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
    if renpy.version_tuple >= (7, 4, 7, 1862):
        config.atl_start_on_show = False 

init 1 python:
    def patched_screenshot():
        if renpy.version_tuple > (7, 3, 5, 606):
            srf = renpy.display.draw.screenshot(None)
        else:
            srf = renpy.display.draw.screenshot(None, False)
        
        return srf

    screenshot_srf = patched_screenshot
