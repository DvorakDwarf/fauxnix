import os
import ruamel.yaml

POSSIBLE_PATHS = [
    "~/.config/fauxnix/fauxnix.yaml",
    "~/.config/fauxnix/config.yaml",
    "fauxnix.yaml" #local
    "/etc/fauxnix.yaml",
]

def find_config() -> str:
    for path in POSSIBLE_PATHS:
        if os.path.exists(path):
            return path

CONFIG_PATH = find_config()

#Why have references if you can't concat them ????
#Change return type to correct thing later
def load_config(yaml: ruamel.yaml.YAML) -> dict:    
    with open(CONFIG_PATH, 'r') as file:
        #Unsafe ???
        config: dict = yaml.load(file)
        for idx in range(len(config["tracked_files"])):
            config["tracked_files"][idx] = ''.join(config["tracked_files"][idx])

    return config

def dump_config(yaml: ruamel.yaml.YAML, config: dict):
    with open(CONFIG_PATH, 'w') as file:
        yaml.dump(config, file)

