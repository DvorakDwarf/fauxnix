import os
import ruamel.yaml

DIRNAME = os.path.dirname(__file__)
POSSIBLE_PATHS = [
    os.path.join(os.environ["HOME"], ".config/fauxnix/fauxnix.yaml"),
    os.path.join(os.environ["HOME"], ".config/fauxnix/config.yaml"),
    os.path.join(DIRNAME, "fauxnix.yaml"), #local
    "/etc/fauxnix.yaml",
]

def find_config() -> str:
    for path in POSSIBLE_PATHS:
        if os.path.exists(path):
            if path == "/etc/fauxnix.yaml":
                print("Using default config in /etc/fauxnix.yaml")
                print("Please use fauxnix --init")

            return path

CONFIG_PATH = find_config()

#Why have references if you can't concat them ????
#Change return type to correct thing later
def load_config(yaml: ruamel.yaml.YAML, forced_local: bool = False) -> dict:  
    active_config = CONFIG_PATH

    if forced_local == True:
        active_config = os.path.join(DIRNAME, "fauxnix.yaml")

    with open(active_config, 'r') as file:
        #Unsafe ???
        config: dict = yaml.load(file)
        for idx in range(len(config["tracked_files"])):
            config["tracked_files"][idx] = ''.join(config["tracked_files"][idx])

    return config

def dump_config(yaml: ruamel.yaml.YAML, config: dict, forced_local: bool = False):
    active_config = CONFIG_PATH

    if forced_local == True:
        active_config = os.path.join(DIRNAME, "fauxnix.yaml")

    with open(active_config, 'w') as file:
        yaml.dump(config, file)

