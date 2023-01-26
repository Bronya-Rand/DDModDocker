## Copyright 2023 Azariel Del Carmen (GanstaKingofSA)

screen mod_list(search=""):
    zorder 101
    style_prefix "modList"

    use ddmd_generic_window("Mod List", allow_search=True):

        side "c":
            xpos 0.05
            ypos 0.15
            xsize int(450 * res_scale)
            ysize int(250 * res_scale)
            spacing 10

            python:
                ddmc_json = get_ddmc_modlist()

            viewport id "mlv":
                mousewheel True
                draggable True
                has vbox
                spacing 3

                for x in ddmc_json:
                    if not search:
                        if x["modShow"] and x["modNSFW"]:
                            textbutton "(NSFW) " + x["modName"].replace("[", "[[").replace("]", "]]"):
                                action Show("mod_list_info", Dissolve(0.25), mod=x)
                        elif x["modShow"]:
                            textbutton x["modName"].replace("[", "[[").replace("]", "]]"):
                                action Show("mod_list_info", Dissolve(0.25), mod=x)
                    else:
                        if search.lower() in x["modName"].lower() or search.lower() in x["modSearch"]:
                            if x["modShow"] and x["modNSFW"]:
                                textbutton "(NSFW) " + x["modName"].replace("[", "[[").replace("]", "]]"):
                                    action Show("mod_list_info", Dissolve(0.25), mod=x)
                            elif x["modShow"]:
                                textbutton x["modName"].replace("[", "[[").replace("]", "]]"):
                                    action Show("mod_list_info", Dissolve(0.25), mod=x)

init python:
    def search_script(msc):
        renpy.show_screen("mod_list", search=msc)

screen mod_search(xs=480, ys=220):
    modal True
    zorder 200

    style_prefix "ddmd_confirm"

    use ddmd_generic_notif(xs, ys):

        vbox:
            xalign .5
            yalign .5
            spacing 8

            label _("Search For?"):
                text_size 20
                xalign 0.5

            input:
                value VariableInputValue("modSearchCriteria") 
                length 24 
                allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz[[]] "
                copypaste True

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action [Hide("mod_search", Dissolve(0.25)), Function(search_script, modSearchCriteria)]
                textbutton _("Clear") action SetVariable("modSearchCriteria", "")

screen mod_list_info(mod):
    zorder 102
    style_prefix "modInfo"

    use ddmd_generic_window("Mod Info", 800, 550):

        side "c":
            xpos 0.05
            ypos 0.11
            xsize int(740 * res_scale)
            ysize int(420 * res_scale)

            viewport id "mlv":
                mousewheel True
                draggable True
                has vbox

                text mod["modName"].replace("[", "[["):
                    style "mods_label_text"
                    size int(22 * res_scale)
                
                python:
                    mod_release_date = datetime.datetime.strptime(mod['modDate'].replace(" ", "T"), "%Y-%m-%dT%H:%M:%S.%f")
                    mrd = mod_release_date.strftime("%d %B %Y")

                if mod["modNSFW"]:
                    text _("{b}This mod is marked as Not Safe For Work{/b}") size int(20 * res_scale)
                text _("Released: ") + mrd size int(20 * res_scale)
                text _("Status: ") + mod["modStatus"] size int(20 * res_scale)
                
                python:
                    playTime = _("Playtime: {u}")

                    if not mod["modPlayTimeHours"] and not mod["modPlayTimeMinutes"]:
                        playTime += _("Unknown")

                    if mod["modPlayTimeHours"]:
                        playTime += str(mod["modPlayTimeHours"]) + _(" hour")

                        if mod["modPlayTimeHours"] > 1:
                            playTime += "s"

                    if mod["modPlayTimeMinutes"]:

                        if mod["modPlayTimeHours"] > 1:
                            playTime += " "
                        playTime += str(mod["modPlayTimeMinutes"]) + _(" minute")

                        if mod["modPlayTimeMinutes"] > 1:
                            playTime += "s"

                text playTime + "{/u}" size int(20 * res_scale)

                null height 20

                text _("{b}Description{/b}") size int(20 * res_scale)
                text mod["modDescription"].replace("[", "[[") size int(20 * res_scale)
        
        imagebutton:
            idle Composite((int(250 * res_scale), int(50 * res_scale)), (0, 0), Transform("ddmd_openinbrowser_icon", size=(int(36 * res_scale), int(36 * res_scale))), (int(40 * res_scale), 0), Text(_("Download Page"), style="mods_text"))
            hover Composite((int(250 * res_scale), int(50 * res_scale)), (0, 0), Transform("ddmd_openinbrowser_icon_hover", size=(int(36 * res_scale), int(36 * res_scale))), (int(40 * res_scale), 0), Text(_("Download Page"), style="mods_button_text"))
            xalign 0.95
            yalign 0.98
            action OpenURL(mod['modUploadURL'])
