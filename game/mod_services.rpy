
init -1 python in ddmd_services:
    from store import persistent
    import threading
    import os
    from time import sleep
    from collections import defaultdict

    class ModListService(object):
        def __init__(self):
            self.modpath = persistent.ddml_basedir + "/game/mods"
            self.mods = defaultdict(list)
            self.old_mods = None

            thread = threading.Thread(target=self.run)
            thread.daemon = True
            thread.start()
    
        def run(self):
            while True:
                new_mods = defaultdict(list)
                for entry in os.listdir(self.modpath):
                    entry_path = os.path.join(self.modpath, entry)
                    if os.path.isdir(entry_path) and os.path.exists(os.path.join(entry_path, "game")):
                        new_mods[entry].append(entry_path)

                # Detect changes and update self.mods
                if self.old_mods is not None:
                    for mod, paths in self.old_mods.items():
                        if mod not in new_mods:
                            for path in paths:
                                self.mods[mod].remove(path)

                    for mod, paths in new_mods.items():
                        if mod not in self.old_mods:
                            for path in paths:
                                self.mods[mod].append(path)

                self.old_mods = new_mods
                sleep(2)
    
    ddmd_modlist_service = ModListService()
    