
init python in ddmd_mod_installer:
    from store import persistent
    from zipfile import ZipFile, BadZipFile
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

        with os.scandir(mod_dir) as entries:
            for entry in entries:
                if entry.is_dir():
                    top_level_folder = entry.name
                    break
        
        return top_level_folder
    
    def identify_mod_format(mod_dir):
        """
        Identifies the format of the mod package based on its content and structure.

        mod_dir: The path to the mod package directory.
        Returns: A string indicating the format of the mod package.
        """
        top_level_folder = get_top_level_folder(mod_dir)

        if top_level_folder is not None:      
            if os.path.isdir(os.path.join(mod_dir, top_level_folder, "characters")) and os.path.isdir(os.path.join(mod_dir, top_level_folder, "game")):
                return 1  # Standard Format
            elif os.path.isdir(os.path.join(mod_dir, top_level_folder, "game")):
                return 2  # Standard Format (No Characters Folder)
        if os.path.isdir(os.path.join(mod_dir, "characters")) and os.path.isdir(os.path.join(mod_dir, "game")):
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
            for entry in os.scandir(mod_dir_path):
                if entry.is_file():
                    shutil.move(entry.path, game_folder_path)
                elif entry.is_dir():
                    shutil.move(entry.path, os.path.join(game_folder_path, entry.name))

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
            except BadZipFile:
                renpy.hide_screen("ddmd_progress")
                renpy.show_screen("ddmd_dialog", message="Error: Invalid ZIP file. Please select a different ZIP file.")
            except OSError as err:
                if os.path.exists(folderPath):
                    shutil.rmtree(folderPath)
                renpy.hide_screen("ddmd_progress")
                renpy.show_screen("ddmd_dialog", message="A error has occured during installation.", message2=str(err))
            except Exception as err:
                if os.path.exists(folderPath):
                    shutil.rmtree(folderPath)
                renpy.hide_screen("ddmd_progress")
                renpy.show_screen("ddmd_dialog", message="A error has occured during installation.", message2=str(err))
