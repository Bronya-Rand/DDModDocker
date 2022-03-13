
## MD Show Transition
transform ml_overlay_effect:
    on show:
        alpha 0.0
        linear 0.5 alpha 1.0

## Confirm Transitons
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
        ycenter 900 yanchor 1.0 alpha 1.00 nearest True
        easein 0.3 ycenter 620
    on hide:
        easein .75 ycenter 900 nearest True