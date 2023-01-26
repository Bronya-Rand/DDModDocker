## Copyright 2023 Azariel Del Carmen (GanstaKingofSA)

## MD Show Transition
transform ml_overlay_effect:
    on show:
        alpha 0.0
        linear 0.5 alpha 1.0

## Confirm Transitions
transform android_like_overlay:
    on show:
        alpha 0.0
        linear 0.3 alpha 1.0
    on hide:
        alpha 1.0
        linear 0.3 alpha 0.0

transform android_like_frame:
    subpixel True
    on show:
        ycenter config.screen_height + int(180 * res_scale) yanchor 1.0 alpha 1.00 nearest True
        easein 0.3 ycenter config.screen_height - int(100 * res_scale)
    on hide:
        easein .75 ycenter config.screen_height + int(180 * res_scale) nearest True

## Mod Hover Transition
transform windows_like_effect:
    on show:
        alpha 0.0
        pause 1.0
        linear 0.25 alpha 1.0
    on hide:
        alpha 1.0
        linear 0.25 alpha 0.0