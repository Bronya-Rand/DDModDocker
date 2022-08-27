## Copyright 2022 Azariel Del Carmen (GanstaKingofSA)

python early:
    import os
    import json
    import threading
    from time import sleep
    import subprocess
    import tempfile
    from zipfile import ZipFile
    import shutil
    import datetime

init -1000 python:

    def _mod_overlay():
        renpy.show_screen("mods")
        renpy.restart_interaction()

    config.keymap['mod_overlay'] = ['K_F9']
    config.underlay.append(
        renpy.Keymap(
        mod_overlay = _mod_overlay
        )
    )

init python:
    current_mod_list = []
    selectedMod = None
    loadedMod = None

    class Mod:
        def __init__(self, modFolderName, path):
            self.modFolderName = modFolderName
            self.path = path

    class SteamLikeOverlay():
        def __init__(self):
            thread = threading.Thread(target=self.run)
            thread.start()
        
        def show_notif(self):
            renpy.display.screen.show_screen("steam_like_overlay", _("Access the Mod Docker menu while playing."), 
                _("Press: ") + config.keymap['mod_overlay'][0].replace("K_", ""))
        
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
        if loadedMod == folderName:
            renpy.show_screen("ddmd_dialog", message="Error: %s is already the selected mod." % folderName)
            return
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
            if err.errno == 2:
                renpy.show_screen("ddmd_dialog", message="No save files were found. You might have deleted the saves already or not launched this mod yet.")
            else:
                renpy.show_screen("ddmd_dialog", message="A error occured while removing %s save data." % mod, message2=str(err))
        except Exception as err:
            renpy.show_screen("ddmd_dialog", message="A error occured while removing %s save data." % mod, message2=str(err))

    def get_current_time(st, at):
        if persistent.military_time:
            return Text(datetime.datetime.now().strftime("%H:%M"), style="time_text"), 1.0
        else:
            return Text(datetime.datetime.now().strftime("%I:%M %p"), style="time_text"), 1.0

    # For > 720p resolutions
    def get_dsr_scale():
        return (config.screen_width / 1280.0)

    res_scale = get_dsr_scale()

