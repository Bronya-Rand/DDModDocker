## Copyright 2023 Azariel Del Carmen (GanstaKingofSA)

init python:
    import tempfile
    import errno

    def can_access(path, drive=False):
        if drive:
            if os.name == "nt" and len(path) == 2 and path[1] == ":":
                return os.path.isdir(path)
            return False

        if os.name == "nt":
            try:
                temp = os.scandir(path)
                return True
            except OSError as e:
                if e.errno in (errno.EACCES, errno.EPERM) or 'WinError 59' in str(e):
                    return False
                raise
        else:
            return os.access(path, os.R_OK)
    
    def get_network_drives():
        result = subprocess.run("net use", check=True, shell=True, capture_output=True, text=True)
        output_lines = result.stdout.strip().split('\n')[1:]
        drives = [line.split()[1].rstrip(':') for line in output_lines if line.startswith('OK')]
        return drives

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

    python:
        title = ""
        if ml:
            title = _("Select DDML Mod Folder")
        elif mac:
            title = _("Select DDLC Mod Folder")
        else:
            title = _("Select DDLC Mod ZIP File")

    use ddmd_generic_window(title):
        
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
                    action [Hide("pc_directory"), Show("pc_directory", loc=If(current_dir != prev_dir, prev_dir, "drive"), ml=ml, mac=mac)]
        
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
                                action If(can_access(x + ":", True), [Show("pc_directory", loc=x + ":/", ml=ml, mac=mac)], Show("ddmd_dialog", message="You do not have permission to access %s." % (x + ":/")))
                    for x in net_drives:
                        hbox:
                            imagebutton:
                                idle Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Transform("ddmd_file_network_drive", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), 2), Text(x + ":/", substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                hover Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Frame("#dbdbdd"), (0, 0), Transform("ddmd_file_network_drive", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), int(2 * res_scale)), Text(x + ":/", substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                action If(can_access(x + ":"), [Show("pc_directory", loc=x + ":/", ml=ml, mac=mac)], Show("ddmd_dialog", message="You do not have permission to access %s." % (x + ":/")))
                else:
                    for x in os.scandir(current_dir):
                        if x.is_dir():
                            hbox:
                                imagebutton:
                                    idle Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Transform("ddmd_file_folder", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), 2), Text(x.name, substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                    hover Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Frame("#dbdbdd"), (0, 0), Transform("ddmd_file_folder", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), int(2 * res_scale)), Text(x.name, substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                    action If(can_access(os.path.join(current_dir, x.path)), [Show("pc_directory", loc=os.path.join(current_dir, x.path), ml=ml, mac=mac)], Show("ddmd_dialog", message="You do not have permission to access %s." % os.path.join(current_dir, x.path).replace("\\", "/")))
                        elif not mac and not ml:
                            if os.path.join(current_dir, x.path).endswith(".zip"):
                                hbox:
                                    imagebutton:
                                        idle Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Transform("ddmd_file_file", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), 2), Text(x.name, substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                        hover Composite((int(460 * res_scale), int(18 * res_scale)), (0, 0), Frame("#dbdbdd"), (0, 0), Transform("ddmd_file_file", size=(int(18 * res_scale), int(18 * res_scale))), (int(20 * res_scale), int(2 * res_scale)), Text(x.name, substitute=False, size=int(12 * res_scale), style="pc_dir_text"))
                                        action [Hide("pc_directory"), Show("mod_name_input", zipPath=os.path.join(current_dir, x.path))]
        
            vbar value YScrollValue("fe") xoffset 20 yoffset 10 ysize int(240 * res_scale)

        if mac or ml:
            if (renpy.windows and loc != "drive") or (not renpy.windows and loc != "/"):
                textbutton _("Select Current Folder"):
                    text_style "mods_button_text"
                    action If(mac, [Hide("pc_directory", Dissolve(0.25)), Show("mod_name_input", zipPath=current_dir, copy=True)], [Hide("pc_directory", Dissolve(0.25)), Function(transfer_data, ddmm_path=current_dir)])
                    text_size int(16 * res_scale)
                    xalign 0.95 yalign 0.98
