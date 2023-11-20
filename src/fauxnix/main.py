#!/usr/bin/env python

import os
import ruamel.yaml
import argparse

import fauxnix.arguments as arguments
import fauxnix.config_parser as config_parser

def main():
    yaml = ruamel.yaml.YAML()

    config = config_parser.load_config(yaml)
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
    mxgroup.add_argument('-in','--init', action='store_true',
                        help="Run this after installation as the user for stuff to work") 

    args = parser.parse_args()

    if args.sync == True:
        try:
            new_gen_dir = arguments.create_dir(yaml)
        except PermissionError:
            print("fauxnix not configured yet. Run fauxnix --init as user first")
            exit()
        
        arguments.copy_pkglist(new_gen_dir)
        arguments.copy_configs(yaml, new_gen_dir)

        print(f"Synced succesfully at {new_gen_dir}")

    #Revert must come with an argument
    elif args.revert != None:
        arguments.revert(yaml, args.revert)
        print("Succesfully reverted")

    elif args.id == True:
        config = config_parser.load_config(yaml)

        config["uid"] = os.getuid()
        config["gid"] = os.getgid()

        config_parser.dump_config(yaml, config)

        print("Succesfully copied this user's gid and uid")

    elif args.list == True:
        arguments.list(yaml)

    elif args.init == True:
        arguments.initialize(yaml)
        print("Succesfully initialized. Modify ~/.config/fauxnix/fauxnix.yaml to add tracked files and change settings")
        print("Please uncomment whichever update_command you will use (paru/pacman/whatever)")

    else:
        parser.print_help()

#Bad practice ?
#Here for easier testing
if __name__ == "__main__":
    main()