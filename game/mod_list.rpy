## Copyright 2022 Azariel Del Carmen (GanstaKingofSA)

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
                ypos -0.005
                xalign 0.96
                imagebutton:
                    idle "ddmd_search_window_icon"
                    hover "ddmd_search_window_icon_hover"
                    action Show("mod_search", Dissolve(0.25))
                imagebutton:
                    idle "ddmd_close_icon"
                    hover "ddmd_close_icon_hover"
                    action Hide("mod_list", Dissolve(0.25))

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

screen mod_search(xs=480, ys=220):
    modal True

    zorder 200

    style_prefix "ddmd_confirm"

    add At("sdc_system/ddmd_app/ddmd_confirm_overlay.png", android_like_overlay)
    key "K_RETURN" action NullAction()

    frame at android_like_frame:
        xsize xs
        ysize ys

        vbox:
            xalign .5
            yalign .5
            spacing 8

            label _("Search For?"):
                text_size 20
                xalign 0.5

            input default "" value VariableInputValue("modSearchCriteria") length 24 allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz[[]] "

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
                imagebutton:
                    idle "ddmd_close_icon"
                    hover "ddmd_close_icon_hover"
                    action Hide("mod_list_info", Dissolve(0.25))

            side "c":
                xpos 0.05
                ypos 0.1
                xsize 740
                ysize 420

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
            
            imagebutton:
                idle Composite((250, 50), (0, 0), "ddmd_openinbrowser_icon", (40, 0), Text("Download Page", style="mods_text"))
                xalign 0.95
                yalign 0.98
                action OpenURL(mod['modUploadURL'])
