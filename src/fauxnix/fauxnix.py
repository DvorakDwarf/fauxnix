import os
import ruamel.yaml
import argparse

import arguments
import config_parser

yaml = ruamel.yaml.YAML()

config_parser = config_parser.load_config(yaml)
os.setegid(config_parser["gid"])
os.seteuid(config_parser["uid"])

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
    new_gen_dir = arguments.create_dir(yaml)
    arguments.copy_pkglist(yaml, new_gen_dir)
    arguments.copy_configs(yaml, new_gen_dir)

#Revert must come with an argument
elif args.revert != None:
    arguments.revert(yaml, args.revert)

    print("Succesfully reverted")

elif args.id == True:
    config = config_parser.load_config(yaml)

    config_parser["uid"] = os.getuid()
    config_parser["gid"] = os.getgid()

    config_parser.dump_config(yaml, config)

    print("Succesfully copied this user's gid and uid")

elif args.list == True:
    arguments.list(yaml)

else:
    parser.print_help()

        
