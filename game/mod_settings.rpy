
init python:
    import os
    import hashlib

    def is_original_file(path):
        if path.endswith("audio.rpa"):
            return hashlib.sha256(open(path, "rb").read()).hexdigest() == '121fedc50823e2a76d947025cc0f2dfa7c64b2454760b50091a64d1d36b7d2e7'
        elif path.endswith("fonts.rpa"):
            return hashlib.sha256(open(path, "rb").read()).hexdigest() == 'd48beafa7e1f3171b0e8e312f857af0e7eb387ef1e524a5be2595d46652d2018'
        elif path.endswith("images.rpa"):
            return hashlib.sha256(open(path, "rb").read()).hexdigest() == '6c3dccd4f35723ca1679b95710d4d09cec3d22439e24264bc6ff60d90640d393'
        elif path.endswith("scripts.rpa"):
            return hashlib.sha256(open(path, "rb").read()).hexdigest() == 'da7ba6d3cf9ec1ae666ec29ae07995a65d24cca400cd266e470deb55e03a51d4'

    def transfer_data(ddmm_path):
        modsTransferred = []
        try:
            for dirs in os.listdir(ddmm_path):
                if not os.path.exists(os.path.join(persistent.ddml_basedir, "game/mods", dirs)):
                    modsTransferred.append(dirs)
                    os.makedirs(os.path.join(persistent.ddml_basedir, "game/mods", dirs))
                    os.makedirs(os.path.join(persistent.ddml_basedir, "game/mods", dirs, "game"))

                    for ddmm_src, mod_dirs, mod_files in os.walk(ddmm_path + "/" + dirs):
                        dst_dir = ddmm_src.replace(ddmm_path + "/" + dirs, os.path.join(persistent.ddml_basedir, "game/mods", dirs))
                        for d in mod_dirs:
                            if d == "characters":
                                shutil.copytree(os.path.join(ddmm_src, d), os.path.join(dst_dir, d))
                        for f in mod_files:
                            if f.endswith((".rpa", ".rpyc", ".rpy")):
                                if not f.startswith("00"):
                                    mod_dir = ddmm_src
                                    break

                    for ddmm_src, mod_dirs, mod_files in os.walk(mod_dir):
                        dst_dir = ddmm_src.replace(mod_dir, os.path.join(persistent.ddml_basedir, "game/mods", dirs, "game"))
                        for mod_d in mod_dirs:
                            shutil.copytree(os.path.join(ddmm_src, mod_d), os.path.join(dst_dir, mod_d))
                        for mod_f in mod_files:
                            if mod_f.endswith(".rpa"):
                                if is_original_file(os.path.join(ddmm_src, mod_f)):
                                    continue
                            shutil.copy2(os.path.join(ddmm_src, mod_f), os.path.join(dst_dir, mod_f))

            renpy.hide_screen("ddmd_progress")
            renpy.show_screen("ddmd_dialog", message="Transferred all data sucessfully.")
        except OSError as err:
            if modsTransferred and os.path.exists(os.path.join(persistent.ddml_basedir, "game/mods", modsTransferred[-1])):
                shutil.rmtree(os.path.join(persistent.ddml_basedir, "game/mods", modsTransferred[-1]))
            renpy.hide_screen("ddmd_progress")
            renpy.show_screen("ddmd_dialog", message="A error has occured while transferring.", message2=str(err))
        except Exception as err:
            if modsTransferred and os.path.exists(os.path.join(persistent.ddml_basedir, "game/mods", modsTransferred[-1])):
                shutil.rmtree(os.path.join(persistent.ddml_basedir, "game/mods", modsTransferred[-1]))
            renpy.hide_screen("ddmd_progress")
            renpy.show_screen("ddmd_dialog", message="A unknown error has occured while transferring.", message2=str(err))

    def transfer_ddmm_data():
        if not renpy.windows:
            renpy.show_screen("ddmd_dialog", message="Transferring data from DDMM is only supported on Windows.")
            return
        renpy.show_screen("ddmd_progress", message="Transferring data. Please wait.")
        ddmm_path = os.path.join(
            os.getenv("APPDATA"), "DokiDokiModManager/GameData/installs"
        )
        if os.path.exists(ddmm_path):
            transfer_data(ddmm_path)
        else:
            renpy.show_screen("ddmd_dialog", message="Error: We were unable to locate a Doki Doki Manager folder in your AppData folder.", message2="If this is in error, please report it on Github.")