screen mods():
    zorder 100
    modal True

    fixed at ml_overlay_effect:
        style_prefix "mods"

        
        if os.path.exists(persistent.ddml_basedir + "/game/docker_custom_image.png"):
            add persistent.ddml_basedir + "/game/docker_custom_image.png" xsize config.screen_width ysize config.screen_height
        elif os.path.exists(persistent.ddml_basedir + "/game/docker_custom_image.jpg"):
            add persistent.ddml_basedir + "/game/docker_custom_image.jpg" xsize config.screen_width ysize config.screen_height
        else:
            add "game_menu_bg" 

        add Transform("#000", alpha=0.8) xsize int(365 * res_scale)
        add Transform("#202020", alpha=0.5) xpos 0.28

        vbox:
            label _("Select a Mod")

            side "c":
                xpos int(50 * res_scale)
                xsize int(250 * res_scale)
                ysize int(450 * res_scale)

                viewport id "mlvp":
                    mousewheel True
                    has vbox
                    spacing int(9 * res_scale)

                    button:
                        action [SetVariable("selectedMod", "DDLC"), SensitiveIf(selectedMod != "DDLC")]

                        add If(loadedMod == "DDLC", Composite((int(310 * res_scale), int(50 * res_scale)), (0, int(1 * res_scale)), Transform("ddmd_selectedmod_icon", size=(int(36 * res_scale), int(36 * res_scale))), 
                            (int(38 * res_scale), 0), Text(If(renpy.version_tuple == (6, 99, 12, 4, 2187), "DDLC Mode", 
                            _("Stock Mode")), style="mods_button_text")), Text(If(renpy.version_tuple == (6, 99, 12, 4, 2187), 
                            _("DDLC Mode"), _("Stock Mode")), style="mods_button_text"))

                    python:
                        global current_mod_list
                        current_mod_list = get_mod_list()

                    for x in current_mod_list:
                        button:
                            action [SetVariable("selectedMod", x.modFolderName), SensitiveIf(x.modFolderName != selectedMod)]
                            
                            add If(loadedMod == x.modFolderName, Composite((int(190 * res_scale), int(50 * res_scale)), (0, int(1 * res_scale)), Transform("ddmd_selectedmod_icon", size=(int(36 * res_scale), int(36 * res_scale))), 
                                (int(38 * res_scale), 0), Text(x.modFolderName, style="mods_button_text", substitute=False)), 
                                Text(x.modFolderName, style="mods_button_text", substitute=False))

        hbox:
            style "mods_return_button"
            vbox:
                imagebutton:
                    idle Transform("ddmd_return_icon", size=(int(48 * res_scale), int(48 * res_scale)))
                    hover Transform("ddmd_return_icon_hover", size=(int(48 * res_scale), int(48 * res_scale)))
                    hovered Show("mods_hover_info", about=_("Exit the DDMD Menu"))
                    unhovered Hide("mods_hover_info")
                    action [Hide("mods_hover_info"), Hide("mods"), With(Dissolve(0.5))]
            null width 10
            vbox:
                imagebutton:
                    idle Transform("ddmd_install_icon", size=(int(48 * res_scale), int(48 * res_scale)))
                    hover Transform("ddmd_install_icon_hover", size=(int(48 * res_scale), int(48 * res_scale)))
                    hovered Show("mods_hover_info", about=_("Install a Mod"))
                    unhovered Hide("mods_hover_info")
                    action [Hide("mods_hover_info"), If(renpy.macintosh and persistent.self_extract is None, 
                        Show("ddmd_confirm", message="ZIP Extraction On?", message2="Does your version of macOS extract ZIP files after downloading?", 
                        yes_action=[SetField(persistent, "self_extract", True), Hide("ddmd_confirm"), Show("pc_directory", Dissolve(0.25), mac=True)], 
                        no_action=[SetField(persistent, "self_extract", False), Hide("ddmd_confirm"), Show("pc_directory", Dissolve(0.25))]), 
                        If(renpy.macintosh and persistent.self_extract, Show("pc_directory", Dissolve(0.25), mac=True), Show("pc_directory", Dissolve(0.25))))]
            null width 10
            vbox:
                imagebutton:
                    idle Transform("ddmd_search_icon", size=(int(48 * res_scale), int(48 * res_scale)))
                    hover Transform("ddmd_search_icon_hover", size=(int(48 * res_scale), int(48 * res_scale)))
                    hovered Show("mods_hover_info", about=_("Browse the Mod List!"))
                    unhovered Hide("mods_hover_info")
                    action Show("ddmd_dialog", message="Mod List Unavailable", message2="The mod list is unavailable in the Ren'Py 8 mode of Mod Docker due to no mod lists for Ren'Py 8 mods. This feature will return when one exists.")
                    # action [Hide("mods_hover_info"), If(not persistent.mod_list_disclaimer_accepted, 
                    #     Show("ddmd_confirm", message="Disclaimer", message2="This mod list source is provided by the defunct Doki Doki Mod Club site. Not all mods may be on here while others may be out-of-date. By accepting this prompt, you acknowledge to the following disclaimer above.", 
                    #     yes_action=[SetField(persistent, "mod_list_disclaimer_accepted", True), Hide("ddmd_confirm"), Show("mod_list", Dissolve(0.25))], 
                    #     no_action=Hide("ddmd_confirm")), Show("mod_list", Dissolve(0.25)))]
            null width 10
            vbox:
                imagebutton:
                    idle Transform("ddmd_settings_icon", size=(int(48 * res_scale), int(48 * res_scale)))
                    hover Transform("ddmd_settings_icon_hover", size=(int(48 * res_scale), int(48 * res_scale)))
                    hovered Show("mods_hover_info", about=_("View DDMD's Settings"))
                    unhovered Hide("mods_hover_info")
                    action [Hide("mods_hover_info"), Show("mod_settings", Dissolve(0.25))]
            null width 10
            vbox:
                imagebutton:
                    idle Transform("ddmd_restart_icon", size=(int(48 * res_scale), int(48 * res_scale)))
                    hover Transform("ddmd_restart_icon_hover", size=(int(48 * res_scale), int(48 * res_scale)))
                    hovered Show("mods_hover_info", about=_("Quit DDMD"))
                    unhovered Hide("mods_hover_info")
                    action Quit()

        vbox:
            hbox:
                if persistent.military_time:
                    xpos config.screen_width - int(105 * res_scale)
                else:
                    xpos config.screen_width - int(130 * res_scale)
                ypos int(25 * res_scale)
                add "ddmd_time_clock"

            hbox:
                viewport id "modinfoname":
                    mousewheel True
                    xpos int(450 * res_scale)
                    ypos int(50 * res_scale)
                    xsize int(700 * res_scale)
                    if selectedMod == "DDLC" and renpy.version_tuple > (6, 99, 12, 4, 2187):
                        label _("Stock Mode")
                    elif selectedMod == "DDLC" and renpy.version_tuple == (6, 99, 12, 4, 2187):
                        label _("DDLC Mode")
                    else:
                        label "[selectedMod]"

        vbox:
            xpos 0.31 
            ypos 0.25 
            label "Options"
            vbox:
                xpos 0.2
                yoffset -20
                textbutton _("Open Save Directory") action Function(open_save_dir)
                if loadedMod != "DDLC":
                    textbutton _("Open Running Mods' Game Directory") action Function(open_dir, config.gamedir)
                textbutton _("Open Mod Docker's Game Directory") action Function(open_dir, persistent.ddml_basedir + "/game")
                if selectedMod != loadedMod and selectedMod != "DDLC":
                    textbutton _("Delete Mod") action Show("ddmd_confirm", message=_("Are you sure you want to remove %s?") % selectedMod, yes_action=[Hide("ddmd_confirm"), Function(delete_mod, selectedMod)], no_action=Hide("ddmd_confirm"))
                if selectedMod != loadedMod:
                    textbutton _("Delete Saves") action Show("ddmd_confirm", message=_("Are you sure you want to remove %s save files?") % selectedMod, yes_action=[Hide("ddmd_confirm"), Function(delete_saves, selectedMod)], no_action=Hide("ddmd_confirm"))

        vbox:
            xpos 0.9
            ypos 0.9
            textbutton _("Select") action If(selectedMod == "DDLC", Function(clearMod), Function(loadMod, persistent.ddml_basedir + "/game/mods/" + selectedMod, selectedMod))

    key "K_ESCAPE" action Hide("mods")

