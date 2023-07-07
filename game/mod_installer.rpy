
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
        top_level_folder = None

        for entry in os.listdir(mod_dir):
            if os.path.isdir(os.path.join(mod_dir, entry)):
                top_level_folder = entry
                break

        return top_level_folder

    def valid_zip(filePath):
        """
        Returns whether the given ZIP file is a valid Ren'Py/DDLC mod ZIP file.

            filePath - the direct path to the ZIP file.
        """
        zip_contents = []

        with ZipFile(filePath, "r") as temp_zip:
            zip_contents = temp_zip.namelist()

        for x in zip_contents:
            if x.endswith((".rpa", ".rpyc", ".rpy")):
                del zip_contents
                return True

        return False

    def identify_mod_format(mod_dir):
        """
        Identifies the format of the mod package based on its content and structure.

        mod_dir: The path to the mod package directory.
        Returns: A string indicating the format of the mod package.
        """
        top_level_folder = get_top_level_folder(mod_dir)
                    
        if os.path.isdir(os.path.join(mod_dir, top_level_folder, "characters")) and os.path.isdir(os.path.join(mod_dir, top_level_folder, "game")):
            return 1  # Standard Format
        elif os.path.isdir(os.path.join(mod_dir, top_level_folder, "game")):
            return 2  # Standard Format (No Characters Folder)
        elif os.path.isdir(os.path.join(mod_dir, "characters")) and os.path.isdir(os.path.join(mod_dir, "game")):
            return 3 # Standard Format without top folder
        elif os.path.isdir(os.path.join(mod_dir, "game")):
            if any(f.endswith((".rpa", ".rpyc", ".rpy")) for f in os.listdir(os.path.join(mod_dir, "game"))):
                return 5  # Possible Format 2 or 4 (game folder with RPAs or RPYC/RPY files)
            else:
                return 4  # Standard Format without top folder (No Characters Folder)
        elif any(f.endswith(".rpa") for f in os.listdir(mod_dir)):
            return 6  # Possible Format 1 (RPAs without game folder)
        elif os.path.isdir(os.path.join(mod_dir, "mod_assets")) or any(f.endswith((".rpyc", ".rpy")) for f in os.listdir(mod_dir)):
            return 7  # Possible Format 3 (RPYC/RPY files without game folder)
        return -1  # Unknown Format

    def extract_mod_from_zip(zipPath):
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
            if copy:
                # Copy characters folder (if applicable)
                if os.path.isdir(characters_dir):
                    shutil.copytree(characters_dir, mod_folder_path)
                # Copy game folder to mod_folder_path
                shutil.copytree(game_dir, mod_folder_path)
            else:
                # Move characters folder (if applicable)
                if os.path.isdir(characters_dir):
                    shutil.move(characters_dir, mod_folder_path)
                # Move game folder to mod_folder_path
                shutil.move(os.path.join(mod_dir_path, "game"), mod_folder_path)
        elif mod_format_id in (6, 7):
            game_folder_path = os.path.join(mod_folder_path, "game")
            # Create game folder in mod_folder_path
            os.makedirs(game_folder_path)
            # Move all files from mod_dir_path to game folder in mod_folder_path
            for entry in os.listdir(mod_dir_path):
                entry_path = os.path.join(mod_dir_path, entry)
                if os.path.isfile(entry_path):
                    shutil.move(entry_path, game_folder_path)
                elif os.path.isdir(entry_path):
                    shutil.move(entry_path, os.path.join(game_folder_path, entry))

    def install_mod(zipPath, copy=False):
        global tempFolderName

        if not tempFolderName:
            renpy.show_screen("ddmd_dialog", message="Error: The folder name cannot be blank.")
            return
        elif tempFolderName.lower() in ("ddlc mode", "stock mode", "ddlc", "stock"):
            tempFolderName = ""
            renpy.show_screen("ddmd_dialog", message="Error: %s is a reserved folder name. Please try another folder name." % tempFolderName)
            return
        elif os.path.exists(os.path.join(persistent.ddml_basedir, "game/mods/" + tempFolderName)):
            tempFolderName = ""
            renpy.show_screen("ddmd_dialog", message="Error: This mod folder already exists. Please try another folder name.")
            return
        else:
            renpy.show_screen("ddmd_progress", message="Installing mod. Please wait.")
            folderPath = os.path.join(persistent.ddml_basedir, "game/mods", tempFolderName)
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
                renpy.show_screen("ddmd_dialog", message="%s has been installed successfully." % tempFolderName)
                tempFolderName = ""
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