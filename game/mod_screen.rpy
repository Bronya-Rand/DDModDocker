## Copyright 2022 Azariel Del Carmen (GanstaKingofSA)

init python:
    import os
    import json
    import threading
    from time import sleep
    import subprocess
    import tempfile
    from zipfile import ZipFile
    import shutil

    current_mod_list = []
    selectedMod = None
    loadedMod = None

    config.keymap['mod_overlay'] = ['K_F9']
    config.underlay.append(
        renpy.Keymap(
        mod_overlay = renpy.curried_call_in_new_context("_mod_overlay")
        )
    )

    class Mod:
        def __init__(self, modFolderName, path):
            self.modFolderName = modFolderName
            self.path = path

    class SteamLikeOverlay():
        def __init__(self):
            thread = threading.Thread(target=self.run)
            thread.start()
        
        def show_notif(self):
            renpy.display.screen.show_screen("steam_like_overlay", "Access the Mod Docker menu while playing.", 
                "Press: " + config.keymap['mod_overlay'][0].replace("K_", ""))
        
        def run(self):
            sleep(1.5)
            self.show_notif()

    start_overlay = SteamLikeOverlay()

    def get_mod_json():
        try:
            with open(persistent.ddml_basedir + "/selectedmod.json", "r") as mod_json:
                temp = json.load(mod_json)
                return temp['modName']
        except:
            return "DDLC"

    selectedMod = get_mod_json()
    loadedMod = selectedMod

    def get_ddmc_modlist():
        with renpy.file("ddmc.json") as mod_json:
            return json.load(mod_json)

    def get_mod_list():
        templist = []
        for modfolder in os.listdir(persistent.ddml_basedir + "/game/mods"):
            if not os.path.exists(persistent.ddml_basedir + "/game/mods/" + modfolder + "/game"):
                continue
                
            modfolderpath = persistent.ddml_basedir + "/game/mods/" + modfolder + "/game"

            ddlcMod = False
            for x in os.listdir(modfolderpath):
                if x.endswith((".rpa", ".rpyc", ".rpy")):
                    ddlcMod = True
            
            if ddlcMod:
                temp = Mod(modfolder, modfolderpath)
                templist.append(temp)
        
        return templist

    def loadMod(x, folderName):
        isRPA = False
        
        for root, dirs, files in os.walk(x + "/game"):
            for f in files:
                if f.endswith(".rpa"):
                    isRPA = True
        
        mod_dict = {
            "modName": folderName,
            "isRPA": isRPA,
        }
        
        with open(persistent.ddml_basedir + "/selectedmod.json", "w") as j:
            json.dump(mod_dict, j)
        
        renpy.show_screen("ddmd_dialog", message="Selected %s as the loadable mod. You must restart Mod Docker in order to load the mod." % folderName)

    def clearMod():
        if os.path.exists(persistent.ddml_basedir + "/selectedmod.json"):
            os.remove(persistent.ddml_basedir + "/selectedmod.json")
        
            if renpy.version_tuple == (6, 99, 12, 4, 2187):
                renpy.show_screen("ddmd_dialog", message="Returned to DDLC mode. You must restart Mod Docker in order to load the mod.")
            else:
                renpy.show_screen("ddmd_dialog", message="Returned to stock mode. You must restart Mod Docker in order to apply these settings.")
        else:
            if renpy.version_tuple == (6, 99, 12, 4, 2187):
                renpy.show_screen("ddmd_dialog", message="Error: You are already in DDLC Mode.")
            else:
                renpy.show_screen("ddmd_dialog", message="Error: You are already in stock mode.")

    def open_save_dir():
        if renpy.windows:
            os.startfile(persistent.ddml_basedir + "/game/MLSaves")
        elif renpy.macintosh:
            subprocess.Popen([ "open", persistent.ddml_basedir + "/game/MLSaves" ])
        else:
            subprocess.Popen([ "xdg-open", persistent.ddml_basedir + "/game/MLSaves" ])

    def open_dir(path):
        if renpy.windows:
            os.startfile(path)
        elif renpy.macintosh:
            subprocess.Popen([ "open", path ])
        else:
            subprocess.Popen([ "xdg-open", path ])

    def set_settings_json():
        temp = [
            {
            "config_gl2": config.gl2
            }
        ]
        with open(persistent.ddml_basedir + "/ddmd_settings.json", "w") as ddmd_settings:
            json.dump(temp, ddmd_settings)

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
                if not valid_zip(zipPath):
                    raise Exception("Given ZIP file is a invalid DDLC Mod ZIP Package. Please select a different ZIP file.")
                    return

                os.makedirs(folderPath)
                os.makedirs(os.path.join(folderPath, "game"))

                if not copy:
                    mod_dir = tempfile.mkdtemp(prefix="NewDDML_", suffix="_TempArchive")

                    with ZipFile(zipPath, "r") as tempzip:
                        tempzip.extractall(mod_dir)
                    
                else:
                    mod_dir = zipPath

                for mod_src, dirs, files in os.walk(mod_dir):
                    dst_dir = mod_src.replace(mod_dir, folderPath)
                    for d in dirs:
                        if d == "characters":
                            shutil.move(os.path.join(mod_src, d), os.path.join(dst_dir, d))
                    for f in files:
                        if f.endswith((".rpa", ".rpyc", ".rpy")):
                            if not f.startswith("00"):
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
                tempFolderName = ""
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
    
    def delete_mod(mod):
        try:
            shutil.rmtree(persistent.ddml_basedir + "/game/mods/" + mod)
            renpy.show_screen("ddmd_dialog", message="Successfully removed %s from Mod Docker." % mod)
        except Exception as err:
            renpy.show_screen("ddmd_dialog", message="A error occured while removing %s." % mod, message2=str(err))

    def delete_saves(mod):
        try:
            shutil.rmtree(persistent.ddml_basedir + "/game/MLSaves/" + mod)
            renpy.show_screen("ddmd_dialog", message="Successfully removed %s save data from Mod Docker." % mod)
        except OSError as err:
            if e.errno == 3:
                renpy.show_screen("ddmd_dialog", message="No save files were found. You might have deleted the saves already or not launched this mod yet.")
        except Exception as err:
            renpy.show_screen("ddmd_dialog", message="A error occured while removing %s save data." % mod, message2=str(err))

