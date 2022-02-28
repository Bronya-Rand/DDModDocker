
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
        with open(config.basedir + "/selectedmod.json", "r") as s:
            j = json.load(s)
            selectedMod = j['modName']
    except:
        selectedMod = "DDLC"

    mod_dir = os.path.join(config.basedir, "game/mods")
    
    if not os.path.exists(mod_dir):
        os.mkdir(mod_dir)
    if not os.path.exists(config.basedir + "/game/MLSaves"):
        os.makedirs(config.basedir + "/game/MLSaves")
    #config.atl_start_on_show = False

    def restart():
        renpy.quit(relaunch=True)

    def get_mod_list():
        global selectedMod
        templist = []
        for modfolder in os.listdir(config.basedir + "/game/mods"):
            if os.path.exists(config.basedir + "/game/mods/" + modfolder + "/game"):
                modfolderpath = config.basedir + "/game/mods/" + modfolder + "/game"
            else:
                modfolderpath = config.basedir + "/game/mods/" + modfolder

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

        for root, dirs, files in os.walk(x):
            for f in files:
                if f.endswith(".rpa"):
                    isRPA = True

        mod_dict = {
            "modName": folderName,
            "isRPA": isRPA,
        }

        with open(config.basedir + "/selectedmod.json", "w") as j:
            json.dump(mod_dict, j)
        
        renpy.show_screen("dialog", message="Successfully selected " + folderName + " as\nthe loadable mod.\nYou must restart DDLC in order to load the mod.", ok_action=Hide("dialog"))

    def clearMod():
        global selectedMod

        s = open(config.basedir + "/selectedmod.json", "w")
        s.close()

        selectedMod = "DDLC"
        
        if renpy.version_tuple == (6, 99, 12, 4, 2187):
            renpy.show_screen("dialog", message="Successfully selected DDLC as the loadable mod.\nYou must restart DDLC in order to load the mod.", ok_action=Hide("dialog"))
        else:
            renpy.show_screen("dialog", message="Returned to stock settings.\nYou must restart DDLC in order to apply these settings.", ok_action=Hide("dialog"))

    def open_save_dir():
        if renpy.windows:
            os.startfile(config.basedir + "/game/MLSaves")
        elif renpy.macintosh:
            subprocess.Popen([ "open", config.basedir + "/game/MLSaves" ])
        else:
            subprocess.Popen([ "xdg-open", config.basedir + "/game/MLSaves" ])
    
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

        add "menu_bg"

        vbox:
            xsize 365
            yfill True
            add Transform("#000", alpha=0.8)

        vbox:
            xpos 0.28
            yfill True
            add Transform("#202020", alpha=0.5)

        label "Select a Mod"

        side "c":

            viewport id "mlvp":
                mousewheel True
                scrollbars True
                area (50, 100, 280, 800)
                has vbox
                spacing 3

                if renpy.version_tuple == (6, 99, 12, 4, 2187):
                    textbutton "DDLC":
                        action [Function(clearMod), SensitiveIf(selectedMod != "DDLC")]
                else:
                    textbutton "Stock":
                        action [Function(clearMod), SensitiveIf(selectedMod != "DDLC")]
                
                null height 12

                python:
                    global current_mod_list
                    current_mod_list = get_mod_list()

                for x in current_mod_list:
                    textbutton "[x.modFolderName!q]":
                        action [SetVariable("selectedMod", x.modFolderName), SensitiveIf(x.modFolderName != selectedMod)]

                    null height 12
        hbox:
            style "mods_return_button"
            vbox:
                textbutton _("Return"):
                    action [Return(0), With(Dissolve(0.5))]
            vbox:
                #xoffset 50
                textbutton _("Restart"):
                    action Function(restart)

        vbox:
            hbox:
                viewport id "modinfoname":
                    area (450, 50, 800, 150)
                    label "[selectedMod]"

                bar value XScrollValue("modinfoname") xsize 800 xpos 0.3 ypos 1.1

        vbox:
            xpos 0.31
            ypos 0.25
            label "Options" 
            vbox:
                xpos 0.2
                yoffset -20
                textbutton "Open Save Directory" action Function(open_save_dir)
                textbutton "Open Game Directory" action Function(open_dir, config.gamedir)
                textbutton "Open DDML Game Directory" action Function(open_dir, config.basedir + "/game")
            
        vbox:
            xpos 0.9
            ypos 0.9
            textbutton "Select" action Function(loadMod, config.basedir + "/game/mods/" + selectedMod, selectedMod)

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
    properties gui.button_properties("navigation_button")
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
    size 22
    outlines [(4, "#803366", 0, 0), (2, "#803366", 2, 2)]
    hover_outlines [(4, "#bb4c96", 0, 0), (2, "#bb4c96", 2, 2)]
    insensitive_outlines [(4, "#f374c9", 0, 0), (2, "#f374c9", 2, 2)]
    line_spacing -16
    line_leading 20

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
