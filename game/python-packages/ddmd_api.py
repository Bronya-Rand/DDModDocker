import renpy
import json
import os

class ModDocker_API:

    def __init__(self):
        self.mods_path = os.path.join(renpy.store.persistent.ddml_basedir, "game/mods")
        self.mod_basedir = renpy.config.basedir.replace("\\", "/")
        self.mod_gamedir = renpy.config.gamedir.replace("\\", "/")
        self.mod_info = []
        self.multipersistent = None

    def parse_mod_info(self, path):
        """
        Parses a given JSON
        """
        with open(path, "r") as mod_info:
            return json.load(mod_info)

    def get_mod_info(self):
        """
        Get's the current mod containers' build name.
        """
        if os.path.exists(os.path.join(self.mod_basedir, "modinfo.json")):
            self.mod_info = self.parse_mod_info(os.path.join(self.mod_basedir, "modinfo.json"))
        else:
            self.mod_info = [
                {
                    "modName": renpy.config.name,
                    "modVersion": renpy.config.version,
                    "buildName": renpy.store.build.name,
                    "saveDir": renpy.config.savedir.replace("\\", "/"),
                }
            ]

    def get_current_container_path(self):
        """
        Returns the mods base directory
        """
        return self.mod_basedir

    def get_current_container_game_folder(self):
        """
        Returns the mods game directory
        """
        return self.mod_gamedir

    def get_current_container_name(self):
        """
        Returns the mods name
        """
        return self.mod_info[0]["modName"]

    def get_current_container_version(self):
        """
        Returns the mod version
        """
        return self.mod_info[0]["modVersion"]

    def get_current_container_build_name(self):
        """
        Returns the mod build name
        """
        return self.mod_info[0]["buildName"]

    def get_current_container_save_folder(self):
        """
        Returns the mod save directory
        """
        return self.mod_info[0]["saveDir"]

    def is_multiple_copies(self):
        """
        Checks if the user has multiple copies of the same mod
        """
        same_mods = []
        for x in os.listdir(self.mods_path):
            try: temp = self.parse_mod_info(os.path.join(self.mods_path, x, "modInfo.json"))
            except IOError: continue
            if temp[0]["buildName"] == self.get_current_container_build_name() and temp[0]["modName"] == self.get_current_container_name():
                same_mods.append(x)
        if len(same_mods) != 0:
            return True
        return False

    def set_multipersistent(self, persist_name):
        """
        [BETA] Makes a multipersistent variable to use across mods for variable
        data or other things.
        """
        self.multipersistent = renpy.persistent.MultiPersistent(persist_name)

    def get_multipersistent(self):
        """
        Returns the multipersistent variable
        """
        return self.multipersistent

    def write_mod_data(self):
        """
        Writes the mod data to a JSON file
        """
        with open(os.path.join(self.mod_basedir, "modinfo.json"), "w") as mod_info:
            json.dump(self.mod_info, mod_info) 