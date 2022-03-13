
init python:
    import os
    import json
    import threading
    from time import sleep
    import subprocess

    current_mod_list = []
    selectedMod = None
    confirmedMod = None

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

    def load_json():
        try:
            with open(persistent.ddml_basedir + "/selectedmod.json", "r") as mod_json:
                temp = json.load(mod_json)
                return temp['modName']
        except:
            return "DDLC"

    selectedMod = load_json()
    confirmedMod = load_json()

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
        global confirmedMod
        isRPA = False
        
        for root, dirs, files in os.walk(x + "/game"):
            for f in files:
                if f.endswith(".rpa"):
                    isRPA = True
        
        mod_dict = {
            "modName": folderName,
            "isRPA": isRPA,
        }
        confirmedMod = folderName
        
        with open(persistent.ddml_basedir + "/selectedmod.json", "w") as j:
            json.dump(mod_dict, j)
        
        renpy.show_screen("ddmd_dialog", message="Selected %s as the loadable mod. You must restart Mod Docker in order to load the mod." % folderName, 
            ok_action=Hide("ddmd_dialog", Dissolve(0.25)))

    def clearMod():
        global confirmedMod
        
        if os.path.exists(persistent.ddml_basedir + "/selectedmod.json"):
            os.remove(persistent.ddml_basedir + "/selectedmod.json")

            confirmedMod = "DDLC"
        
            if renpy.version_tuple == (6, 99, 12, 4, 2187):
                renpy.show_screen("ddmd_dialog", message="Returned to DDLC mode. You must restart Mod Docker in order to load the mod.", 
                    ok_action=Hide("ddmd_dialog", Dissolve(0.25)))
            else:
                renpy.show_screen("ddmd_dialog", message="Returned to stock mode. You must restart Mod Docker in order to apply these settings.", 
                    ok_action=Hide("ddmd_dialog", Dissolve(0.25)))
        else:
            if renpy.version_tuple == (6, 99, 12, 4, 2187):
                renpy.show_screen("ddmd_dialog", message="Error: You are already in DDLC Mode.", 
                    ok_action=Hide("ddmd_dialog", Dissolve(0.25)))
            else:
                renpy.show_screen("ddmd_dialog", message="Error: You are already in stock mode.", 
                    ok_action=Hide("ddmd_dialog", Dissolve(0.25)))
        

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
                            action [SetVariable("selectedMod", "DDLC"), SensitiveIf(selectedMod != "DDLC")]
                    else:
                        textbutton "Stock Mode":
                            action [SetVariable("selectedMod", "DDLC"), SensitiveIf(selectedMod != "DDLC")]

                    python:
                        global current_mod_list
                        current_mod_list = get_mod_list()

                    for x in current_mod_list:
                        textbutton "[x.modFolderName!q]":
                            action [SetVariable("selectedMod", x.modFolderName), SensitiveIf(x.modFolderName != selectedMod)]

        hbox:
            style "mods_return_button"
            vbox:
                imagebutton:
                    idle "ddmd_return_icon"
                    hover "ddmd_return_icon_hover"
                    action [Return(0), With(Dissolve(0.5))]
            null width 10
            vbox:
                imagebutton:
                    idle "ddmd_search_icon"
                    hover "ddmd_search_icon_hover"
                    action If(not persistent.mod_list_disclaimer_accepted, 
                    Show("confirm", message="{b}Disclaimer{/b}: This mod list source is provided by the defunct Doki Doki Mod Club site.\nNot all mods may be on here while others may be out-of-date.\nBy accepting this prompt, you acknoledge to the following disclaimer above.", 
                        yes_action=[SetField(persistent, "mod_list_disclaimer_accepted", True), Hide("confirm", Dissolve(0.25)), 
                        Show("mod_list", Dissolve(0.25))], no_action=Hide("confirm", Dissolve(0.25))), 
                        Show("mod_list", Dissolve(0.25)))
            null width 10
            vbox:
                imagebutton:
                    idle "ddmd_restart_icon"
                    hover "ddmd_restart_icon_hover"
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
                textbutton "Open [[REDACTED] Game Directory" action Function(open_dir, persistent.ddml_basedir + "/game")
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
                        message2="Some mods may not have certain effects if this setting is off. {b}A restart is required to load OpenGL 2{/b}.", 
                        yes_action=[SetField(persistent, "enable_gl2", False)], no_action=Hide("ddmd_confirm", 
                        Dissolve(0.25))), Show("ddmd_confirm", Dissolve(0.25), message="Enable OpenGL 2?", 
                        message2="Some mods may suffer from broken affects if this setting is on. {b}A restart is required to load OpenGL 2{/b}.", 
                        yes_action=[SetField(persistent, "enable_gl2", True), Quit()], no_action=Hide("ddmd_confirm", 
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
