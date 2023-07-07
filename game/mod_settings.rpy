
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
        try:
            for mod_dir in os.listdir(ddmm_path):
                mod_path = os.path.join(persistent.ddml_basedir, "game/mods", mod_dir)

                if not os.path.exists(mod_path):
                    os.makedirs(mod_path)

                for ddmm_src, mod_dirs, _ in os.walk(os.path.join(ddmm_path, mod_dir)):
                    dst_dir = ddmm_src.replace(os.path.join(ddmm_path, mod_dir), mod_path)
                    for d in mod_dirs:
                        if d in ("characters", "game"):
                            shutil.copytree(os.path.join(ddmm_src, d), os.path.join(dst_dir, d))

            renpy.hide_screen("ddmd_progress")
            renpy.show_screen("ddmd_dialog", message="Transferred all data sucessfully.")
        except OSError as err:
            mod_path = os.path.join(persistent.ddml_basedir, "game/mods", mod_dir)
            if os.path.exists(mod_path):
                shutil.rmtree(mod_path)
            renpy.hide_screen("ddmd_progress")
            renpy.show_screen("ddmd_dialog", message="A error has occured while transferring %s." % mod_dir, message2=str(err))
        except Exception as err:
            mod_path = os.path.join(persistent.ddml_basedir, "game/mods", mod_dir)
            if os.path.exists(mod_path):
                shutil.rmtree(mod_path)
            renpy.hide_screen("ddmd_progress")
            renpy.show_screen("ddmd_dialog", message="A unknown error has occured while transferring%s." % mod_dir, message2=str(err))

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
                    idle ConditionSwitch("config.gl2", Composite((int(250 * res_scale), int(40 * res_scale)), (0, 0), Transform("ddmd_toggle_on", size=(int(48 * res_scale), int(48 * res_scale))),
                        (int(55 * res_scale), int(13 * res_scale)), Text(_("Enable OpenGL 2 Globally"), style="modSettings_text", size=int(18 * res_scale))), "True",
                        Composite((int(250 * res_scale), int(40 * res_scale)), (0, 0), Transform("ddmd_toggle_off", size=(int(48 * res_scale), int(48 * res_scale))), (int(55 * res_scale), int(13 * res_scale)), 
                        Text(_("Enable OpenGL 2 Globally"), style="modSettings_text", size=int(18 * res_scale))))
                    hover ConditionSwitch("config.gl2", Composite((int(250 * res_scale), int(40 * res_scale)), (0, 0), Transform("ddmd_toggle_on_hover", size=(int(48 * res_scale), int(48 * res_scale))),
                        (int(55 * res_scale), 14), Text(_("Enable OpenGL 2 Globally"), style="modSettings_text", size=int(18 * res_scale))), "True", 
                        Composite((int(250 * res_scale), int(40 * res_scale)), (0, 0), Transform("ddmd_toggle_off_hover", size=(int(48 * res_scale), int(48 * res_scale))), (int(55 * res_scale), int(13 * res_scale)), Text(_("Enable OpenGL 2 Globally"), 
                        style="modSettings_text", size=int(18 * res_scale))))
                    action If(config.gl2, Show("ddmd_confirm", Dissolve(0.25), message=_("Disable OpenGL 2?"), 
                        message2=_("Some mods may not have certain effects display if this setting is turned off. {b}A restart is required to load OpenGL 2{/b}."), 
                        yes_action=[SetField(config, "gl2", False), Function(set_settings_json), Quit()], no_action=Hide("ddmd_confirm", 
                        Dissolve(0.25))), Show("ddmd_confirm", Dissolve(0.25), message=_("Enable OpenGL 2?"), 
                        message2=_("Some mods may suffer from broken affects if this setting is turned on. {b}A restart is required to load OpenGL 2{/b}."), 
                        yes_action=[SetField(config, "gl2", True), Function(set_settings_json), Quit()], no_action=Hide("ddmd_confirm", 
                        Dissolve(0.25))))

                imagebutton:
                    idle ConditionSwitch("persistent.military_time", Composite((int(250 * res_scale), int(40 * res_scale)), (0, 0), Transform("ddmd_toggle_on", size=(int(48 * res_scale), int(48 * res_scale))),
                        (int(55 * res_scale), 13), Text(_("Use 24-Hour Format"), style="modSettings_text", size=int(18 * res_scale))), "True",
                        Composite((int(250 * res_scale), int(40 * res_scale)), (0, 0), Transform("ddmd_toggle_off", size=(int(48 * res_scale), int(48 * res_scale))), (int(55 * res_scale), int(13 * res_scale)), 
                        Text(_("Use 24-Hour Format"), style="modSettings_text", size=int(18 * res_scale))))
                    hover ConditionSwitch("persistent.military_time", Composite((int(250 * res_scale), int(40 * res_scale)), (0, 0), Transform("ddmd_toggle_on_hover", size=(int(48 * res_scale), int(48 * res_scale))),
                        (int(55 * res_scale), 14), Text(_("Use 24-Hour Format"), style="modSettings_text", size=int(18 * res_scale))), "True", 
                        Composite((int(250 * res_scale), int(40 * res_scale)), (0, 0), Transform("ddmd_toggle_off_hover", size=(int(48 * res_scale), int(48 * res_scale))), (int(55 * res_scale), int(13 * res_scale)), Text(_("Use 24-Hour Format"), 
                        style="modSettings_text", size=int(18 * res_scale))))
                    action [If(persistent.military_time, SetField(persistent, "military_time", False),
                        SetField(persistent, "military_time", True))]
                
                if renpy.windows:
                    imagebutton:
                        idle Composite((int(410 * res_scale), int(40 * res_scale)), (10, 0), Transform("ddmd_transfer_icon", size=(int(36 * res_scale), int(36 * res_scale))), (int(55 * res_scale), int(7 * res_scale)), 
                            Text(_("[Beta] Transfer DDMM Mods to DDMD"), style="modSettings_text", substitute=False, size=int(18 * res_scale)))
                        hover Composite((int(410 * res_scale), int(40 * res_scale)), (10, 0), Transform("ddmd_transfer_icon_hover", size=(int(36 * res_scale), int(36 * res_scale))), (int(55 * res_scale), int(7 * res_scale)), 
                            Text(_("[Beta] Transfer DDMM Mods to DDMD"), style="modSettings_text", substitute=False, size=int(18 * res_scale)))
                        action If(not persistent.transfer_warning, Show("ddmd_confirm", message=_("Transfer Warning"), 
                            message2=_("Transferring mods is in beta and some mods may not work due to Ren'Py version differences. By accepting this disclaimer, transferring will proceed."), 
                            yes_action=[SetField(persistent, "transfer_warning", True), Hide("ddmd_confirm"), Function(transfer_ddmm_data)], 
                            no_action=Hide("ddmd_confirm")), Function(transfer_ddmm_data))

                imagebutton:
                    idle Composite((int(410 * res_scale), int(40 * res_scale)), (10, 0), Transform("ddmd_transfer_icon", size=(int(36 * res_scale), int(36 * res_scale))), (int(55 * res_scale), int(7 * res_scale)), 
                        Text(_("[Beta] Transfer DDML Mods to DDMD"), style="modSettings_text", substitute=False, size=int(18 * res_scale)))
                    hover Composite((int(410 * res_scale), int(40 * res_scale)), (10, 0), Transform("ddmd_transfer_icon_hover", size=(int(36 * res_scale), int(36 * res_scale))), (int(55 * res_scale), int(7 * res_scale)), 
                        Text(_("[Beta] Transfer DDML Mods to DDMD"), style="modSettings_text", substitute=False, size=int(18 * res_scale)))
                    action If(not persistent.transfer_warning, Show("ddmd_confirm", message=_("Transfer Warning"), 
                        message2=_("Transferring mods is in beta and some mods may not work due to Ren'Py version differences. By accepting this disclaimer, transferring will proceed."), 
                        yes_action=[SetField(persistent, "transfer_warning", True), Hide("ddmd_confirm"), Show("pc_directory", Dissolve(0.25), ml=True)], 
                        no_action=Hide("ddmd_confirm")), Show("pc_directory", Dissolve(0.25), ml=True))
