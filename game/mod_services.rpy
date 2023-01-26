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
            for modfolder in os.listdir(self.modpath):
                if os.path.exists(os.path.join(self.modpath, modfolder, "game")):
                    self.mods[modfolder] = os.path.join(self.modpath, modfolder, "game")

            while True:
                modFolders = []
                for modfolder in os.listdir(self.modpath):
                    if os.path.exists(os.path.join(self.modpath, modfolder, "game")):
                        modFolders.append(modfolder)

                if len(modFolders) < len(self.mods):
                    for mod in self.mods.keys():
                        if not os.path.exists(os.path.join(self.modpath, mod)):
                            self.mods.pop(mod)
                elif len(modFolders) > len(self.mods):
                    for mod in modFolders:
                        if not self.mods.get(mod):
                            self.mods[mod] = os.path.join(self.modpath, mod, "game")

                sleep(5)

    ddmd_modlist_service = ModListService()