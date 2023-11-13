import os
import subprocess
import ruamel.yaml
import json 
import shutil
from datetime import date, datetime

import config_parser

GENERATION_DIR = os.path.join(os.environ["HOME"], ".config/fauxnix/generations")
PKGLIST_PATH = os.path.join(os.environ["HOME"], ".config/fauxnix/pkglist.txt")

def get_gen(dir: str) -> int:
    gen_section = dir.split("_")[0]
    gen_num = int(gen_section[1:])

    return gen_num

def get_sorted_gen(dirs: list) -> list:
    return sorted(dirs, key=get_gen)

def create_dir(yaml: ruamel.yaml.YAML) -> str:
    config = config_parser.load_config(yaml)

    #The gens are sorted by the number in ascending order. Important
    try:
        dirs = os.listdir(GENERATION_DIR)
    except FileNotFoundError:
        print("Generations directory could not be found")
        print("Likely not initialized, please use fauxnix --init")
        quit()
    
    dirs = get_sorted_gen(dirs)

    if len(dirs) == 0:
        new_gen_num = "0"
    else:
        #Take all gens, sort, find highest one, split along_, take 2nd character and following
        gen_num = get_gen(dirs[-1])
        new_gen_num = str(gen_num + 1)
    
    current_date = str(date.today())
    new_gen_dir = os.path.join(GENERATION_DIR, str("G" + new_gen_num + "_" + current_date))
    os.mkdir(new_gen_dir)

    if len(dirs) > config["history_length"]:
        gen_difference = len(dirs) - config["history_length"]
        outdated_gens = dirs[0:gen_difference]
        for gen_dir in outdated_gens:
            gen_path = os.path.join(GENERATION_DIR, gen_dir)
            print(f"Deleting outdated generation: {gen_dir}")
            shutil.rmtree(gen_path)

    return new_gen_dir

def copy_pkglist(new_gen_dir: str):
    new_pkglist_path = os.path.join(new_gen_dir, "pkglist.txt")
    shutil.copyfile(PKGLIST_PATH, new_pkglist_path)

#TODO
def copy_configs(yaml: ruamel.yaml.YAML, new_gen_dir: str):
    config = config_parser.load_config(yaml)
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
        expanded_path = os.path.expandvars(file_path)
        filename = file_path.split('/')[-1]
        new_config_path = os.path.join(new_gen_dir, filename)
        try:
            shutil.copyfile(expanded_path, new_config_path)
        except FileNotFoundError:
            print(f"File {expanded_path} not found!!!")

        meta['og_paths'][filename] = file_path

    meta_path = os.path.join(new_gen_dir, "meta.json")
    with open(meta_path, 'w') as file:
        json.dump(meta, file, indent=4)

def revert(yaml: ruamel.yaml.YAML, target_gen: int):
    try:
        dirs = os.listdir(GENERATION_DIR)
    except FileNotFoundError:
        print("Generations directory could not be found")
        print("Likely not initialized, please use fauxnix --init")
        quit()
        
    revert_dir = ""
    for dir in dirs:
        gen_num = get_gen(dir)
        #Everything after G
        if gen_num == target_gen:
            revert_dir = dir

    revert_dir = os.path.join(GENERATION_DIR, revert_dir)

    config = config_parser.load_config(yaml)
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
        old_path = os.path.expandvars(meta["og_paths"][tracked_file])
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

def list(yaml: ruamel.yaml.YAML):
    try:
        dirs = os.listdir(GENERATION_DIR)
    except FileNotFoundError:
        print("Generations directory could not be found")
        print("Likely not initialized, please use fauxnix --init")
        quit()
    
    config = config_parser.load_config(yaml)
    generations = []

    if len(dirs) == 0:
        print("No exisiting generations, try syncing first!")
        return

    for dir in get_sorted_gen(dirs):
        #Always starts with Gx
        generation_num = get_gen(dir)

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

def initialize(yaml: ruamel.yaml.YAML):
    config = config_parser.load_config(yaml)
    config["uid"] = os.getuid()
    config["gid"] = os.getgid()

    home_dir = os.environ["HOME"]
    main_dir = os.path.join(home_dir, ".config/fauxnix")
    gen_dir = os.path.join(main_dir, "generations")
    pkglist_path = os.path.join(main_dir, "pkglist.txt")
    new_config_path = os.path.join(main_dir, "fauxnix.yaml")

    if os.path.exists(main_dir) == False:
        os.mkdir(main_dir)
        print(f"Created {main_dir}")

    if os.path.exists(gen_dir) == False:
        os.mkdir(gen_dir)
        print(f"Created {gen_dir}")


    if os.path.exists(pkglist_path) == False:
        #Create empty file
        with open(pkglist_path, "w") as file: 
            pass

        print(f"Created {pkglist_path}")

    #If config already there, does nothing. Otherwise copies new one
    old_config_path = config_parser.find_config()
    try:
        shutil.copyfile(old_config_path, new_config_path)
    except shutil.SameFileError:
        pass
    print(f"Copied {old_config_path} to {new_config_path}")

    config_parser.dump_config(yaml, config)

