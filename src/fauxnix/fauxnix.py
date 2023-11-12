import os
import ruamel.yaml
import argparse

import arguments
import config

yaml = ruamel.yaml.YAML()

config = config.load_config(yaml)
os.setegid(config["gid"])
os.seteuid(config["uid"])

parser = argparse.ArgumentParser(
                prog='fauxnix',
                description='Declarative configuration for the people, not sysadmins '
                )

mxgroup = parser.add_mutually_exclusive_group()
mxgroup.add_argument('-s', '--sync', action='store_true',
                    help="create new generation") 
mxgroup.add_argument('-i', '--id', action='store_true',
                    help="place the user uid and gid in the config") 
mxgroup.add_argument('-l', '--list', action='store_true',
                    help="list existing generations") 
mxgroup.add_argument('-r', '--revert', type=int,
                    help="revert to previous generation. Takes generation #") 

args = parser.parse_args()

if args.sync == True:
    new_gen_dir = arguments.create_dir()
    arguments.copy_pkglist(new_gen_dir)
    arguments.copy_configs(new_gen_dir)

#Revert must come with an argument
elif args.revert != None:
    arguments.revert(args.revert)

    print("Succesfully reverted")

elif args.id == True:
    config = config.load_config(yaml)

    config["uid"] = os.getuid()
    config["gid"] = os.getgid()

    config.dump_config(yaml, config)

    print("Succesfully copied this user's gid and uid")

elif args.list == True:
    arguments.list()

else:
    parser.print_help()

        
