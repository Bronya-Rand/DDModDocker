## Copyright 2022 Azariel Del Carmen (GanstaKingofSA)

screen ddmd_confirm(message, yes_action, no_action, message2=None, xs=480, ys=220):
    modal True

    zorder 200

    style_prefix "ddmd_confirm"
    
    add At("sdc_system/ddmd_app/ddmd_confirm_overlay.png", android_like_overlay) xsize config.screen_width ysize config.screen_height

    frame at android_like_frame:
        xsize int(xs * res_scale)
        ysize int(ys * res_scale)

        vbox:
            xalign .5
            yalign .5
            spacing int(8 * res_scale)

            label _(message):
                text_size int(20 * res_scale)
                xalign 0.0
                substitute False

            if message2:
                text _(message2):
                    xalign 0.0
                    size int(16 * res_scale)
                    outlines []
                    substitute False

            hbox:
                xalign 0.5
                spacing int(100 * res_scale)

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

screen ddmd_dialog(message, message2=None, xs=480, ys=220):
    modal True

    zorder 200

    style_prefix "ddmd_confirm"

    add At("sdc_system/ddmd_app/ddmd_confirm_overlay.png", android_like_overlay) xsize config.screen_width ysize config.screen_height

    frame at android_like_frame:
        xsize int(xs * res_scale)
        ysize int(ys * res_scale)

        vbox:
            xalign .5
            yalign .5
            spacing 8

            label _(message):
                xalign 0.0
                text_size int(16 * res_scale)
                substitute False

            if message2:
                text _(message2):
                    xalign 0.0
                    size int(16 * res_scale)
                    outlines []
                    substitute False

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action Hide("ddmd_dialog", Dissolve(0.25))

screen mod_name_input(zipPath, copy=False, xs=480, ys=220):
    modal True

    zorder 200

    style_prefix "ddmd_confirm"

    add At("sdc_system/ddmd_app/ddmd_confirm_overlay.png", android_like_overlay) xsize config.screen_width ysize config.screen_height
    key "K_RETURN" action NullAction()

    frame at android_like_frame:
        xsize int(xs * res_scale)
        ysize int(ys * res_scale)

        vbox:
            xalign .5
            yalign .5
            spacing 8

            label _("Enter the name you wish to call this mod."):
                text_size int(18 * res_scale)
                xalign 0.5

            input default "" value VariableInputValue("tempFolderName") length 24 allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action [Hide("mod_name_input"), Function(install_mod, zipPath=zipPath, copy=copy)]

screen ddmd_progress(message, xs=480, ys=220):
    modal True

    zorder 200

    style_prefix "ddmd_confirm"

    add At("sdc_system/ddmd_app/ddmd_confirm_overlay.png", android_like_overlay) xsize config.screen_width ysize config.screen_height
    key "K_RETURN" action NullAction()

    frame at android_like_frame:
        xsize int(xs * res_scale)
        ysize int(ys * res_scale)

        vbox:
            xalign .5
            yalign .5
            spacing 8

            text _(message):
                size 18
                xalign 0.5
                substitute False
