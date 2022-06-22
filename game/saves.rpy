## Copyright 2022 Azariel Del Carmen (GanstaKingofSA)

python early:
    import json
    
    try:
        with open(renpy.config.basedir + "/selectedmod.json", "r") as mod_json:
            temp = json.load(mod_json)
            selectedMod = temp['modName']
    except IOError:
        selectedMod = "DDLC"

    renpy.config.savedir = renpy.config.basedir + "/game/MLSaves/" + selectedMod