## Copyright 2022 Azariel Del Carmen (GanstaKingofSA)

screen ddmd_confirm(xs=480, ys=220, message, message2=None, yes_action, no_action):
    modal True

    zorder 200

    style_prefix "ddmd_confirm"
    
    add At("sdc_system/ddmd_app/ddmd_confirm_overlay.png", android_like_overlay)

    frame at android_like_frame:
        xsize xs
        ysize ys

        vbox:
            xalign .5
            yalign .5
            spacing 8

            label _(message):
                text_size 20
                xalign 0.0
            
            if message2:
                text _(message2):
                    xalign 0.0
                    size 16
                    outlines []
                    substitute False

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

screen ddmd_dialog(xs=480, ys=220, message, message2=None):
    modal True

    zorder 200

    style_prefix "ddmd_confirm"

    add At("sdc_system/ddmd_app/ddmd_confirm_overlay.png", android_like_overlay)

    frame at android_like_frame:
        xsize xs
        ysize ys

        vbox:
            xalign .5
            yalign .5
            spacing 8

            label _(message):
                xalign 0.0
                text_size 16

            if message2:
                text _(message2):
                    xalign 0.0
                    size 16
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

    add At("sdc_system/ddmd_app/ddmd_confirm_overlay.png", android_like_overlay)
    key "K_RETURN" action NullAction()

    frame at android_like_frame:
        xsize xs
        ysize ys

        vbox:
            xalign .5
            yalign .5
            spacing 8

            label _("Enter the name you wish to call this mod."):
                text_size 18
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

    add At("sdc_system/ddmd_app/ddmd_confirm_overlay.png", android_like_overlay)
    key "K_RETURN" action NullAction()

    frame at android_like_frame:
        xsize xs
        ysize ys

        vbox:
            xalign .5
            yalign .5
            spacing 8

            text _(message):
                size 18
                xalign 0.5
                substitute False
