
init 1 python:
    gui.button_height = None
    gui.navigation_spacing = -gui.navigation_spacing

init python:
    import os
    import json
    import threading
    from time import sleep
    import subprocess
    import shutil

    current_mod_list = []
    selectedMod = None

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
            renpy.display.screen.hide_screen("steam_like_overlay")
            renpy.display.screen.show_screen("steam_like_overlay", "Access the DDML menu while playing.\n\n\t\t\t\t\t\t\tPress: "+ config.keymap['mod_overlay'][0].replace("K_", ""))
        
        def run(self):
            sleep(1.5)
            self.show_notif()

    start_overlay = SteamLikeOverlay()
    
    try:
        with open(persistent.ddml_basedir + "/selectedmod.json", "r") as s:
            j = json.load(s)
            selectedMod = j['modName']
    except:
        selectedMod = "DDLC"

    if "DDML.exe" in os.listdir(config.gamedir):
        if not os.path.exists(persistent.ddml_basedir + "/game/mods"):
            os.makedirs(persistent.ddml_basedir + "/game/mods")
        if not os.path.exists(persistent.ddml_basedir + "/game/MLSaves"):
            os.makedirs(persistent.ddml_basedir + "/game/MLSaves")

    def restart():
        renpy.quit(relaunch=True)

    def get_mod_list():
        global selectedMod
        templist = []
        for modfolder in os.listdir(persistent.ddml_basedir + "/game/mods"):
            if os.path.exists(persistent.ddml_basedir + "/game/mods/" + modfolder + "/game"):
                modfolderpath = persistent.ddml_basedir + "/game/mods/" + modfolder + "/game"
            else:
                modfolderpath = persistent.ddml_basedir + "/game/mods/" + modfolder

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

        if not os.path.exists(x + "/game"):
            renpy.show_screen("dialog", message="We were unable to load this mod as this mods' game folder\nis missing in it's directory. Make sure all files are inside a\ngame folder in the mod folder and try again.", ok_action=Hide("dialog"))
            return

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
        
        renpy.show_screen("dialog", message="Successfully selected " + folderName + " as\nthe loadable mod.\nYou must restart DDLC in order to load the mod.", ok_action=Hide("dialog"))

    def clearMod():
        global selectedMod

        s = open(persistent.ddml_basedir + "/selectedmod.json", "w")
        s.close()

        selectedMod = "DDLC"
        
        if renpy.version_tuple == (6, 99, 12, 4, 2187):
            renpy.show_screen("dialog", message="Successfully selected DDLC as the loadable mod.\nYou must restart DDLC in order to load the mod.", ok_action=Hide("dialog"))
        else:
            renpy.show_screen("dialog", message="Returned to stock settings.\nYou must restart DDLC in order to apply these settings.", ok_action=Hide("dialog"))

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

screen mods():
    zorder 100
    
    fixed at ml_overlay_effect:
        style_prefix "mods"
        
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
                    has vbox

                    spacing 6

                    if renpy.version_tuple == (6, 99, 12, 4, 2187):
                        textbutton "DDLC":
                            action [Function(clearMod), SensitiveIf(selectedMod != "DDLC")]
                    else:
                        textbutton "Stock":
                            action [Function(clearMod), SensitiveIf(selectedMod != "DDLC")]

                    python:
                        global current_mod_list
                        current_mod_list = get_mod_list()

                    for x in current_mod_list:
                        textbutton "[x.modFolderName!q]":
                            action [SetVariable("selectedMod", x.modFolderName), SensitiveIf(x.modFolderName != selectedMod)]

        hbox:
            style "mods_return_button"
            vbox:
                textbutton _("Return"):
                    action [Return(0), With(Dissolve(0.5))]
            vbox:
                textbutton _("Restart"):
                    action Function(restart)

        vbox:
            hbox:
                viewport id "modinfoname":
                    xpos 450
                    ypos 50
                    xsize 700
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
                textbutton "Open Game Directory" action Function(open_dir, config.gamedir)
                textbutton "Open DDML Game Directory" action Function(open_dir, persistent.ddml_basedir + "/game")

                if not config.gl2:
                    textbutton "Enable OpenGL 2":
                        action Show("confirm", message="Are you sure you want to enable OpenGL 2?\nSome mods may suffer from broken affects if this setting is on.\n\n{b}A restart is required to load OpenGL 2{/b}", yes_action=[SetField(config, "gl2", True), Function(restart)] , no_action=Hide("confirm"))
                else:
                    textbutton "Disable OpenGL 2":
                        action Show("confirm", message="Are you sure you want to disable OpenGL 2?\nSome mods may not have certain effects if this setting is off.\n\n{b}A restart is required to load OpenGL 2{/b}", yes_action=[SetField(config, "gl2", False), Function(restart), Hide("confirm")] , no_action=Hide("confirm"))
        vbox:
            xpos 0.9
            ypos 0.9
            textbutton "Select" action Function(loadMod, persistent.ddml_basedir + "/game/mods/" + selectedMod, selectedMod)

style mods_viewport is gui_viewport
style mods_button is gui_button
style mods_button_text is gui_button_text

style mods_label is gui_label
style mods_label_text is gui_label_text

style mods_label:
    xpos 50
    ysize 120

style mods_button:
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style mods_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size gui.title_text_size
    color "#fff"
    outlines [(6, "#803366", 0, 0), (3, "#803366", 2, 2)]
    yalign 0.5

style mods_info_label is mods_label
style mods_info_label_text is mods_label_text

style mods_info_label:
    ypos 0.5
    
style mods_button_text:
    font "gui/font/RifficFree-Bold.ttf"
    color "#fff"
    outlines [(4, "#803366", 0, 0), (2, "#803366", 2, 2)]
    hover_outlines [(4, "#bb4c96", 0, 0), (2, "#bb4c96", 2, 2)]
    insensitive_outlines [(4, "#f374c9", 0, 0), (2, "#f374c9", 2, 2)]

style mods_return_button is gui_button
style mods_return_button_text is gui_button_text

style mods_return_button:
    xpos 80
    yalign 1.0
    yoffset -30

style mods_return_button_text:
    outlines [(4, "#803366", 0, 0), (2, "#803366", 2, 2)]
    hover_outlines [(4, "#bb4c96", 0, 0), (2, "#bb4c96", 2, 2)]
    insensitive_outlines [(4, "#f374c9", 0, 0), (2, "#f374c9", 2, 2)]

label _mod_overlay:

    $ renpy.call_screen("mods")
    return

transform ml_overlay_effect:
    on show:
        alpha 0.0
        linear 0.5 alpha 1.0

init -1:
    screen steam_like_overlay(message):

        zorder 200
        style_prefix "steam"

        frame at steam_effect:
            xsize 200
            ysize 100
            xalign 1.0
            yalign 1.0

            vbox:
                xalign 0.5
                yalign 0.5
                text message size 16 

        timer 3.25 action Hide('steam_like_overlay')

    style steam_frame is frame
    style steam_text:
        color "#000"
        outlines []

    transform steam_effect:
        subpixel True
        on show:
            ycenter 800 yanchor 1.0 alpha 1.00 nearest True
            easein .45 ycenter 670
        on hide:
            easein .45 ycenter 800 nearest True
