
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

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

screen ddmd_dialog(xs=480, ys=220, message, ok_action):
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

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action
