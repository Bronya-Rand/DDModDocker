
init python in ddmd_mod_installer:
    from store import persistent
    from zipfile import ZipFile
    import os
    import shutil
    import tempfile

    tempFolderName = ""

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

    def inInvalidDir(path):
        for x in ("lib", "renpy"):
            if x + "/" in path.replace("\\", "/"):
                return True
        return False

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
                if not copy:
                    if not valid_zip(zipPath):
                        raise Exception("Given ZIP file is a invalid DDLC Mod ZIP Package. Please select a different ZIP file.")
                        return

                    mod_dir = tempfile.mkdtemp(prefix="NewDDML_", suffix="_TempArchive")

                    with ZipFile(zipPath, "r") as tempzip:
                        tempzip.extractall(mod_dir)

                else:
                    validMod = False
                    for mod_src, dirs, files in os.walk(zipPath):
                        for mod_f in files:
                            if mod_f.endswith((".rpa", ".rpyc", ".rpy")):
                                validMod = True
                    if validMod:
                        mod_dir = zipPath
                    else:
                        raise Exception("Given Mod Folder is a invalid DDLC Mod Folder Package. Please select a different mod folder.")
                        return

                os.makedirs(folderPath)
                os.makedirs(os.path.join(folderPath, "game"))

                for mod_src, dirs, files in os.walk(mod_dir):
                    dst_dir = mod_src.replace(mod_dir, folderPath)
                    for d in dirs:
                        if d == "characters":
                            shutil.move(os.path.join(mod_src, d), os.path.join(dst_dir, d))
                    for f in files:
                        if f.endswith((".rpa", ".rpyc", ".rpy")):
                            if not inInvalidDir(mod_src):
                                mod_dir = mod_src
                                break

                for mod_src, dirs, files in os.walk(mod_dir):
                    dst_dir = mod_src.replace(mod_dir, folderPath + "/game")
                    for mod_d in dirs:
                        shutil.move(os.path.join(mod_src, mod_d), os.path.join(dst_dir, mod_d))
                    for mod_f in files:
                        shutil.move(os.path.join(mod_src, mod_f), os.path.join(dst_dir, mod_f))

                renpy.hide_screen("ddmd_progress")
                renpy.show_screen("ddmd_dialog", message="%s has been installed successfully." % tempFolderName)
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
            tempFolderName = ""