init -1:
    screen steam_like_overlay(message, message2):

        zorder 200
        style_prefix "steam"

        frame at steam_effect:
            xsize int(200 * res_scale)
            ysize int(100 * res_scale)
            xalign 1.0
            yalign 1.0
            
            vbox:
                xalign 0.5
                yalign 0.15
                text message size int(16 * res_scale)
            vbox:
                xalign 0.5
                yalign 0.9
                text message2 size int(16 * res_scale)
                

        timer 3.25 action Hide('steam_like_overlay')

    style steam_frame:
        background Frame("sdc_system/ddmd_app/steam_frame.png", left=4, top=4, bottom=4, right=4, tile=False)

    style steam_text is renpy_generic_text:
        color "#fff"
        outlines []

    transform steam_effect:
        subpixel True
        on show:
            ycenter config.screen_height + int(80 * res_scale) yanchor 1.0 alpha 1.00 nearest True
            easein .45 ycenter config.screen_height - int(50 * res_scale)
        on hide:
            easein .45 ycenter config.screen_height + int(80 * res_scale) nearest True

screen mods_hover_info(about):
    zorder 101
    style_prefix "mods_hover"

    python:
        currentpos = renpy.get_mouse_pos()
    
    frame at windows_like_effect:
        xpos currentpos[0]
        ypos currentpos[1] + 15
        xsize int(150 * res_scale)

        text _(about)
