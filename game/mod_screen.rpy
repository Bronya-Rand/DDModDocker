
init 1 python:
    #config.developer = True
    gui.button_height = None
    gui.navigation_spacing = -gui.navigation_spacing

init python:
    import os
    import json
    import threading
    from time import sleep
    import subprocess

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
            renpy.display.screen.show_screen("steam_like_overlay", "Access the Mod Docker menu while playing.\n\n\t\t\t\t\t\t\tPress: "+ config.keymap['mod_overlay'][0].replace("K_", ""))
        
        def run(self):
            sleep(1.5)
            self.show_notif()

    start_overlay = SteamLikeOverlay()

    def load_json():
        try:
            with open(persistent.ddml_basedir + "/selectedmod.json", "r") as mod_json:
                temp = json.load(mod_json)
                return temp['modName']
        except:
            return "DDLC"

    selectedMod = load_json()

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
        
        renpy.show_screen("dialog", Dissolve(0.25), message="Selected %s\nas the loadable mod. You must restart Mod Docker in order to load the mod." % folderName, ok_action=Hide("dialog", Dissolve(0.25)))

    def clearMod():
        global selectedMod
        
        os.remove(persistent.ddml_basedir + "/selectedmod.json")
        selectedMod = "DDLC"
        
        if renpy.version_tuple == (6, 99, 12, 4, 2187):
            renpy.show_screen("dialog", Dissolve(0.25), message="Returned to DDLC mode.\nYou must restart Mod Docker in order to load the mod.", ok_action=Hide("dialog", Dissolve(0.25)))
        else:
            renpy.show_screen("dialog", Dissolve(0.25), message="Returned to stock mode.\nYou must restart Mod Docker in order to apply these settings.", ok_action=Hide("dialog", Dissolve(0.25)))

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

default persistent.mod_list_disclaimer_accepted = False

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

                    if renpy.version_tuple == (6, 99, 12, 4, 2187):
                        textbutton "DDLC Mode":
                            action [Function(clearMod), SensitiveIf(selectedMod != "DDLC")]
                    else:
                        textbutton "Stock Mode":
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
                textbutton _("Search"):
                    action If(not persistent.mod_list_disclaimer_accepted, 
                    Show("confirm", message="{b}Disclaimer{/b}: This mod list source is provided by the defunct Doki Doki Mod Club site.\nNot all mods may be on here while others may be out-of-date.\nBy accepting this prompt, you acknoledge to the following disclaimer above.", 
                        yes_action=[SetField(persistent, "mod_list_disclaimer_accepted", True), Hide("confirm", Dissolve(0.25)), Show("mod_list", Dissolve(0.25))], no_action=Hide("confirm", Dissolve(0.25))), 
                    Show("mod_list", Dissolve(0.25)))
            vbox:
                textbutton _("Restart"):
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
                textbutton "Open Game Directory" action Function(open_dir, config.gamedir)
                textbutton "Open Mod Docker Game Directory" action Function(open_dir, persistent.ddml_basedir + "/game")
                if not config.gl2:
                    textbutton "Enable OpenGL 2":
                        action Show("confirm", Dissolve(0.25), message="Are you sure you want to enable OpenGL 2?\nSome mods may suffer from broken affects if this setting is on.\n\n{b}A restart is required to load OpenGL 2{/b}", yes_action=[SetField(config, "gl2", True), Quit()] , no_action=Hide("confirm", Dissolve(0.25)))
                else:
                    textbutton "Disable OpenGL 2":
                        action Show("confirm", Dissolve(0.25), message="Are you sure you want to disable OpenGL 2?\nSome mods may not have certain effects if this setting is off.\n\n{b}A restart is required to load OpenGL 2{/b}", yes_action=[SetField(config, "gl2", False), Quit(), Hide("confirm")] , no_action=Hide("confirm", Dissolve(0.25)))
        vbox:
            xpos 0.9
            ypos 0.9
            if selectedMod != "DDLC":
                textbutton "Select" action Function(loadMod, persistent.ddml_basedir + "/game/mods/" + selectedMod, selectedMod)

    key "K_ESCAPE" action Return(0)

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
    xpos 30
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

