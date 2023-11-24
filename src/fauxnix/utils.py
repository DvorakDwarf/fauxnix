import os
import ruamel.yaml

import config_parser as config_parser

def get_gen(dir: str) -> int:
    gen_section = dir.split("_")[0]
    gen_num = int(gen_section[1:])

    return gen_num

def get_sorted_gen(dirs: list) -> list:
    return sorted(dirs, key=get_gen)

def get_gen_dir(yaml: ruamel.yaml.YAML) -> str:
    config = config_parser.load_config(yaml)
    GENERATION_DIR = os.path.join(config["storage"], "fauxnix/generations")

    return GENERATION_DIR

def find_gen(dirs: list, target_gen: int) -> str:
    for dir in dirs:
        gen_num = get_gen(dir)
        #Everything after G
        if gen_num == target_gen:
            return dir

    return ""    

def get_pkglist_path(yaml: ruamel.yaml.YAML) -> str:
    storage = config_parser.load_config(yaml)["storage"]
    PKGLIST_PATH = os.path.join(storage, "fauxnix/pkglist.txt")

    return PKGLIST_PATH

def set_envs(config: dict):
    for env_name in config["env"]:
        os.environ[env_name] = config["env"][env_name]