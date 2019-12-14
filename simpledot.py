import subprocess
import argparse
import os
import time
import yaml

parser = argparse.ArgumentParser(description='Set up dotfiles.')
parser.add_argument('--config_file', '-f', required=True, help='Config file to use.')
parser.add_argument('--run', '-r', action='store_true', default=False)
parser.add_argument('--create_package', '-c', help='Create a new/empty package directory.')
args = parser.parse_args()

with open(args.config_file, 'r') as file:
    config_file = yaml.safe_load(file)

vendor_directory = config_file['vendor-directory']
if not os.path.exists(vendor_directory):
    print("Can't find vendor directory: " + vendor_directory + ". Please check your config file. Exiting.")
    exit()
shell_location = config_file['shell-location']
packages = config_file['packages']
sources_file = './sources.sh'
artifacts_folder = "./artifacts"
timestamp = str(int(time.time()))
log_file = "./artifacts/logs-" + timestamp + ".log"

# package structure from root of package
package_functions = {
    'depends': 'depends.sh',
    'exists': 'exists.sh',
    'install': 'install.sh',
    'remove': 'remove.sh',
    'source': 'source.sh'
}

# create artifacts folder to output generated artifacts
if not os.path.exists(artifacts_folder):
    os.mkdir(artifacts_folder)

def write_file(file, data, flags="a"):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, flags) as f:
        f.write(data)

def log(message):
    print(message)
    write_file(log_file, message + "\n")

# create a new package
if args.create_package is not None:
    package_location = vendor_directory + "/" + args.create_package
    package_scripts = {key: package_location + "/" + value for (key, value) in package_functions.items()}
    for key,file in package_scripts.items():
        write_file(file=file, data="")
    exit()

if args.run:
    # run the script
    for package_name in packages:
        package_location = vendor_directory + "/" + package_name
        package_scripts = {key: package_location + "/" + value for (key, value) in package_functions.items()}

        # check if package exists
        exists = subprocess.call([shell_location, package_scripts['exists']])
        if exists == 0:
            log("Package exists: " + package_name + ". Ignoring.")
            continue
        else:
            log("Package does not exist: " + package_name + ".")

        # check if any dependencies that are defined exist
        depends = subprocess.call([shell_location, package_scripts['depends']])
        if depends == 1:
            log("Package dependencies not met: " + package_name + ". See " + package_scripts['depends'] + ".")
            break
        else:
            log("Package dependencies met.")

        # install the package
        log("Installing package: " + package_name)
        subprocess.call([shell_location, package_scripts['install']])
        log("Package installed successfully: " + package_name)


    # build sources
    if os.path.exists(sources_file):
        src_loc = "./artifacts/sources-" + timestamp + ".bkp"
        log("Sources file exists. Backing up to: " + src_loc)
        os.rename(sources_file, src_loc)

    log("Creating new sources file.")
    for package_name in packages:
        vendor_directory = os.path.abspath(vendor_directory)
        package_location = vendor_directory + "/" + package_name
        package_scripts = {key: package_location + "/" + value for (key, value) in package_functions.items()}
        write_file(file=sources_file, data="source " + package_scripts['source'] + "\n", flags="a")
        log("Appended to sources file: " + package_scripts['source'])
    log("Sources file created successfully. Please add the following command to your .bashrc or .bash_profile:")
    log("source \"" + os.path.abspath(".") + "/sources.sh\"")