screen mod_list(search=None):
    zorder 101
    style_prefix "modList"

    drag:
        drag_name "mlist"
        drag_handle (0, 0, 1.0, 40)
        xsize 500
        ysize 300
        xpos 0.2
        ypos 0.3
        
        frame:
            hbox:
                ypos 0.005
                xalign 0.52 
                text "DDMC Mod List"

            hbox:
                ypos 0.005
                xalign 0.96
                textbutton "S" action Show("mod_search", Dissolve(0.25))
                textbutton "X" action Hide("mod_list", Dissolve(0.25))

            side "c":
                xpos 0.05
                ypos 0.15
                xsize 450
                ysize 250

                python:
                    ddmc_json = get_ddmc_modlist()

                viewport id "mlv":
                    mousewheel True
                    draggable True
                    has vbox

                    for x in ddmc_json:
                        if not search:
                            if x["modShow"] and x["modNSFW"]:
                                textbutton "(NSFW) " + x["modName"].replace("[", "[[").replace("]", "]]"):
                                    action Show("mod_list_info", Dissolve(0.25), mod=x)
                            elif x["modShow"]:
                                textbutton x["modName"].replace("[", "[[").replace("]", "]]"):
                                    action Show("mod_list_info", Dissolve(0.25), mod=x)
                        else:
                            if search in x["modName"] or search in x["modSearch"]:
                                if x["modShow"] and x["modNSFW"]:
                                    textbutton "(NSFW) " + x["modName"].replace("[", "[[").replace("]", "]]"):
                                        action Show("mod_list_info", Dissolve(0.25), mod=x)
                                elif x["modShow"]:
                                    textbutton x["modName"].replace("[", "[[").replace("]", "]]"):
                                        action Show("mod_list_info", Dissolve(0.25), mod=x)  

style renpy_generic_text:
    color "#000"
    outlines []

style modList_text is renpy_generic_text
style modList_button_text is mods_button_text

default modSearchCriteria = ""
screen mod_search():
    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"
    key "K_RETURN" action NullAction()

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _("Search For?"):
                style "confirm_prompt"
                xalign 0.5

            input default "" value VariableInputValue("modSearchCriteria") length 12 allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz[[]] "

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action [Hide("mod_search", Dissolve(0.25)), Show("mod_list", search=modSearchCriteria)]

screen mod_list_info(mod):
    zorder 102
    style_prefix "modInfo"
    drag:
        drag_name "mlistinfo"
        drag_handle (0, 0, 1.0, 40)
        xsize 800
        ysize 550
        xpos 0.2
        ypos 0.3
        
        frame:
            hbox:
                ypos 0.005
                xalign 0.52 
                text "Mod Info"

            hbox:
                ypos 0.005
                xalign 0.98
                textbutton "X":
                    text_style "navigation_button_text"
                    action Hide("mod_list_info", Dissolve(0.25))

            side "c":
                xpos 0.05
                ypos 0.1
                xsize 740
                ysize 420

                python:
                    ddmc_json = get_ddmc_modlist()

                viewport id "mlv":
                    mousewheel True
                    draggable True
                    has vbox

                    text mod["modName"].replace("[", "[["):
                        style "mods_label_text"
                        size 24
                    
                    python:
                        mod_release_date = datetime.datetime.strptime(mod['modDate'].replace(" ", "T"), "%Y-%m-%dT%H:%M:%S.%f")
                        mrd = mod_release_date.strftime("%d %B %Y")

                    if mod["modNSFW"]:
                        text "{b}This mod is marked as Not Safe For Work{/b}"
                    text "Released: " + mrd
                    text "Status: " + mod["modStatus"]
                    
                    python:
                        playTime = "Playtime: {u}"

                        if not mod["modPlayTimeHours"] and not mod["modPlayTimeMinutes"]:
                            playTime += "Unknown"

                        if mod["modPlayTimeHours"]:
                            playTime += str(mod["modPlayTimeHours"]) + " hour"

                            if mod["modPlayTimeHours"] > 1:
                                playTime += "s"

                        if mod["modPlayTimeMinutes"]:

                            if mod["modPlayTimeHours"] > 1:
                                playTime += " "
                            playTime += str(mod["modPlayTimeMinutes"]) + " minute"

                            if mod["modPlayTimeMinutes"] > 1:
                                playTime += "s"

                    text playTime + "{/u}"

                    null height 20

                    text "{b}Description{/b}"
                    text mod["modDescription"].replace("[", "[[")
            
            textbutton "Download":
                xalign 0.95
                yalign 0.98
                action OpenURL(mod['modUploadURL'])

style modInfo_text is renpy_generic_text
style modInfo_button_text is mods_button_text

init -1:
    screen steam_like_overlay(message):

        zorder 200
        style_prefix "steam"

        frame at steam_effect:
            xsize 200
            ysize 100
            xalign 1.0
            yalign 1.0

            has vbox:
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
