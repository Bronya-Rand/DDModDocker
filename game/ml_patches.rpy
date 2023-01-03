## Copyright 2022 Azariel Del Carmen (GanstaKingofSA)

init -100 python:
    import os
    import hashlib

    for archive in ['audio','images','fonts','scripts']:
        if archive + ".rpa" not in os.listdir(persistent.ddml_basedir + "/game"):
            raise Exception("'%s.rpa' was not found in the Mod Docker game folder. Check your installation and try again." % archive)

    ## Hash as of DDLC 1.1.1
    if hashlib.sha256(open(os.path.join(persistent.ddml_basedir, "game/scripts.rpa"), "rb").read()).hexdigest() != 'da7ba6d3cf9ec1ae666ec29ae07995a65d24cca400cd266e470deb55e03a51d4':
        raise Exception("Hash mismatch between the current 'scripts.rpa' file and DDLC 1.1.1's 'scripts.rpa'.\nPlease add DDLC's original 1.1.1 'scripts.rpa' into DDML's game directory.")

    if not os.path.exists(persistent.ddml_basedir + "/characters"):
        os.makedirs(persistent.ddml_basedir + "/characters")
    if not os.path.exists(persistent.ddml_basedir + "/game/mods"):
        os.makedirs(persistent.ddml_basedir + "/game/mods")

    if config.window_title != "Doki Doki Mod Docker: SE (Alpha)":
        config.window_title = "Doki Doki Mod Docker: SE (Alpha) - R6 Mod Container"

init python:
    if not os.path.exists(config.basedir + "/characters"):
        os.makedirs(config.basedir + "/characters")

init 1 python:
    # Addresses the MAS Updater Issue
    store.updater.DEFERRED_UPDATE_FILE = os.path.join(config.basedir, "update", "deferred.txt")
    store.updater.DEFERRED_UPDATE_LOG = os.path.join(config.basedir, "update", "log.txt")
        
init 1 python:
    import ddmd_api

    modDocker_api = ddmd_api.ModDocker_API()
    modDocker_api.get_mod_info()

    # Re-write in case of new API updates
    if modDocker_api.get_current_container_save_folder().split("/")[-1] != "DDLC":
        modDocker_api.write_mod_data()

init -100 python:

    def patched_file(fn):
        import re
        basechrs = re.compile(r"^(monika|sayori|yuri|natsuki)\.chr")

        if ".." in fn:
            fn = fn.replace("..", config.basedir.replace("\\", "/"))

        # Include CHRs if called from patch RPA
        if basechrs.match(fn):
            return renpy.loader.load('mod_patches/chrs/' + fn)
        return renpy.loader.load(fn)

    renpy.file = patched_file

    Composite = LiveComposite