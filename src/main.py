import os
from datetime import date
import shutil
import yaml
import argparse
import subprocess

GENERATION_DIR = "src/generations/"

def create_dir() -> str:
    length = 0
    for _, dirnames, _ in os.walk(GENERATION_DIR):
        length = len(dirnames)

        #Only care about first, next wasn't working, idk
        break

    dir_name = os.path.join(GENERATION_DIR, str(date.today()) + " G" + str(length))
    os.mkdir(dir_name)

    return dir_name

def copy_pkglist(dir_name: str):
    pkglist_dir = os.path.join(dir_name, "pkglist.txt")
    shutil.copyfile("src/pkglist.txt", pkglist_dir)

#TODO
def copy_configs(dir_name):
    with open('src/config.yml', 'r') as file:
        config = yaml.safe_load(file)
        for file in config:
            config_path = os.path.join(dir_name)
            shutil.copyfile("src/pkglist.txt", pkglist_dir)

        # print(config['tracked_files'])

parser = argparse.ArgumentParser(
                prog='fauxnix',
                description='Declarative configuration for the people, not sysadmins '
                )

mxgroup = parser.add_mutually_exclusive_group()

mxgroup.add_argument('-s', '--sync', action='store_true',
                    help="create new generation") 
mxgroup.add_argument('-r', '--revert', type=int,
                    help="revert to previous generation. Takes generation #") 

args = parser.parse_args()

if args.sync == True:
    dir_name = create_dir()
    copy_pkglist(dir_name)
    copy_configs(dir_name)

elif args.revert != "":
    dirs = os.listdir(GENERATION_DIR)
    revert_dir = ""
    for dir in dirs:
        split = dir.split("G")
        #Everything after G
        if int(split[1]) == args.revert:
            revert_dir = dir

    revert_dir = os.path.join(GENERATION_DIR, revert_dir)

    with open('src/config.yml', 'r') as file:
        config = yaml.safe_load(file)
        revert_command = config["update_command"] + revert_dir
        print(revert_command)
        subprocess.Popen(revert_command)