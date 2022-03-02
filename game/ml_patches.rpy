
init 1 python:
    
    def patched_restore_character(names):
        if type(names) != list:
            raise Exception("'names' parameter must be a list. Example: [\"monika\", \"sayori\"].")

        for x in names:
            if renpy.android:
                try: renpy.file(os.environ['ANDROID_PUBLIC'] + "/characters/" + x + ".chr")
                except: open(os.environ['ANDROID_PUBLIC'] + "/characters/" + x + ".chr", "wb").write(renpy.file(x + ".chr").read())
            else:
                try: renpy.file(config.basedir + "/characters/" + x + ".chr")
                except: open(config.basedir + "/characters/" + x + ".chr", "wb").write(renpy.file(x + ".chr").read())

    restore_character = patched_restore_character