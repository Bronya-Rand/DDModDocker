
init python in ddmd_mod_installer:
    from store import persistent
    from zipfile import ZipFile
    import os
    import shutil
    import tempfile

    def inInvalidDir(path):
        for x in ("lib", "renpy"):
            if os.path.normpath(x) in os.path.normpath(path):
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
    
    def extract_mod_from_zip(zipPath, modPath):
        mod_dir = tempfile.mkdtemp(prefix="NewDDML_", suffix="_TempArchive")

        try:
            with ZipFile(zipPath, "r") as tempzip:
                tempzip.extractall(mod_dir)
            return mod_dir
        except BadZipFile:
            shutil.rmtree(mod_dir)
            return None

        with ZipFile(zipPath, "r") as tempzip:
            tempzip.extractall(mod_dir)

    def move_mod_files(mod_dir, folderPath, copy):
        """
        Moves or copies the mod files from the mod directory or mod package folder to the mod folder.
        """
        if copy:
            for dirpath, dirnames, filenames in os.walk(mod_dir):
                if dirpath.endswith("characters"):
                    shutil.copytree(dirpath, folderPath)
                if "game" in dirnames:
                    shutil.copytree(os.path.join(dirpath, "game"), os.path.join(folderPath, "game"))
                else:
                    os.makedirs(os.path.join(folderPath, "game"))
                for filename in filenames:
                    shutil.copy2(os.path.join(dirpath, filename), os.path.join(folderPath, "game", filename))
        else:
            for dirpath, dirnames, filenames in os.walk(mod_dir):
                if dirpath.endswith("characters"):
                    shutil.move(dirpath, folderPath)
                if "game" in dirnames:
                    shutil.move(os.path.join(dirpath, "game"), os.path.join(folderPath, "game"))
                else:
                    os.makedirs(os.path.join(folderPath, "game"))
                for filename in filenames:
                    shutil.move(os.path.join(dirpath, filename), os.path.join(folderPath, "game", filename))

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
                
                os.makedirs(folderPath)
                
                move_mod_files(mod_dir, folderPath, copy)
                
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
