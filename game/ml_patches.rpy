
init -100 python:
    import hashlib

    for archive in ['audio','images','fonts','scripts']:
        if archive + ".rpa" not in os.listdir(persistent.ddml_basedir + "/game"):
            raise Exception("'%s' was not found in the Mod Docker game folder. Check your installation and try again." % archive + ".rpa")

    ## Hash as of DDLC 1.1.1
    if hashlib.sha256(renpy.file(persistent.ddml_basedir + "/game/scripts.rpa").read()).hexdigest() != 'da7ba6d3cf9ec1ae666ec29ae07995a65d24cca400cd266e470deb55e03a51d4':
        raise Exception("Hash mismatch between the current 'scripts.rpa' file and DDLC 1.1.1's 'scripts.rpa'.\nPlease add DDLC's original 1.1.1 'scripts.rpa' into DDML's game directory.")

    if not os.path.exists(persistent.ddml_basedir + "/characters"):
        os.makedirs(persistent.ddml_basedir + "/characters")
    if not os.path.exists(persistent.ddml_basedir + "/game/mods"):
        os.makedirs(persistent.ddml_basedir + "/game/mods")
    if not os.path.exists(persistent.ddml_basedir + "/game/MLSaves"):
        os.makedirs(persistent.ddml_basedir + "/game/MLSaves")
    if not os.path.exists(config.basedir + "/characters"):
        os.makedirs(config.basedir + "/characters")
    
init 1 python:

    def patched_file(fn):
        if ".." in fn:
            fn = fn.replace("..", config.basedir)

        return renpy.loader.load(fn)

    renpy.file = patched_file