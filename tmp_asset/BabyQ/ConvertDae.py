#! usr/bin/python
# coding=utf-8
# Convert dae to compression version

import os
import zipfile
import shutil
import commands

compression = zipfile.ZIP_STORED


def add_folder_zip(zip_file, folder):
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        if os.path.isfile(path):
            process_dae_ifNeed(f, folder)
            zip_file.write(path)
        elif os.path.isdir(path):
            add_folder_zip(zip_file, path)


def zip_back(filename, top):
    # compress file back
    unzip_folder = filename
    zf_back = zipfile.ZipFile(filename + ".zip", 'w')
    if os.path.isfile(unzip_folder):
        process_dae_ifNeed(unzip_folder, top)
        zf_back.write(unzip_folder)
    elif os.path.isdir(unzip_folder):
        add_folder_zip(zf_back, unzip_folder)


# extract zip
def unzip_if_need(filename, topdir):
    path = filename
    if path.endswith(".dae") or path.endswith(".DAE"):
        process_dae_ifNeed(path, topdir)
        return False
    if zipfile.is_zipfile(path):
        print "process " + path
        zf1 = zipfile.ZipFile(path, 'r')
        for target_path1 in zf1.namelist():
            if not target_path1.startswith('__MACOSX/'):
                if not zf1.extract(target_path1, topdir):
                    return False
        return True


def process_dae_ifNeed(f, top):
    if f.endswith('.dae'):
        scn_assets = "old.scnassets"
        if not os.path.exists(scn_assets):
            os.mkdir(scn_assets)
        f_path = os.path.join(top, f)
        shutil.move(f_path, scn_assets + "/" + f)
        command = "xcrun copySceneKitAssets " + scn_assets + " -o new.scnassets"
        print "prcessing " + f
        commands.getstatusoutput(command)
        shutil.move("new.scnassets" + "/" + f, top)
        os.removedirs("new.scnassets")
        shutil.rmtree(scn_assets)


# main
cwd = os.getcwd()
for top, dirs, files in os.walk(os.getcwd()):
    for f in files:
        if unzip_if_need(f, top):
            os.remove(f)
            file_name, file_extension = os.path.splitext(f)
            zip_back(file_name, top)
            shutil.rmtree(file_name)










