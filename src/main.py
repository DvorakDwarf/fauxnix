import os
import ruamel.yaml
from datetime import date, datetime
import shutil
import argparse
import subprocess
import json 

DIRNAME = os.path.dirname(__file__)
GENERATION_DIR = os.path.join(DIRNAME, "generations/")
CONFIG_PATH = os.path.join(DIRNAME, 'config.yml')
PKGLIST_PATH = os.path.join(DIRNAME, 'pkglist.txt')
yaml = ruamel.yaml.YAML()

with open(CONFIG_PATH, 'r') as file:
    #Unsafe ???
    config: dict = yaml.load(file)
    os.setegid(config["gid"])
    os.seteuid(config["uid"])

def create_dir() -> str:
    length = 0
    for _, dirnames, _ in os.walk(GENERATION_DIR):
        length = len(dirnames)

        #Only care about first, next wasn't working, idk
        break

    new_gen_dir = os.path.join(GENERATION_DIR, str(date.today()) + "_G" + str(length))
    os.mkdir(new_gen_dir)

    return new_gen_dir

def copy_pkglist(new_gen_dir: str):
    new_pkglist_path = os.path.join(DIRNAME, new_gen_dir, "pkglist.txt")
    shutil.copyfile(PKGLIST_PATH, new_pkglist_path)

#TODO
def copy_configs(new_gen_dir):
    with open(CONFIG_PATH, 'r') as file:
        #Unsafe ???
        config: dict = yaml.load(file)

    now = datetime.now()
    meta: dict = {"og_paths": {}}
    meta["date"] = now.strftime("%d/%m/%Y, %H:%M:%S")

    for file_path in config['tracked_files']:
        filename = file_path.split('/')[-1]
        new_config_path = os.path.join(new_gen_dir, filename)
        shutil.copyfile(file_path, new_config_path)

        meta['og_paths'][filename] = file_path

    meta_path = os.path.join(DIRNAME, new_gen_dir, "meta.json")
    with open(meta_path, 'w') as file:
        json.dump(meta, file, indent=4)

def revert():
    dirs = os.listdir(GENERATION_DIR)
    revert_dir = ""
    for dir in dirs:
        split = dir.split("G")
        #Everything after G
        if int(split[1]) == args.revert:
            revert_dir = dir

    revert_dir = os.path.join(GENERATION_DIR, revert_dir)

    with open(CONFIG_PATH, 'r') as file:
        config = yaml.load(file)

    with open(os.path.join(revert_dir, "meta.json")) as file:
        meta: dict = json.load(file)

    for tracked_file in meta["og_paths"]:
        old_path = meta["og_paths"][tracked_file]
        tracked_file = os.path.join(revert_dir, tracked_file)
        shutil.copyfile(tracked_file, old_path)

    old_pkg_path = os.path.join(revert_dir, "pkglist.txt")
    revert_command = config["update_command"] + old_pkg_path
    subprocess.run(revert_command, shell=True)

    #Makes this unique to pacman, find more general workaround later
    subprocess.run("sudo pacman -D --asdeps $(pacman -Qqe)", shell=True)
    subprocess.run(f"sudo pacman -D --asexplicit $(<{old_pkg_path})", shell=True)
    subprocess.run("sudo pacman -Qtdq | sudo pacman -Rns -", shell=True)

parser = argparse.ArgumentParser(
                prog='fauxnix',
                description='Declarative configuration for the people, not sysadmins '
                )

mxgroup = parser.add_mutually_exclusive_group()
mxgroup.add_argument('-s', '--sync', action='store_true',
                    help="create new generation") 
mxgroup.add_argument('-r', '--revert', type=int,
                    help="revert to previous generation. Takes generation #") 
mxgroup.add_argument('-i', '--id', action='store_true',
                    help="place the user uid and gid in the config") 

args = parser.parse_args()

if args.sync == True:
    new_gen_dir = create_dir()
    copy_pkglist(new_gen_dir)
    copy_configs(new_gen_dir)

elif args.id == True:
    with open(CONFIG_PATH, 'r') as file:
        config = yaml.load(file)

    config["uid"] = os.getuid()
    config["gid"] = os.getgid()

    with open(CONFIG_PATH, 'w') as file:
        yaml.dump(config, file)

#Revert must come with an argument
elif args.revert != "":
    revert()

        