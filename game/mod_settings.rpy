
init python:

    def transfer_data(ddmm_path):
        modsTransferred = []
        try:
            for dirs in os.listdir(ddmm_path):
                if not os.path.exists(persistent.ddml_basedir + "/game/mods/" + dirs):
                    modsTransferred.append(dirs)
                    os.makedirs(persistent.ddml_basedir + "/game/mods/" + dirs)
                    os.makedirs(persistent.ddml_basedir + "/game/mods/" + dirs + "/game")

                    for ddmm_src, mod_dirs, mod_files in os.walk(ddmm_path + "/" + dirs):
                        dst_dir = ddmm_src.replace(ddmm_src + "/" + dirs, persistent.ddml_basedir + "/game/mods/" + dirs)
                            for d in mod_dirs:
                                if d == "characters":
                                    shutil.copytree(os.path.join(ddmm_src, d), os.path.join(dst_dir, d))
                            for f in mod_files:
                                if f.endswith((".rpa", ".rpyc", ".rpy")):
                                    if not f.startswith("00"):
                                        mod_dir = mod_src
                                        break
                        
                    for ddmm_src, mod_dirs, mod_files in os.walk(mod_dir):
                        dst_dir = ddmm_src.replace(ddmm_src + "/" + dirs + "/game", persistent.ddml_basedir + "/game/mods/" + dirs + "/game")
                        for mod_d in mod_dirs:
                            shutil.copy2(os.path.join(ddmm_src, mod_d), os.path.join(dst_dir, mod_d))
                        for mod_f in mod_files:
                            shutil.copy2(os.path.join(ddmm_src, mod_f), os.path.join(dst_dir, mod_f))
            tempDirPath = ""
            renpy.hide_screen("ddmd_progress")
        except OSError as err:
            tempDirPath = ""
            shutil.rmtree(persistent.ddml_basedir + "/game/mods/" + modsTransferred[-1])
            renpy.hide_screen("ddmd_progress")
            renpy.show_screen("ddmd_dialog", message="A error has occured while transfering %s." % modsTransferred[-1], message2=str(err))
        except Exception as err:
            tempDirPath = ""
            shutil.rmtree(persistent.ddml_basedir + "/game/mods/" + modsTransferred[-1])
            renpy.hide_screen("ddmd_progress")
            renpy.show_screen("ddmd_dialog", message="A error has occured while transfering %s." % modsTransferred[-1], message2=str(err))

    def transfer_ddmm_data():
        if not renpy.windows:
            renpy.show_screen("ddmd_dialog", message="Transferring data from DDMM is only supported on Windows.")
            return
        renpy.show_screen("ddmd_progress", message="Transferring data. Please wait.")
        ddmm_path = os.path.join(
            os.getenv("APPDATA"), "DokiDokiModManager/GameData/installs"
        )
        transfer_data(ddmm_path)
        renpy.show_screen("ddmd_dialog", message="Transferred all data from DDMM sucessfully.")

    def transfer_ddml_data(ddml_path):
        renpy.show_screen("pc_folder_directory", Dissolve(0.25), folderType="DDML")
        transfer_data(tempDirPath)
        renpy.show_screen("ddmd_dialog", message="Transferred all data from DDML sucessfully.")

screen mod_settings():
    zorder 101
    style_prefix "modSettings"

    drag:
        drag_name "msettings"
        drag_handle (0, 0, 1.0, 40)
        xsize 500
        ysize 300
        xpos 0.3
        ypos 0.3
        
        frame:
            hbox:
                ypos 0.005
                xalign 0.52 
                text "Settings"

            hbox:
                ypos -0.005
                xalign 0.98
                imagebutton:
                    idle "ddmd_close_icon"
                    hover "ddmd_close_icon_hover"
                    action Hide("mod_settings", Dissolve(0.25))

            side "c":
                xpos 0.05
                ypos 0.15
                xsize 450
                ysize 250
                spacing 10

                imagebutton:
                    idle ConditionSwitch("config.gl2", Composite((250, 50), (0, 0), "ddmd_toggle_on",
                        (55, 7), Text("Enable OpenGL 2", style="modSettings_text")), "True",
                        Composite((250, 50), (0, 0), "ddmd_toggle_off", (55, 7), 
                        Text("Enable OpenGL 2", style="modSettings_text")))
                    hover ConditionSwitch("config.gl2", Composite((250, 50), (0, 0), "ddmd_toggle_on_hover",
                        (55, 7), Text("Enable OpenGL 2", style="modSettings_text")), "True", 
                        Composite((250, 50), (0, 0), "ddmd_toggle_off_hover", (55, 7), Text("Enable OpenGL 2", 
                        style="modSettings_text")))
                    action If(config.gl2, Show("ddmd_confirm", Dissolve(0.25), message="Disable OpenGL 2?", 
                        message2="This mod may not have certain effects display if this setting is turned off. {b}A restart is required to load OpenGL 2{/b}.", 
                        yes_action=[SetField(config, "gl2", False), Function(set_settings_json), Quit()], no_action=Hide("ddmd_confirm", 
                        Dissolve(0.25))), Show("ddmd_confirm", Dissolve(0.25), message="Enable OpenGL 2?", 
                        message2="This mod may suffer from broken affects if this setting is turned on. {b}A restart is required to load OpenGL 2{/b}.", 
                        yes_action=[SetField(config, "gl2", True), Function(set_settings_json), Quit()], no_action=Hide("ddmd_confirm", 
                        Dissolve(0.25))))

                if renpy.windows:        
                    button:
                        action Function(transfer_ddmm_data)
                                
                        add If(Composite((210, 50), (0, 1), "ddmd_transfer_icon", (38, 0), Text("[Beta] Transfer DDMM Mods to DDMD", style="modSettings_text", substitute=False))) 
                
                button:
                    action Show(transfer_data, Dissolve(0.25))
                            
                    add If(Composite((210, 50), (0, 1), "ddmd_transfer_icon", (38, 0), Text("[Beta] Transfer DDML Mods to DDMD", style="modSettings_text", substitute=False))) 

style modSettings_text is mods_text