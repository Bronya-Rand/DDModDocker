
init 1 python:

    def patched_file(fn):
        if ".." in fn:
            fn = fn.replace("..", config.basedir.replace("\\", "/"))

        return renpy.loader.load(fn)

    renpy.file = patched_file