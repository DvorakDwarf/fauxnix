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

def get_gen(dir: str) -> int:
    gen_section = dir.split("_")[0]
    print(gen_section)
    gen_num = int(gen_section[1:])

    print(gen_num)
    return gen_num

def get_sorted_gen() -> list:
    pass

def create_dir() -> str:
    with open(CONFIG_PATH, 'r') as file:
        #Unsafe ???
        config: dict = yaml.load(file)

    dirs = os.listdir(GENERATION_DIR)

    if len(dirs) == 0:
        new_gen_num = "0"
    else:
        #Take all gens, sort, find highest one, split along_, take 2nd character and following
        gen_num = get_gen(sorted(dirs)[-1])
        new_gen_num = str(gen_num + 1)
    
    current_date = str(date.today())
    new_gen_dir = os.path.join(GENERATION_DIR, str("G" + new_gen_num + "_" + current_date))
    os.mkdir(new_gen_dir)

    if len(dirs) > config["history_length"]:
        print(sorted(dirs)[0])

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
    if config["day_first"] == True:
        meta["date"] = now.strftime("%d/%m/%Y %H:%M:%S")
        meta["day_first"] = True
    elif config["day_first"] == False:
        meta["date"] = now.strftime("%m/%d/%Y %H:%M:%S")
        meta["day_first"] = False
    else:
        print("day_first variable in config is not a bool. Assuming true")
        meta["date"] = now.strftime("%d/%m/%Y %H:%M:%S")
        meta["day_first"] = True

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
        gen_num = get_gen(dir)
        #Everything after G
        if gen_num == target_gen:
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
    with open(CONFIG_PATH, 'r') as file:
        config = yaml.load(file)

    dirs = os.listdir(GENERATION_DIR)
    generations = []

    if len(dirs) == 0:
        print("No exisiting generations, try syncing first!")
        return

    for dir in sorted(dirs):
        #Always starts with Gx
        generation_num = dir[1]

        with open(os.path.join(GENERATION_DIR, dir, "meta.json")) as file:
            meta: dict = json.load(file)

        if config["day_first"] != meta["day_first"]:
            #Swap day and month around
            new_date = meta["date"].split('/')
            new_date[0], new_date[1] = new_date[1], new_date[0]
            meta["date"] = '/'.join(new_date)

        generations.append({"generation": generation_num, "date": meta["date"]})
    
    print("Available generations: ")
    for gen in generations:
        print(f"G{gen['generation']} - {gen['date']}")



