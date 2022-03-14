
## Standard Ren'Py Font
style renpy_generic_text:
    color "#fff"
    outlines []

## Main UI (Folder List)
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
    font "sdc_system/ddmd_app/Raleway-Bold.ttf"
    size 38
    color "#fff"
    outlines [(6, "#803366", 0, 0), (3, "#803366", 2, 2)]
    yalign 0.5

style mods_text:
    size 24
    font "sdc_system/ddmd_app/Raleway-Bold.ttf"
    outlines [(2, "#803366", 0, 0), (1, "#803366", 1, 1)]

## Main UI 2 (Mod Options)
style mods_info_label is mods_label
style mods_info_label_text is mods_label_text

style mods_info_label:
    ypos 0.5

style mods_button_text:
    font "sdc_system/ddmd_app/Raleway-Bold.ttf"
    color "#fff"
    size 24
    outlines [(4, "#803366", 0, 0), (2, "#803366", 2, 2)]
    hover_outlines [(4, "#bb4c96", 0, 0), (2, "#bb4c96", 2, 2)]
    insensitive_outlines [(4, "#f374c9", 0, 0), (2, "#f374c9", 2, 2)]

## Main UI 3 (Sidebar Options)
style mods_return_button is gui_button
style mods_return_button_text is gui_button_text

style mods_return_button:
    xpos 70
    yalign 1.0
    yoffset -30

style mods_return_button_text:
    outlines [(4, "#803366", 0, 0), (2, "#803366", 2, 2)]
    hover_outlines [(4, "#bb4c96", 0, 0), (2, "#bb4c96", 2, 2)]
    insensitive_outlines [(4, "#f374c9", 0, 0), (2, "#f374c9", 2, 2)]

style mods_frame:
    padding gui.frame_borders.padding
    background Frame("sdc_system/ddmd_app/ddmd_frame.png", left=4, top=27, bottom=4, right=4, tile=False)

## Mod List
style modList_text is renpy_generic_text
style modList_button_text is mods_button_text
style modList_frame is mods_frame:
    background Frame("sdc_system/ddmd_app/ddmd_frame.png", left=4, top=3, bottom=4, right=4, tile=False)

## Mod List Info
style modInfo_text is renpy_generic_text
style modInfo_button_text is mods_button_text
style modInfo_frame is mods_frame

## Mod Confirm/Dialog
style ddmd_confirm_frame:
    background Frame("sdc_system/ddmd_app/secondary_frame.png", top=1, bottom=1, left=1, right=1, tile=False)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style ddmd_confirm_prompt is gui_prompt
style ddmd_confirm_prompt_text is gui_prompt_text
style ddmd_confirm_button is gui_medium_button
style ddmd_confirm_button_text is mods_button_text

style ddmd_confirm_prompt_text:
    color "#fff"
    outlines []
    text_align 0.0
    layout "subtitle"

style ddmd_confirm_button:
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

## Mod Hover Info
style mods_hover_frame:
    background Frame("#fff", left=4, top=4, bottom=4, right=4, tile=False)

style mods_hover_text:
    color "#000"
    outlines []
    size 12