## Copyright 2022 Azariel Del Carmen (GanstaKingofSA)

init -100 python:
    import hashlib

    for archive in ['audio','images','fonts','scripts']:
        if archive + ".rpa" not in os.listdir(persistent.ddml_basedir + "/game"):
            raise Exception("'%s.rpa' was not found in the Mod Docker game folder. Check your installation and try again." % archive)

    if not os.path.exists(persistent.ddml_basedir + "/characters"):
        os.makedirs(persistent.ddml_basedir + "/characters")
    if not os.path.exists(persistent.ddml_basedir + "/game/mods"):
        os.makedirs(persistent.ddml_basedir + "/game/mods")

    if config.window_title != "Doki Doki Mod Docker (Alpha)":
        container_name = config.name or config.basedir.replace("\\", "/").split("/")[-1]
        config.window_title = _("Doki Doki Mod Docker (Alpha) - Mod Container: ") + container_name

init python:
    if not os.path.exists(config.basedir + "/characters"):
        os.makedirs(config.basedir + "/characters")

init 1 python:
    import ddmd_api
    
    modDocker_api = ddmd_api.ModDocker_API()
    modDocker_api.get_mod_info()
    
    # Re-write in case of new API updates
    if modDocker_api.get_current_container_save_folder().split("/")[-1] != "DDLC":
        modDocker_api.write_mod_data()

init -100 python:

    def patched_file(fn):
        if ".." in fn:
            fn = fn.replace("..", config.basedir.replace("\\", "/"))
            
        return renpy.loader.load(fn)

    renpy.file = patched_file