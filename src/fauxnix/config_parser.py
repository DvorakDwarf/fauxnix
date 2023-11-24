import os
import ruamel.yaml

DIRNAME = os.path.dirname(__file__)
POSSIBLE_PATHS = [
    os.path.join(os.environ["HOME"], ".config/fauxnix/fauxnix.yaml"),
    os.path.join(os.environ["HOME"], ".config/fauxnix/config.yaml"),
    os.path.join(DIRNAME, "fauxnix.yaml"), #local
    "/etc/fauxnix.yaml",
]

print(POSSIBLE_PATHS)

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
def load_config(yaml: ruamel.yaml.YAML) -> dict:  
    active_config = CONFIG_PATH

    #If user is root, find first available home user
    #If you have multiple users using fauxnix, you are screwed
    if os.getuid() == 0:
        active_config = find_home()

    with open(active_config, 'r') as file:
        #Unsafe ???
        config: dict = yaml.load(file)
        for idx in range(len(config["tracked_files"])):
            config["tracked_files"][idx] = ''.join(config["tracked_files"][idx])

    return config

def dump_config(yaml: ruamel.yaml.YAML, config: dict):
    active_config = CONFIG_PATH

    #If user is root, find first available home user
    #If you have multiple active users with fauxnix, you are screwed
    if os.getuid() == 0:
        active_config = find_home()

    print(active_config)
    with open(active_config, 'w') as file:
        yaml.dump(config, file)

def find_home() -> str:
    potential_homes = os.listdir("/home")

    for home in potential_homes:
        home = os.path.join("/home", home)
        fauxnix_config = os.path.join(home, ".config/fauxnix/fauxnix.yaml")
        if os.path.exists(fauxnix_config):
            return fauxnix_config

    # print("Could not find config, defaulting")
    return CONFIG_PATH