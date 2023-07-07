## Copyright 2023 Azariel Del Carmen (GanstaKingofSA)

python early:
    import os
    import json

    def save_path():
        if renpy.macintosh:
            rv = "~/Library/RenPy/DD-ModDocker"
            return os.path.expanduser(rv)

        elif renpy.windows:
            if 'APPDATA' in os.environ:
                return os.path.join(os.environ['APPDATA'], "RenPy", "DD-ModDocker")
            else:
                rv = "~/RenPy/DD-ModDocker"
                return os.path.expanduser(rv)

        else:
            rv = "~/.renpy/DD-ModDocker"
            return os.path.expanduser(rv)
    
    try:
        with open(os.path.join(renpy.config.basedir, "selectedmod.json"), "r") as mod_json:
            temp = json.load(mod_json)
            selectedMod = temp['modName']
    except IOError:
        selectedMod = "DDLC"

    renpy.config.savedir = os.path.join(save_path(), selectedMod)