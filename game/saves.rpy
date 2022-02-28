python early:
    import json
    try:
        with open(renpy.config.basedir + "/selectedmod.json", "r") as s:
            j = json.load(s)
            selectedMod = j['modName']
    except:
        selectedMod = "DDLC"

    renpy.config.savedir = renpy.config.basedir + "/game/MLSaves/" + selectedMod