init -1 python in ddmd_services:
    from store import persistent
    import threading
    import os
    from time import sleep

    class ModListService(object):
        def __init__(self):
            self.modpath = persistent.ddml_basedir + "/game/mods"
            self.mods = {}
            thread = threading.Thread(target=self.run)
            thread.daemon = True
            thread.start()

        def run(self):
            for entry in os.scandir(self.modpath):
                if entry.is_dir() and os.path.exists(os.path.join(entry.path, "game")):
                    self.mods[entry.name] = os.path.join(entry.path, "game")

            while True:
                modFolders = {
                    entry.name: entry.path
                    for entry in os.scandir(self.modpath)
                    if entry.is_dir() and os.path.exists(os.path.join(entry.path, "game"))
                }
                
                removed_mods = [mod for mod in self.mods if mod not in modFolders]
                self.mods = {mod: path for mod, path in self.mods.items() if mod not in removed_mods}

                added_mods = [mod for mod in modFolders if mod not in self.mods]
                self.mods.update({mod: path for mod, path in modFolders.items() if mod in added_mods})

                sleep(5)

    ddmd_modlist_service = ModListService()