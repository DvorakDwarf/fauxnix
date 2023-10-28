import os
from datetime import date
import shutil
import yaml
import argparse
import subprocess
import json 

DIRNAME = os.path.dirname(__file__)
GENERATION_DIR = os.path.join(DIRNAME, "generations/")
CONFIG_PATH = os.path.join(DIRNAME, 'config.yml')
PKGLIST_PATH = os.path.join(DIRNAME, 'pkglist.txt')

def create_dir() -> str:
    length = 0
    for _, dirnames, _ in os.walk(GENERATION_DIR):
        length = len(dirnames)

        #Only care about first, next wasn't working, idk
        break

    new_gen_dir = os.path.join(GENERATION_DIR, str(date.today()) + " G" + str(length))
    os.mkdir(new_gen_dir)

    return new_gen_dir

def copy_pkglist(new_gen_dir: str):
    new_pkglist_path = os.path.join(DIRNAME, new_gen_dir, "pkglist.txt")
    shutil.copyfile(PKGLIST_PATH, new_pkglist_path)

#TODO
def copy_configs(new_gen_dir):
    with open(CONFIG_PATH, 'r') as file:
        config: dict = yaml.safe_load(file)
        meta: dict = {"og_paths": {}}
        for file_path in config['tracked_files']:
            filename = file_path.split('/')[-1]
            new_config_path = os.path.join(new_gen_dir, filename)
            shutil.copyfile(file_path, new_config_path)

            meta['og_paths'][filename] = file_path

        meta_path = os.path.join(DIRNAME, new_gen_dir, "meta.json")
        with open(meta_path, 'w') as file:
            json.dump(meta, file, indent=4)

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
    new_gen_dir = create_dir()
    copy_pkglist(new_gen_dir)
    copy_configs(new_gen_dir)

#Revert must come with an argument
elif args.revert != "":
    dirs = os.listdir(GENERATION_DIR)
    revert_dir = ""
    for dir in dirs:
        split = dir.split("G")
        #Everything after G
        if int(split[1]) == args.revert:
            revert_dir = dir

    revert_dir = os.path.join(GENERATION_DIR, revert_dir)

    with open(CONFIG_PATH, 'r') as file:
        config = yaml.safe_load(file)
        revert_command = config["update_command"] + revert_dir
        print(revert_command)
        # subprocess.Popen(revert_command)