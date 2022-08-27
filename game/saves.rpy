## Copyright 2022 Azariel Del Carmen (GanstaKingofSA)

python early:
    import json

    if os.path.exists(renpy.config.basedir + "/game/MLSaves"):
        for src, dirs, files in os.walk(renpy.config.basedir + "/game/MLSaves"):
            for d in dirs:
                src_dir = os.path.join(src, d)
                dst_dir = src_dir.replace(src, renpy.config.savedir)
                shutil.move(src_dir, dst_dir)
    
    try:
        with open(renpy.config.basedir + "/selectedmod.json", "r") as mod_json:
            temp = json.load(mod_json)
            selectedMod = temp['modName']
    except IOError:
        selectedMod = "DDLC"

    renpy.config.savedir = renpy.main.__main__.path_to_saves(
            renpy.config.gamedir
        ) + "/" + selectedMod