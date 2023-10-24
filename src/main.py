import os
from datetime import date
import shutil
import yaml

GENERATION_DIR = "generations/"

def create_dir() -> str:
    length = 0
    for _, dirnames, _ in os.walk(GENERATION_DIR):
        length = len(dirnames)

        #Only care about first
        break

    dir_name = os.path.join(GENERATION_DIR, str(date.today()) + " G" + str(length))
    os.mkdir(dir_name)

    return dir_name

def copy_pkglist(dir_name: str):
    pkglist_dir = os.path.join(dir_name, "pkglist.txt")
    shutil.copyfile("pkglist.txt", pkglist_dir)

def copy_configs(dir_name):
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
        # print(config['tracked_files'])

dir_name = create_dir()
copy_pkglist(dir_name)
copy_configs(dir_name)


