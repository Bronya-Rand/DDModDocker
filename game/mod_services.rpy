
init -1 python in ddmd_services:
    from store import persistent
    import threading
    import os
    from time import sleep
    from collections import defaultdict

    class ModListService(object):
        def __init__(self):
            self.modpath = persistent.ddml_basedir + "/game/mods"
            self.mods = {}
            thread = threading.Thread(target=self.run)
            thread.daemon = True
            thread.start()
    
        def run(self):
            for modfolder in os.listdir(self.modpath):
                if os.path.isdir(os.path.join(self.modpath, modfolder, "game")):
                    self.mods[modfolder] = os.path.join(self.modpath, modfolder, "game")

            while True:
                modFolders = {}
                for entry in os.listdir(self.modpath):
                    entry_path = os.path.join(self.modpath, entry)
                    if os.path.isdir(entry_path) and os.path.exists(os.path.join(entry_path, "game")):
                        modFolders[entry] = entry_path

                for modfolder in os.listdir(self.modpath):
                    modfolder_path = os.path.join(self.modpath, modfolder)
                    if os.path.exists(os.path.join(modfolder_path, "game")):
                        if modfolder not in modFolders:
                            modFolders[modfolder] = modfolder_path

                if len(modFolders) < len(self.mods):
                    for mod in self.mods.keys():
                        if not os.path.exists(os.path.join(self.modpath, mod)):
                            self.mods.pop(mod)
                elif len(modFolders) > len(self.mods):
                    for mod in modFolders:
                        if mod not in self.mods:
                            self.mods[mod] = os.path.join(self.modpath, mod, "game")
                
                sleep(2)
    
    ddmd_modlist_service = ModListService()
    