screen mod_settings():
    zorder 101
    style_prefix "modSettings"

    use ddmd_generic_window("Settings"):

        side "c":
            xpos 0.05
            ypos 0.15
            xsize int(450 * res_scale)
            ysize int(250 * res_scale)
            spacing 5

            viewport id "msw":
                mousewheel True
                draggable True
                has vbox
                spacing 1

                imagebutton:
                    idle ConditionSwitch("persistent.military_time", LiveComposite((int(250 * res_scale), int(40 * res_scale)), (0, 0), Transform("ddmd_toggle_on", size=(int(48 * res_scale), int(48 * res_scale))),
                        (int(55 * res_scale), 13), Text(_("Use 24-Hour Format"), style="modSettings_text", size=int(18 * res_scale))), "True",
                        LiveComposite((int(250 * res_scale), int(40 * res_scale)), (0, 0), Transform("ddmd_toggle_off", size=(int(48 * res_scale), int(48 * res_scale))), (int(55 * res_scale), int(13 * res_scale)), 
                        Text(_("Use 24-Hour Format"), style="modSettings_text", size=int(18 * res_scale))))
                    hover ConditionSwitch("persistent.military_time", LiveComposite((int(250 * res_scale), int(40 * res_scale)), (0, 0), Transform("ddmd_toggle_on_hover", size=(int(48 * res_scale), int(48 * res_scale))),
                        (int(55 * res_scale), 14), Text(_("Use 24-Hour Format"), style="modSettings_text", size=int(18 * res_scale))), "True", 
                        LiveComposite((int(250 * res_scale), int(40 * res_scale)), (0, 0), Transform("ddmd_toggle_off_hover", size=(int(48 * res_scale), int(48 * res_scale))), (int(55 * res_scale), int(13 * res_scale)), Text(_("Use 24-Hour Format"), 
                        style="modSettings_text", size=int(18 * res_scale))))
                    action [If(persistent.military_time, SetField(persistent, "military_time", False),
                        SetField(persistent, "military_time", True))]
                
                if renpy.windows:
                    imagebutton:
                        idle LiveComposite((int(410 * res_scale), int(40 * res_scale)), (10, 0), Transform("ddmd_transfer_icon", size=(int(36 * res_scale), int(36 * res_scale))), (int(55 * res_scale), int(7 * res_scale)), 
                            Text(_("[Beta] Transfer DDMM Mods to DDMD"), style="modSettings_text", substitute=False, size=int(18 * res_scale)))
                        hover LiveComposite((int(410 * res_scale), int(40 * res_scale)), (10, 0), Transform("ddmd_transfer_icon_hover", size=(int(36 * res_scale), int(36 * res_scale))), (int(55 * res_scale), int(7 * res_scale)), 
                            Text(_("[Beta] Transfer DDMM Mods to DDMD"), style="modSettings_text", substitute=False, size=int(18 * res_scale)))
                        action If(not persistent.transfer_warning, Show("ddmd_confirm", message=_("Transfer Warning"), 
                            message2=_("Transferring mods is in beta and some mods may not work due to Ren'Py version differences. By accepting this disclaimer, transferring will proceed."), 
                            yes_action=[SetField(persistent, "transfer_warning", True), Hide("ddmd_confirm"), Function(transfer_ddmm_data)], 
                            no_action=Hide("ddmd_confirm")), Function(transfer_ddmm_data))

                imagebutton:
                    idle LiveComposite((int(410 * res_scale), int(40 * res_scale)), (10, 0), Transform("ddmd_transfer_icon", size=(int(36 * res_scale), int(36 * res_scale))), (int(55 * res_scale), int(7 * res_scale)), 
                        Text(_("[Beta] Transfer DDML Mods to DDMD"), style="modSettings_text", substitute=False, size=int(18 * res_scale)))
                    hover LiveComposite((int(410 * res_scale), int(40 * res_scale)), (10, 0), Transform("ddmd_transfer_icon_hover", size=(int(36 * res_scale), int(36 * res_scale))), (int(55 * res_scale), int(7 * res_scale)), 
                        Text(_("[Beta] Transfer DDML Mods to DDMD"), style="modSettings_text", substitute=False, size=int(18 * res_scale)))
                    action If(not persistent.transfer_warning, Show("ddmd_confirm", message=_("Transfer Warning"), 
                        message2=_("Transferring mods is in beta and some mods may not work due to Ren'Py version differences. By accepting this disclaimer, transferring will proceed."), 
                        yes_action=[SetField(persistent, "transfer_warning", True), Hide("ddmd_confirm"), Show("pc_directory", Dissolve(0.25), ml=True)], 
                        no_action=Hide("ddmd_confirm")), Show("pc_directory", Dissolve(0.25), ml=True))
