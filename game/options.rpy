## Copyright 2022 Azariel Del Carmen (GanstaKingofSA)

# This file customizes what your mod is and and how it starts and builds!

# This controls what your mod is called.
define config.name = "Doki Doki Mod Docker (Alpha)"
define config.window_title = config.name

# This controls whether you want your mod name to show in the main menu.
# If your mod name is big, it is suggested to turn this off.
define gui.show_name = False

# This controls the version number of your mod.
define config.version = "1.0.7"

# This adds information about your mod in the About screen.
# DDLC does not have a 'About' screen so you can leave this blank.
define gui.about = _("")

# This control the name of your mod build when you package your mod
# in the Ren'Py Launcher or DDMM (Doki Doki Mod Maker).
# Note:
#   The build name is ASCII only so no numbers, spaces, or semicolons.
#   Example: Doki Doki Yuri Time to DokiDokiYuriTime
define build.name = "DokiDokiModDocker"

# This controls the save folder name of your mod.
# Finding your Saves:
#   Windows: %AppData%/RenPy/
#   macOS: $HOME/Library/RenPy/ (Un-hide the Library Folder)
#   Linux: $HOME/.renpy/
define config.save_directory = "DD-ModDocker"

# This controls the window logo of your mod.
define config.window_icon = "sdc_system/DDMDLogo.png"

init python:
    build.executable_name = "DDMD"

    if len(renpy.loadsave.location.locations) > 1: del(renpy.loadsave.location.locations[1])
    renpy.game.preferences.pad_enabled = False
    def replace_text(s):
        s = s.replace('--', u'\u2014') 
        s = s.replace(' - ', u'\u2014') 
        return s
    config.replace_text = replace_text

    def game_menu_check():
        if quick_menu: renpy.call_in_new_context('_game_menu')

    config.game_menu_action = game_menu_check

    def force_integer_multiplier(width, height):
        if float(width) / float(height) < float(config.screen_width) / float(config.screen_height):
            return (width, float(width) / (float(config.screen_width) / float(config.screen_height)))
        else:
            return (float(height) * (float(config.screen_width) / float(config.screen_height)), height)

## Build configuration #########################################################
##
## This section controls how Ren'Py turns your project into distribution files.

init python:
    ## The following variables take file patterns. File patterns are case-
    ## insensitive, and matched against the path relative to the base directory,
    ## with and without a leading /. If multiple patterns match, the first is
    ## used.
    ##
    ## In a pattern:
    ##  * matches all characters, except the directory separator.
    ##  ** matches all characters, including the directory separator.
    ##
    ## Examples:
    ##  "*.txt" matches txt files in the base directory.
    ##  "game/**.ogg" matches ogg files in the game directory or any of its
    ## subdirectories.
    ##  "**.psd" matches psd files anywhere in the project.

    # These variables declare the packages to build your mod that is Team Salvato
    # IPG compliant. Do not mess with these variables whatsoever.
    # build.package("DDMD6",'zip','mod',description="Ren'Py 6 DDMD Build (Alpha)")
    # build.package("full",'zip','windows linux mac renpy mod all',description="Ren'Py 7 DDMD Build: All")
    build.package("ddmd-win",'zip','windows linux renpy mod all',description="Ren'Py 7 DDMD Build: Windows/Linux")
    build.package("ddmd-mac",'app-zip','mac renpy mod all',description="Ren'Py 7 DDMD Build: macOS")

    # These variables declare the archives that will be made to your packaged mod.
    # To add another archive, make a build.archive variable like in this example:
    build.archive("ddml", 'mod')
    build.archive("mod_patches", 'mod')
    
    #############################################################
    # These variables classify packages for PC and Android platforms.
    # Make sure to add 'all' to your build.classify variable if you are planning
    # to build your mod on Android like in this example.
    #   Example: build.classify("game/**.pdf", "scripts all")
    
    build.classify("game/**.rpyc", "ddml")
    build.classify("game/sdc_system/**", "ddml")
    build.classify("game/python-packages/**", "mod")
    build.classify("game/ddmc.json", "mod")
    build.classify("How to use DDMD (macOS).txt", "mod")
    build.classify("How to use DDMD (Windows, Linux).txt", "mod")
    build.classify("ddmd_settings.json", "mod")
    build.classify("game/mod_patches/**", "mod_patches")

    build.classify("game/MLSaves/**", None)
    build.classify("game/mods/**", None)
    build.classify("game/docker_custom_image.png", None)
    build.classify("game/firstrun", None)
    build.classify("BUILDING.md", None)
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('**.rpy', None)
    build.classify('**.psd', None)
    build.classify('**.sublime-project', None)
    build.classify('**.sublime-workspace', None)
    build.classify('/music/*.*', None)
    build.classify('script-regex.txt', None)
    build.classify('/game/10', None)
    build.classify('/game/cache/*.*', None)
    build.classify('**.rpa', None)
   
    # This sets' README.html as documentation
    build.documentation('README.html')

    build.include_old_themes = False
