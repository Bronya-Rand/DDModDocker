## Copyright 2022-2024 Azariel Del Carmen (bronya_rand)

init -100 python:
    import hashlib

    for archive in ['audio','images','fonts','scripts']:
        if archive + ".rpa" not in os.listdir(persistent.ddml_basedir + "/game"):
            raise Exception("'%s.rpa' was not found in the Mod Docker game folder. Check your installation and try again." % archive)

    if hashlib.sha256(open(os.path.join(persistent.ddml_basedir, "game/scripts.rpa"), "rb").read()).hexdigest() != "a4833c4b8a611e8ea8c0f5e168a33aa13dafe2eed183593f12293497b121d339":
        raise Exception("Hash mismatch between the current 'scripts.rpa' file and DDMD's patched 'scripts.rpa'.\nPlease add DDMD's patched 'scripts.rpa' into DDMD's game directory.")

    if not os.path.exists(persistent.ddml_basedir + "/characters"):
        os.makedirs(persistent.ddml_basedir + "/characters")
    if not os.path.exists(persistent.ddml_basedir + "/game/mods"):
        os.makedirs(persistent.ddml_basedir + "/game/mods")

init 1 python:
    if config.window_title != "Doki Doki Mod Docker (Alpha)":
        container_name = config.window_title or config.name or config.basedir.replace("\\", "/").split("/")[-1]
        config.window_title = _("Doki Doki Mod Docker (Alpha) - Mod Container: ") + container_name

init python:
    if not os.path.exists(config.basedir + "/characters"):
        os.makedirs(config.basedir + "/characters")

init 1 python:
    # Addresses the Ren'Py/MAS Updater Issue
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