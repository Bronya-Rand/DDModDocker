# Copyright 2024 Azariel Del Carmen (bronya_rand)

import renpy
import os
import json


class ModDockerMain(object):

    def __init__(self):
        self.renpy_sdk_folders = [
            "launcher",
            "gui",
            "doc",
            "module",
            "tutorial",
            "the_question",
        ]
        self.mod_name = None
        self.ddlc_mode = False
        self.rpa_format = False

    def running_renpy_sdk(self):
        """
        Checks to see if the code is being executed within the Ren'Py Launcher.
        """
        return any(
            folder in self.renpy_sdk_folders
            for folder in os.listdir(renpy.config.basedir)
        )

    def set_renpy_to_mod(self, mod_data):
        """
        Sets class data to mod data.
        """
        try:
            self.mod_name = mod_data["modName"]
            self.rpa_format = mod_data["isRPA"]
        except KeyError:
            raise Exception(
                "Invalid Selected Mod JSON or the file has been corrupt. Delete the file and select a mod once again."
            )

        mod_directory = os.path.join(renpy.config.gamedir, "mods", self.mod_name)
        mod_game_directory = os.path.join(mod_directory, "game")
        mod_directory_normalized = os.path.normpath(mod_directory).replace("\\", "/")

        if not os.path.exists(mod_game_directory):
            raise Exception(
                "'game' folder could not be found in {}.".format(
                    mod_directory_normalized
                )
            )

        renpy.config.gamedir = os.path.normpath(mod_game_directory).replace("\\", "/")

    def initialize_docker(self):
        """
        Initializes the DDMD engine. Validates error loading mod JSON or if
        """
        mod_json_path = os.path.join(renpy.config.basedir, "selectedmod.json")
        if not os.path.exists(mod_json_path):
            self.ddlc_mode = True
            return

        try:
            with open(mod_json_path, "r") as mj:
                mod_data = json.load(mj)
                self.set_renpy_to_mod(mod_data)
        except (IOError, ValueError):
            self.ddlc_mode = True
            return

    def find_mod_archives(self, archive_extensions):
        """
        Locates and loads the necessary RPAs for DDLC + Mods
        """
        if self.running_renpy_sdk():
            return []
        archives = []

        if os.path.exists(os.path.join(renpy.config.basedir, "game", "ddml.rpa")):
            archives.append("ddml")

        # Base DDLC
        archives.append("audio")
        archives.append("fonts")
        archives.append("images")

        # Base DDLC + RPYC Mode
        if self.ddlc_mode or not self.rpa_format:
            archives.append("scripts")
        else:
            # RPA Mode
            for i in sorted(os.listdir(renpy.config.gamedir)):
                base, ext = os.path.splitext(i)

                if not (ext in archive_extensions):
                    continue

                if base in archives:
                    archives.remove(base)

                archives.append("mods/{}/game/{}".format(self.mod_name, base))

            if os.path.exists(
                os.path.join(renpy.config.basedir, "game", "mod_patches.rpa")
            ):
                archives.append("mod_patches")

        archives.reverse()

        return archives

    def assign_docker_files_to_script(self):
        """
        Assigns only Ren'Py, DDMD and Mod Files to Ren'Py to load.
        """
        if self.running_renpy_sdk():
            return renpy.game.script.script_files

        if self.ddlc_mode:
            return [x for x in renpy.game.script.script_files if "mods/" not in x[0]]

        mods_set = set()

        # Make sure we add the needed DDMD files
        ddmd_files = [
            "mod_installer",
            "mod_services",
            "mod_screen",
            "mod_settings",
            "ml_patches",
            "mod_content",
            "mod_dir_browser",
            "mod_list",
            "mod_prompt",
            "mod_styles",
            "mod_transforms",
            "saves",
        ]

        for renpy_file, archive_path in renpy.game.script.script_files:
            if renpy_file in ddmd_files or (
                archive_path is not None and "renpy/" in archive_path.replace("\\", "/")
            ):
                temp_tuple = (renpy_file, archive_path)
                mods_set.add(temp_tuple)

        for renpy_file, archive_path in renpy.game.script.script_files:
            temp_tuple = (renpy_file, archive_path)
            if "mods/{}/".format(self.mod_name) in renpy_file:
                mods_set.add(temp_tuple)
            elif archive_path is None and renpy_file.split("/")[-1] not in [
                existing_renpy_file.split("/")[-1]
                for existing_renpy_file, x in mods_set
            ]:
                mods_set.add(temp_tuple)

        return list(mods_set)

    def verify_setting_integrity(self):
        """
        Makes sure the mod list and settings file are in-tact and loads the configured settings.
        """
        if self.running_renpy_sdk():
            return

        settings_path = os.path.join(renpy.config.basedir, "ddmd_settings.json")
        ddmc_json_path = os.path.join(renpy.config.basedir, "game", "ddmc.json")

        if not os.path.isfile(settings_path):
            with open(settings_path, "wb") as ddmd_settings:
                ddmd_settings.write(
                    renpy.exports.file("sdc_system/backups/settings.backup").read()
                )

        if not os.path.isfile(ddmc_json_path):
            with open(ddmc_json_path, "wb") as ddmc_json:
                ddmc_json.write(
                    renpy.exports.file("sdc_system/backups/ddmc.backup").read()
                )

        with open(settings_path, "r") as ddmd_settings:
            ddmd_configuration = json.load(ddmd_settings)

        renpy.config.gl2 = ddmd_configuration.get("config_gl2", False)

    def finalize(self):
        """
        Sets the base directory to the mod to avoid Ren'Py conflicts.
        """
        if self.running_renpy_sdk():
            return

        renpy.store.persistent.ddml_basedir = renpy.config.basedir.replace("\\", "/")
        if not self.ddlc_mode:
            renpy.config.basedir = os.path.join(
                renpy.config.basedir, "game/mods", self.mod_name
            )
