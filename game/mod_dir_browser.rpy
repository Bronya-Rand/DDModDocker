## Copyright 2022 Azariel Del Carmen (GanstaKingofSA)

init python:
    def can_access(path, drive=False):
        try:
            if not renpy.windows or drive:
                return os.access(path, os.R_OK)
            else:
                for x in os.listdir(path):
                    print(x)
                    break
        except OSError as e:
            if e.errno == 13 or e.errno == 2:
                return False
            raise
        return True


screen pc_directory(loc=None):
    modal True
    
    zorder 200
    style_prefix "pc_dir"

    drag:
        drag_name "file"
        drag_handle (0, 0, 1.0, 40)
        xsize 500
        ysize 300
        xpos 0.3
        ypos 0.3
        
        frame:

            python:
                if loc and loc != "drive":
                    current_dir = loc
                elif (loc == "drive" and renpy.windows):
                    current_dir = None
                else:
                    current_dir = persistent.ddml_basedir

                if current_dir is not None:
                    prev_dir = os.path.dirname(current_dir)
                    dir_size = len(os.listdir(current_dir))
                else:
                    net_drives = subprocess.check_output("powershell (Get-WmiObject -ClassName Win32_MappedLogicalDisk).Name", shell=True).replace("\r\n", "").split(":")
                    net_drives.pop(-1)
                    drives = subprocess.check_output("powershell (Get-PSDrive -PSProvider FileSystem).Name", shell=True).split("\r\n")
                    drives.pop(-1)
                    
                    for x in drives:
                        if x in net_drives:
                            drives.remove(x)
                         
            if (renpy.windows and loc != "drive") or (not renpy.windows and loc != "/"):
                hbox:
                    xalign 0.02 yoffset 6
                    imagebutton:
                        idle "sdc_system/file_app/OSBack.png"
                        hover LiveComposite((18, 18), (0, 0), Frame("#dbdbdd"), (0, 0), "sdc_system/file_app/OSBack.png")
                        action [Hide("pc_directory"), Show("pc_directory", loc=If(current_dir != prev_dir, prev_dir, "drive"))]

            hbox:
                ypos 0.005
                xalign 0.52 
                text "Select ZIP File"

            hbox:
                ypos -0.005
                xalign 0.98
                imagebutton:
                    idle "ddmd_close_icon"
                    hover "ddmd_close_icon_hover"
                    action [Hide("pc_directory", Dissolve(0.25))]
            
            side "c r":
                yoffset 35
                xoffset 5
                xsize 470
                ysize 250

                viewport id "fe":
                    #spacing 2
                    mousewheel True 
                    has vbox

                    if current_dir is None:
                        for x in drives:
                            hbox:
                                imagebutton:
                                    idle LiveComposite((460, 18), (0, 0), "ddmd_file_physical_drive", (18, 2), Text(x + ":/", substitute=False, size=10, style="pc_dir_text"))
                                    hover LiveComposite((460, 18), (0, 0), Frame("#dbdbdd"), (0, 0), "ddmd_file_physical_drive", (18, 2), Text(x + ":/", substitute=False, size=10, style="pc_dir_text"))
                                    action If(can_access(x + ":", True), [Hide("pc_directory"), Show("pc_directory", loc=x + ":/")], Show("ddmd_dialog", message="You do not have permission to access %s." % (x + ":/")))
                        for x in net_drives:
                            hbox:
                                imagebutton:
                                    idle LiveComposite((460, 18), (0, 0), "ddmd_file_network_drive", (18, 2), Text(x + ":/", substitute=False, size=10, style="pc_dir_text"))
                                    hover LiveComposite((460, 18), (0, 0), Frame("#dbdbdd"), (0, 0), "ddmd_file_network_drive", (18, 2), Text(x + ":/", substitute=False, size=10, style="pc_dir_text"))
                                    action If(can_access(x + ":"), [Hide("pc_directory"), Show("pc_directory", loc=x + ":/")], Show("ddmd_dialog", message="You do not have permission to access %s." % (x + ":/")))
                    else:
                        for x in os.listdir(current_dir):
                            if os.path.isdir(os.path.join(current_dir, x)):
                                hbox:
                                    imagebutton:
                                        idle LiveComposite((460, 18), (0, 0), "ddmd_file_folder", (18, 2), Text(x, substitute=False, size=10, style="pc_dir_text"))
                                        hover LiveComposite((460, 18), (0, 0), Frame("#dbdbdd"), (0, 0), "ddmd_file_folder", (18, 2), Text(x, substitute=False, size=10, style="pc_dir_text"))
                                        action If(can_access(os.path.join(current_dir, x)), [Hide("pc_directory"), Show("pc_directory", loc=os.path.join(current_dir, x))], Show("ddmd_dialog", message="You do not have permission to access %s." % os.path.join(current_dir, x).replace("\\", "/")))
                            elif os.path.join(current_dir, x).endswith(".zip"):
                                hbox:
                                    imagebutton:
                                        idle LiveComposite((460, 18), (0, 0), "ddmd_file_file", (18, 2), Text(x, substitute=False, size=10, style="pc_dir_text"))
                                        hover LiveComposite((460, 18), (0, 0), Frame("#dbdbdd"), (0, 0), "ddmd_file_file", (18, 2), Text(x, substitute=False, size=10, style="pc_dir_text"))
                                        action [Hide("pc_directory"), Show("mod_name_input", zipPath=os.path.join(current_dir, x))]
            
                vbar value YScrollValue("fe") xoffset 20 yoffset 10 ysize 240

## File Explorer
style pc_dir_frame is mods_frame
style pc_dir_button_text:
    color "#fff"
    outlines []
    text_align 0.0

style pc_dir_scrollbar:
    xsize 8
    ysize 96
    base_bar Frame("#222222")
    thumb Frame("sdc_system/file_app/FileExplorerHBar.png", tile=False)

style pc_dir_vscrollbar:
    xsize 8
    ysize 96
    base_bar Frame("#222222")
    thumb Frame("sdc_system/file_app/FileExplorerVBar.png", tile=False)

style pc_dir_text is pc_dir_button_text