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

## Why use this over Nix/NixOS ?
When I used NixOS I felt like a neanderthal having to edit what packages I want in the config instead of just using a command like pacman. I didn't like Nix store and how it locks you into using Nix packages and breaking stuff you might normally install with git or some such. The gravest offense was the fact that osu! was laggy as hell. There are some other minor annoyances I had with Nix that all together made me crawl back into the inviting arms of Arch Linux and having full control over my system. If you relate to any of this but still like the idea of saving your system state and being able to reproduce it like me, you might like **fauxnix**
