### Simple Dot Files
* A simple, highly configurable, dotfile manager.

### Requirements
* Python3 
* Some bash scripting knowledge

### About
* I don't like managing my dotfile in a single giant kludgy file
* Also, don't like ansible's or other config management tools abstraction away from bash
* Define your package in a handful of bash scripts 
    * depends.sh - returns 0 or 1 if dependencies are installed
    * exists.sh - returns 0 or 1 if the package exists on the system already
    * install.sh - script run to install the package
    * remove.sh - script run to remove the package
    * source.sh -  source command(s) for the package. 

### Usage
1. Create your config file
    * see config-macos-bash.yaml for a documented example
1. Create your packages
    * run `python3 simpledot.py -c <your package name> -f <your config file name>`
    * You will see a directory created in your vendor-directory folder with your package name with empty scripts
1. Fill out one or more of the scripts in the package
    * all commands in the source.sh will be sourced and all commands in install.sh will be run
1. Add your new package name to your config file under the packages key
1. run `python3 simpledot.py -f <your config file name>`
    * this will install all of your install.sh files and create a sources.sh file to add to your .bash_profile

