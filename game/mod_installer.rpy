
init python in ddmd_mod_installer:
    from store import persistent
    from zipfile import ZipFile, BadZipfile
    import os
    import shutil
    import tempfile

    def inInvalidDir(path):
        for x in ("lib", "renpy"):
            if os.path.normpath(x) in os.path.normpath(path):
                return True
        if path.endswith(".app"):
            return True
        return False

    def check_mod_validity(zipPath, copy):
        """
        Checks mod validity for mod packages and ZIP files.

        filePath: The direct path to the ZIP file.
        Returns: A boolean indicating a valid mod ZIP file.
        """
        if not copy:
            # ZIP file check
            with ZipFile(zipPath, "r") as temp_zip:
                zip_contents = temp_zip.namelist()

            mod_files = zip_contents
        else:
            # Folder check
            mod_files = []

            for mod_src, dirs, files in os.walk(zipPath):
                for mod_f in files:
                    mod_files.append(os.path.join(mod_src, mod_f))

        # Check if mod files contain Ren'Py files
        if any(file.endswith((".rpa", ".rpyc", ".rpy")) for file in mod_files):
            return True
        return False

    def get_top_level_folder(mod_dir):
        """
        Get's the top level folder of a mod archive if available.

        mod_dir: The path to the ZIP temp folder or mod folder package.
        Returns: A string of the top level folder or NoneType.
        """
        top_level_folder = None

        for entry in os.listdir(mod_dir):
            if os.path.isdir(os.path.join(mod_dir, entry)):
                top_level_folder = entry
                break

        return top_level_folder

    def identify_mod_format(mod_dir):
        """
        Identifies the format of the mod package based on its content and structure.

        mod_dir: The path to the mod package directory.
        Returns: An integer indicating the format of the mod package.
        """

        # Check for top-level folder
        top_level_folder = get_top_level_folder(mod_dir)

        # Standard Format
        if top_level_folder is not None:
            if os.path.isdir(os.path.join(mod_dir, top_level_folder, "characters")) and os.path.isdir(os.path.join(mod_dir, top_level_folder, "game")):
                return 1
            elif os.path.isdir(os.path.join(mod_dir, top_level_folder, "game")):
                return 2

        # Standard Format without top folder
        if os.path.isdir(os.path.join(mod_dir, "characters")) and os.path.isdir(os.path.join(mod_dir, "game")):
            return 3

        # Check for game folder and RPAs/RPYC/RPY files
        game_dir = os.path.join(mod_dir, "game")
        if os.path.isdir(game_dir):
            if any(f.endswith((".rpa", ".rpyc", ".rpy")) for f in os.listdir(game_dir)):
                return 5
            else:
                return 4

        # Check for RPAs without game folder
        if any(f.endswith(".rpa") for f in os.listdir(mod_dir)):
            return 6

        # Check for RPYC/RPY files without game folder
        mod_assets_dir = os.path.join(mod_dir, "mod_assets")
        if os.path.isdir(mod_assets_dir) or any(f.endswith((".rpyc", ".rpy")) for f in os.listdir(mod_dir)):
            return 7

        # Unknown Format
        return -1

    def extract_mod_from_zip(zipPath):
        """
        Extracts a Mod ZIP package to a temporary folder

        mod_dir: The path to the mod package directory.
        Returns: A string path to the temp folder or NoneType
        """
        mod_dir = tempfile.mkdtemp(prefix="NewDDML_", suffix="_TempArchive")

        try:
            with ZipFile(zipPath, "r") as tempzip:
                tempzip.extractall(mod_dir)
            return mod_dir
        except BadZipFile:
            shutil.rmtree(mod_dir)
            return None

    def move_mod_files(mod_folder_path, mod_dir_path, mod_format_id, copy):
        """
        Moves or copies the mod files from the mod directory or mod package folder to the mod folder.

        mod_folder_path: Path to the mod folder.
        mod_dir_path: Path to the mod directory or mod package folder.
        mod_format_id: Integer value indicating the mod format ID.
        copy: Boolean value indicating whether to copy the files (macOS only).
        """

        if mod_format_id in (1, 2, 3, 4, 5):
            characters_dir = os.path.join(mod_dir_path, "characters")
            game_dir = os.path.join(mod_dir_path, "game")

            # Copy or move characters folder (if applicable)
            if os.path.isdir(characters_dir):
                if copy:
                    shutil.copytree(characters_dir, mod_folder_path)
                else:
                    shutil.move(characters_dir, mod_folder_path)

            # Copy or move game folder to mod_folder_path
            if copy:
                shutil.copytree(game_dir, mod_folder_path)
            else:
                shutil.move(game_dir, mod_folder_path)

        elif mod_format_id in (6, 7):
            game_folder_path = os.path.join(mod_folder_path, "game")

            # Create game folder if it doesn't exist
            if not os.path.exists(game_folder_path):
                os.makedirs(game_folder_path)

            # Move all files from mod_dir_path to game folder in mod_folder_path
            for entry in os.listdir(mod_dir_path):
                entry_path = os.path.join(mod_dir_path, entry)

                if os.path.isfile(entry_path):
                    shutil.move(entry_path, game_folder_path)
                elif os.path.isdir(entry_path):
                    shutil.move(entry_path, os.path.join(game_folder_path, entry))

    def install_mod(zipPath, modFolderName, copy=False):
        if not modFolderName:
            renpy.show_screen("ddmd_dialog", message="Error: The folder name cannot be blank.")
            return
        elif modFolderName.lower() in ("ddlc mode", "stock mode", "ddlc", "stock"):
            renpy.show_screen("ddmd_dialog", message="Error: %s is a reserved folder name. Please try another folder name." % modFolderName)
            return
        elif os.path.exists(os.path.join(persistent.ddml_basedir, "game/mods/" + modFolderName)):
            renpy.show_screen("ddmd_dialog", message="Error: This mod folder already exists. Please try another folder name.")
            return
        else:
            renpy.show_screen("ddmd_progress", message="Installing mod. Please wait.")
            folderPath = os.path.join(persistent.ddml_basedir, "game/mods", modFolderName)
            try:
                if not check_mod_validity(zipPath, copy):
                    raise Exception("Given file/folder is an invalid DDLC Mod Package. Please select a different file/folder.")
                
                if not copy:
                    mod_dir = extract_mod_from_zip(zipPath)
                    if mod_dir is None:
                        raise Exception("Invalid mod structure. Please select a different ZIP file.")
                else:
                    mod_dir = zipPath

                mod_format_id = identify_mod_format(mod_dir)
                print("Mod Format ID: %d" % mod_format_id)
                if mod_format_id == -1:
                    raise Exception("Mod is packaged in a way that is unknown to DDMD. Re-download the mod that follows a proper DDLC mod package standard or contact 'bronya_rand' with the mod in question.")
                
                os.makedirs(folderPath)

                if mod_format_id in (1, 2):
                    top_level_folder = get_top_level_folder(mod_dir)
                    mod_dir_path = os.path.join(mod_dir, top_level_folder)
                    move_mod_files(folderPath, mod_dir_path, mod_format_id, copy)
                else:
                    move_mod_files(folderPath, mod_dir, mod_format_id, copy)
                
                renpy.hide_screen("ddmd_progress")
                renpy.show_screen("ddmd_dialog", message="%s has been installed successfully." % modFolderName)
                modFolderName = ""
            except BadZipfile:
                renpy.hide_screen("ddmd_progress")
                renpy.show_screen("ddmd_dialog", message="Error: Invalid ZIP file. Please select a different ZIP file.")
            except OSError as err:
                if os.path.exists(folderPath):
                    shutil.rmtree(folderPath)
                renpy.hide_screen("ddmd_progress")
                renpy.show_screen("ddmd_dialog", message="An error has occured during installation.", message2=str(err))
            except Exception as err:
                if os.path.exists(folderPath):
                    shutil.rmtree(folderPath)
                renpy.hide_screen("ddmd_progress")
                renpy.show_screen("ddmd_dialog", message="An unexpected error has occured during installation.", message2=str(err))