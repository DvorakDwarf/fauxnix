# fauxnix (pho-nix)
Non-invasive* Reproducible* Declarative* config management for Nix non-believers
![2023-11-19_18-32](https://github.com/DvorakDwarf/fauxnix/assets/96934612/7d091ce7-4d95-4ea9-a87a-e568ca3871e5)

## What is this ?
It's an Arch Linux python script to store and restore past states of your PC. Everytime you install a package it creates a new generation folder containing your full list of packages at the time as well as any config files you told it to track. 

## What can it do ?
* Save the packages installed on your system everytime you install something new (`fauxnix -s`)
* Save the config files you specify
* Let you modify your important config files in one place
* View existing generation (`fauxnix -l`)
* Revert to a previous generation (`fauxnix -r GENERATION_NUMBER`)
* Reconstruct your system on a new machine given you copied the generation you want to revert to
* Let you keep saying you use arch, btw

## Installation
1. Use your AUR helper of choice on `fauxnix-git` such as `paru -S fauxnix-git` or clone this repo
2. Run `fauxnix --init` as the user
3. Edit the config in `fauxnix.yaml` inside `~/.config/fauxnix` according to the instructions inside
4. `fauxnix --help` for all commands
5. PROFIT

