import os
import subprocess
import ruamel.yaml
import json 
import shutil
from datetime import date, datetime

DIRNAME = os.path.dirname(__file__)
GENERATION_DIR = os.path.join(DIRNAME, "generations/")
CONFIG_PATH = os.path.join(DIRNAME, 'config.yml')
PKGLIST_PATH = os.path.join(DIRNAME, 'pkglist.txt')
yaml = ruamel.yaml.YAML()

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
    meta["date"] = now.strftime("%d/%m/%Y %H:%M:%S")

    for file_path in config['tracked_files']:
        filename = file_path.split('/')[-1]
        new_config_path = os.path.join(new_gen_dir, filename)
        try:
            shutil.copyfile(file_path, new_config_path)
        except FileNotFoundError:
            print(f"File {file_path} not found!!!")

        meta['og_paths'][filename] = file_path

    meta_path = os.path.join(DIRNAME, new_gen_dir, "meta.json")
    with open(meta_path, 'w') as file:
        json.dump(meta, file, indent=4)

def revert(target_gen: int):
    dirs = os.listdir(GENERATION_DIR)
    revert_dir = ""
    for dir in dirs:
        split = dir.split("G")
        #Everything after G
        if int(split[1]) == target_gen:
            revert_dir = dir

    revert_dir = os.path.join(GENERATION_DIR, revert_dir)

    with open(CONFIG_PATH, 'r') as file:
        config = yaml.load(file)

    with open(os.path.join(revert_dir, "meta.json")) as file:
        meta: dict = json.load(file)

    old_pkg_path = os.path.join(revert_dir, "pkglist.txt")
    revert_command = config["update_command"] + old_pkg_path
    # subprocess.run(revert_command, shell=True)

    # #Makes this unique to pacman, find more general workaround later
    # subprocess.run("sudo pacman -D --asdeps $(pacman -Qqe)", shell=True)
    # subprocess.run(f"sudo pacman -D --asexplicit $(<{old_pkg_path})", shell=True)
    # subprocess.run("sudo pacman -Qtdq | sudo pacman -Rns -", shell=True)

    for tracked_file in meta["og_paths"]:
        old_path = meta["og_paths"][tracked_file]
        gen_file = os.path.join(revert_dir, tracked_file)
        try:
            shutil.copyfile(gen_file, old_path)
        except FileNotFoundError:
            print(f'The directory where the file "{tracked_file}" used to be isn\'t there anymore')
            answer = input("Do you wish to create the directory ? (Y/n) ").lower()
            if answer == "" or answer == "y":
                #Linux specific
                target_dir = old_path.split("/")
                target_dir.pop(-1)
                #LINUX SPECIFIC
                target_dir = '/'.join(target_dir)
                os.makedirs(target_dir)
                shutil.copyfile(gen_file, old_path)

            else:
                print("The file was not copied. Make sure this did not break anything")


def list():
    dirs = os.listdir(GENERATION_DIR)
    generations = []
    for dir in dirs:
        split = dir.split("G")
        generation_num = split[-1]

        with open(os.path.join(GENERATION_DIR, dir, "meta.json")) as file:
            meta: dict = json.load(file)

        generations.append({"generation": generation_num, "date": meta["date"]})

    print("Available generations: ")
    for gen in generations:
        print(f"G{gen['generation']} - {gen['date']}")
