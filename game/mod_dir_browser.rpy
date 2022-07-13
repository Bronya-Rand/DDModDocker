## Copyright 2022 Azariel Del Carmen (GanstaKingofSA)

init python:
    def can_access(path, drive=False):
        try:
            if not renpy.windows or drive:
                return os.access(path, os.R_OK)
            else:
                for x in os.listdir(path):
                    break
        except OSError as e:
            if e.errno == 13 or e.errno == 2 or e.errno == 22:
                return False
            raise
        return True
    
    def get_network_drives():
        temp = subprocess.run("powershell (Get-WmiObject -ClassName Win32_MappedLogicalDisk).Name", check=True, shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8").replace("\r\n", "").split(":")
        temp.pop(-1)
        return temp

    def get_physical_drives(net_drives):
        temp = subprocess.run("powershell (Get-PSDrive -PSProvider FileSystem).Name", check=True, shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8").split("\r\n")
        temp.pop(-1)

        for x in temp:
            if x in net_drives:
                temp.remove(x)
        return temp

screen pc_directory(loc=None, ml=False, mac=False):
    modal True
    
    zorder 200
    style_prefix "pc_dir"

    drag:
        drag_name "file"
        drag_handle (0, 0, 1.0, 40)
        xsize int(500 * res_scale)
        ysize int(300 * res_scale)
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
                    net_drives = get_network_drives()
                    drives = get_physical_drives(net_drives)
                         
            if (renpy.windows and loc != "drive") or (not renpy.windows and loc != "/"):
                hbox:
                    xalign 0.02 yoffset 6
                    imagebutton:
                        idle Transform("sdc_system/file_app/OSBack.png", size=(int(18 * res_scale), int(18 * res_scale)))
                        hover Composite((int(18 * res_scale), int(18 * res_scale)), (0, 0), Frame("#dbdbdd"), (0, 0), Transform("sdc_system/file_app/OSBack.png", size=(int(18 * res_scale), int(18 * res_scale))))
                        action [Hide("pc_directory"), Show("pc_directory", loc=If(current_dir != prev_dir, prev_dir, "drive"))]

            hbox:
                ypos 0.005
                xalign 0.52
                if ml:
                    text "Select DDML Mod Folder"
                elif mac:
                    text "Select DDLC Mod Folder"
                else:
                    text "Select DDLC Mod ZIP File"

            hbox:
                ypos -0.005
                xalign 0.98
                imagebutton:
                    idle Transform("ddmd_close_icon", size=(int(36 * res_scale), int(36 * res_scale)))
                    hover Transform("ddmd_close_icon_hover", size=(int(36 * res_scale), int(36 * res_scale)))
                    action [Hide("pc_directory", Dissolve(0.25))]
            
            side "c r":
                yoffset int(45 * res_scale)
                xoffset int(5 * res_scale)
                xsize int(470 * res_scale)
                ysize int(250 * res_scale)

                viewport id "fe":
                    #spacing 2
                    mousewheel True 
                    has vbox

                    if current_dir is None:
                        for x in drives:
                            hbox:
                                imagebutton:
                                    idle Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Transform("ddmd_file_physical_drive", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), int(2 * res_scale)), Text(x + ":/", substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                    hover Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Frame("#dbdbdd"), (0, 0), Transform("ddmd_file_physical_drive", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), int(2 * res_scale)), Text(x + ":/", substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                    action If(can_access(x + ":", True), [Hide("pc_directory"), Show("pc_directory", loc=x + ":/")], Show("ddmd_dialog", message="You do not have permission to access %s." % (x + ":/")))
                        for x in net_drives:
                            hbox:
                                imagebutton:
                                    idle Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Transform("ddmd_file_network_drive", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), 2), Text(x + ":/", substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                    hover Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Frame("#dbdbdd"), (0, 0), Transform("ddmd_file_network_drive", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), int(2 * res_scale)), Text(x + ":/", substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                    action If(can_access(x + ":"), [Hide("pc_directory"), Show("pc_directory", loc=x + ":/")], Show("ddmd_dialog", message="You do not have permission to access %s." % (x + ":/")))
                    else:
                        for x in os.listdir(current_dir):
                            if os.path.isdir(os.path.join(current_dir, x)):
                                hbox:
                                    imagebutton:
                                        idle Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Transform("ddmd_file_folder", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), 2), Text(x, substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                        hover Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Frame("#dbdbdd"), (0, 0), Transform("ddmd_file_folder", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), int(2 * res_scale)), Text(x, substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                        action If(can_access(os.path.join(current_dir, x)), [Hide("pc_directory"), Show("pc_directory", loc=os.path.join(current_dir, x))], Show("ddmd_dialog", message="You do not have permission to access %s." % os.path.join(current_dir, x).replace("\\", "/")))
                            elif not mac and not ml:
                                if os.path.join(current_dir, x).endswith(".zip"):
                                    hbox:
                                        imagebutton:
                                            idle Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Transform("ddmd_file_file", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), 2), Text(x, substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                            hover Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Frame("#dbdbdd"), (0, 0), Transform("ddmd_file_file", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), int(2 * res_scale)), Text(x, substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                            action [Hide("pc_directory"), Show("mod_name_input", zipPath=os.path.join(current_dir, x))]
            
                vbar value YScrollValue("fe") xoffset 20 yoffset 10 ysize int(240 * res_scale)

            if mac or ml:
                if (renpy.windows and loc != "drive") or (not renpy.windows and loc != "/"):
                    textbutton "Select Current Folder":
                        text_style "mods_button_text"
                        action If(mac, [Hide("pc_directory", Dissolve(0.25)), Function(transfer_data, ddmm_path=current_dir)], [Hide("pc_directory", Dissolve(0.25)), Show("mod_name_input", zipPath=current_dir, copy=True)])
                        text_size int(16 * res_scale)
                        xalign 0.95 yalign 0.98