screen mods():
    zorder 100

    fixed at ml_overlay_effect:
        style_prefix "mods"

        if os.path.exists(persistent.ddml_basedir + "/game/docker_custom_image.png"):
            add persistent.ddml_basedir + "/game/docker_custom_image.png" xsize 1280 ysize 720
        else:
            add "game_menu_bg"
        add Transform("#000", alpha=0.8) xsize 365
        add Transform("#202020", alpha=0.5) xpos 0.28

        vbox:
            label _("Select a Mod")

            side "c":
                xpos 50
                xsize 250
                ysize 450

                viewport id "mlvp":
                    mousewheel True
                    has vbox:

                        spacing 6

                    button:
                        action [SetVariable("selectedMod", "DDLC"), SensitiveIf(selectedMod != "DDLC")]

                        add If(loadedMod == "DDLC", Composite((310, 50), (0, 1), "ddmd_selectedmod_icon", 
                            (38, 0), Text(If(renpy.version_tuple == (6, 99, 12, 4, 2187), "DDLC Mode", 
                            "Stock Mode"), style="mods_button_text")), Text(If(renpy.version_tuple == (6, 99, 12, 4, 2187), 
                            "DDLC Mode", "Stock Mode"), style="mods_button_text"))

                    python:
                        global current_mod_list
                        current_mod_list = get_mod_list()

                    for x in current_mod_list:
                        button:
                            action [SetVariable("selectedMod", x.modFolderName), SensitiveIf(x.modFolderName != selectedMod)]
                            
                            add If(loadedMod == x.modFolderName, Composite((210, 50), (0, 1), "ddmd_selectedmod_icon", 
                                (38, 0), Text(x.modFolderName, style="mods_button_text", substitute=False)), 
                                Text(x.modFolderName, style="mods_button_text", substitute=False))

        hbox:
            style "mods_return_button"
            vbox:
                imagebutton:
                    idle "ddmd_return_icon"
                    hover "ddmd_return_icon_hover"
                    hovered Show("mods_hover_info", about="Exit the DDMD Menu")
                    unhovered Hide("mods_hover_info")
                    action [Return(0), With(Dissolve(0.5))]
            null width 10
            vbox:
                imagebutton:
                    idle "ddmd_install_icon"
                    hover "ddmd_install_icon_hover"
                    hovered Show("mods_hover_info", about="Install a Mod")
                    unhovered Hide("mods_hover_info")
                    action [Hide("mods_hover_info"), If(renpy.macintosh and not persistent.macos_zip_warn, [Show("ddmd_dialog", "As of now, Mod Docker only supports Mod ZIP packages. Downloading mods via Safari may auto-extract these ZIP files and requires them to be re-zipped."), SetField(persistent, "macos_zip_warn", True), Show("pc_directory", Dissolve(0.25))], Show("pc_directory", Dissolve(0.25)))]
            null width 10
            vbox:
                imagebutton:
                    idle "ddmd_search_icon"
                    hover "ddmd_search_icon_hover"
                    hovered Show("mods_hover_info", about="Browse the Mod List!")
                    unhovered Hide("mods_hover_info")
                    action If(not persistent.mod_list_disclaimer_accepted, 
                    [Hide("mods_hover_info"), Show("ddmd_confirm", message="Disclaimer", message2="This mod list source is provided by the defunct Doki Doki Mod Club site. Not all mods may be on here while others may be out-of-date. By accepting this prompt, you acknoledge to the following disclaimer above.", 
                        yes_action=[SetField(persistent, "mod_list_disclaimer_accepted", True), Hide("ddmd_confirm", Dissolve(0.25)), 
                        Show("mod_list", Dissolve(0.25))], no_action=Hide("ddmd_confirm", Dissolve(0.25)))], 
                        Show("mod_list", Dissolve(0.25)))
            null width 10
            vbox:
                imagebutton:
                    idle "ddmd_restart_icon"
                    hover "ddmd_restart_icon_hover"
                    hovered Show("mods_hover_info", about="Quits DDMD")
                    unhovered Hide("mods_hover_info")
                    action Quit()

        vbox:
            hbox:
                viewport id "modinfoname":
                    xpos 450
                    ypos 50
                    xsize 700
                    if selectedMod == "DDLC" and renpy.version_tuple > (6, 99, 12, 4, 2187):
                        label "Stock Mode"
                    elif selectedMod == "DDLC" and renpy.version_tuple == (6, 99, 12, 4, 2187):
                        label "DDLC Mode"
                    else:
                        label "[selectedMod]"
                bar value XScrollValue("modinfoname")

        vbox:
            xpos 0.31
            ypos 0.25
            label "Options"
            vbox:
                xpos 0.2
                yoffset -20
                textbutton "Open Save Directory" action Function(open_save_dir)
                if loadedMod != "DDLC":
                    textbutton "Open Selected Mod's Game Directory" action Function(open_dir, config.gamedir)
                textbutton "Open Mod Docker's Game Directory" action Function(open_dir, persistent.ddml_basedir + "/game")
                if selectedMod != loadedMod and selectedMod != "DDLC":
                    textbutton "Delete Mod" action Function(delete_mod, selectedMod)
                if selectedMod != loadedMod:
                    textbutton "Delete Saves" action Function(delete_saves, selectedMod)
                if selectedMod == loadedMod and selectedMod != "DDLC":
                    imagebutton:
                        idle ConditionSwitch("config.gl2", Composite((250, 50), (0, 0), "ddmd_toggle_on",
                            (55, 7), Text("Enable OpenGL 2", style="mods_text")), "True",
                            Composite((250, 50), (0, 0), "ddmd_toggle_off", (55, 7), 
                            Text("Enable OpenGL 2", style="mods_text")))
                        hover ConditionSwitch("config.gl2", Composite((250, 50), (0, 0), "ddmd_toggle_on_hover",
                            (55, 7), Text("Enable OpenGL 2", style="mods_text")), "True", 
                            Composite((250, 50), (0, 0), "ddmd_toggle_off_hover", (55, 7), Text("Enable OpenGL 2", 
                            style="mods_text")))
                        action If(config.gl2, Show("ddmd_confirm", Dissolve(0.25), message="Disable OpenGL 2?", 
                            message2="This mod may not have certain effects display if this setting is turned off. {b}A restart is required to load OpenGL 2{/b}.", 
                            yes_action=[SetField(config, "gl2", False), Function(set_settings_json), Quit()], no_action=Hide("ddmd_confirm", 
                            Dissolve(0.25))), Show("ddmd_confirm", Dissolve(0.25), message="Enable OpenGL 2?", 
                            message2="This mod may suffer from broken affects if this setting is turned on. {b}A restart is required to load OpenGL 2{/b}.", 
                            yes_action=[SetField(config, "gl2", True), Function(set_settings_json), Quit()], no_action=Hide("ddmd_confirm", 
                            Dissolve(0.25))))

        vbox:
            xpos 0.9
            ypos 0.9
            textbutton "Select" action If(selectedMod == "DDLC", Function(clearMod), Function(loadMod, persistent.ddml_basedir + "/game/mods/" + selectedMod, selectedMod))

    key "K_ESCAPE" action Return(0)

label _mod_overlay:

    $ renpy.call_screen("mods")
    return

init -1:
    screen steam_like_overlay(message, message2):

        zorder 200
        style_prefix "steam"

        frame at steam_effect:
            xsize 200
            ysize 100
            xalign 1.0
            yalign 1.0
            
            vbox:
                xalign 0.5
                yalign 0.15
                text message size 16
            vbox:
                xalign 0.5
                yalign 0.9
                text message2 size 16
                

        timer 3.25 action Hide('steam_like_overlay')

    style steam_frame:
        background Frame("sdc_system/ddmd_app/steam_frame.png", left=4, top=4, bottom=4, right=4, tile=False)

    style steam_text:
        color "#fff"
        outlines []

    transform steam_effect:
        subpixel True
        on show:
            ycenter 800 yanchor 1.0 alpha 1.00 nearest True
            easein .45 ycenter 670
        on hide:
            easein .45 ycenter 800 nearest True

screen mods_hover_info(about):
    zorder 101
    style_prefix "mods_hover"

    python:
        currentpos = renpy.get_mouse_pos()
    
    frame at windows_like_effect:
        xpos currentpos[0]
        ypos currentpos[1] + 15
        xsize 150

        text _(about)
