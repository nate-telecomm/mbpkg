#!/usr/bin/env python3
import os
import socket
import sys
import platform
from pathlib import Path
from itertools import cycle
from shutil import get_terminal_size
import time
import requests
import inspect
import threading
from promethium import col
import re
import ast

def check_sudo():
    if platform.system() != "Windows":
        if os.path.isdir("/data/data/com.termux/files/"):
            return "termux"
        elif os.getuid() != 0:
            print(col.red + "Alert: Running MB uses root" + col.end)
            sys.exit(1)


class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = threading.Thread(target=self._animate, daemon=True)
        self.steps = ["|", "/", "-", "\\"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            time.sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

def install_crate(crate, url, installed):
    data = open(crate, "r").read()
    crate_info = re.search(r'crate:\[name="(.+?)", shard="(.+?)"\]', data)
    name = crate_info.group(1)
    shard = crate_info.group(2)

# Extracting packages
    packages = re.findall(r'pkg\["(.+?)"\]', data)

# Storing variables
    variables = {
        'name': name,
        'shard': shard,
        'packages': packages
    }

    print(f'Installing "{name}"')
    for pkg in packages:
        install(url, pkg, installed)
def install(url, package, installed, hide_output=False):
    try:
        if hide_output == False:
            if package in installed:
                loader = Loader(f'Reinstalling "{package}"', "Installed!", 0.09).start()
            else:
                loader = Loader(f'Installing "{package}"', "Installed!", 0.09).start()
        response = requests.get(f"{url.strip()}/{package}")
        if response.status_code == 200:
            if platform.system() == "Windows":
                open(f"{user_profile_dir}\\mbconf\\pkgs\\{package}", "w").write(response.text)
            else:
                if check_sudo() == "termux": 
                    open(f"/data/data/com.termux/files/usr/bin/{package}", "w").write(response.text)
                    os.system(f"chmod +x /data/data/com.termux/files/usr/bin/{package}")
                else:
                    open(f"/usr/bin/{package}", "w").write(response.text)
                    os.system(f"chmod +x /usr/bin/{package}")

        else:
            print("\nInstallation failed")
            if response.status_code == 404:
                print("Package not found")
            sys.exit(1)
        time.sleep(1)
        if hide_output == False:
            loader.stop()
        if platform.system() == "Windows":
            if package not in installed:
                open("{user_profile_dir}\\mbconf\\installed", "a").write(f"{package}\n")
        else:
            if package not in installed:
                open(f"{home_dir}/.config/mbconf/installed", "a").write(f"{package}\n")

    except IndexError:
        print("No package provided")

def read_conf():
    if platform.system() == "Windows":
        content = open(f"C:\\Users\\{os.getlogin()}\\mbconf\\mb.conf", "r").readlines()
        installed = [line.strip() for line in open(f"{user_profile_dir}\\mbconf\\installed", "r").readlines() if line.strip()]

    else:
        content = open(f"{home_dir}/.config/mbconf/mb.conf", "r").readlines()
        installed = [line.strip() for line in open(f"{home_dir}/.config/mbconf/installed", "r").readlines() if line.strip()]
    ver = content[3]
    ver = ver[6:]
    shard = content[4]
    shard = shard[8:]
    url = content[5]
    url = url[6:]
    return installed, content, ver, shard, url

def main():
    installed, content, ver, shard, url = read_conf()
    try:
        raise_no_flag_error = sys.argv[1]
        check_sudo()
        if sys.argv[1] == "shard-type":
            print(shard)
            print(url)
        elif sys.argv[1] == "ver":
            print(ver)
        elif sys.argv[1] == "install-crate":
            try:
                install_crate(sys.argv[2], url, installed)
            except IndexError:
                print("No crate provided")
        elif sys.argv[1] == "list-pkg":
            if platform.system() == "Windows":
                print(open(f"{user_profile_dir}\\mbconf\\installed").read())
            else:
                print(open(f"{home_dir}/.config/mbconf/installed").read())

        elif sys.argv[1].startswith("install"):
            if sys.argv[1] == "install":
                install(url, sys.argv[2], installed)
        elif sys.argv[1] == "remove":
            try:
                if sys.argv[2] in installed:
                    loader = Loader(f'Removing "{sys.argv[2]}"', "Removed!", 0.09).start()
                    time.sleep(1)
                    if platform.system() == "Windows":
                        lines = open(f"{user_profile_dir}\\mbconf\\installed", 'r').readlines()
                        with open(f"{user_profile_dir}\\mbconf\\installed", 'w') as file:
                            for line in lines:
                                if sys.argv[2] not in line:
                                    file.write(line)
                        os.remove(f"{user_profile_dir}\\mbconf\\pkgs\\{sys.argv[2]}")

                    else:
                        lines = open(f"{home_dir}/.config/mbconf/installed", 'r').readlines()
                        with open(f"{home_dir}/.config/mbconf/installed", 'w') as file:
                            for line in lines:
                                if sys.argv[2] not in line:
                                    file.write(line)
                        if check_sudo() == "termux":
                            os.remove(f"/data/data/com.termux/files/usr/bin/{sys.argv[2]}")
                        else:
                            os.remove(f"/usr/bin/{sys.argv[2]}")
                    loader.stop()
                else:
                    print("Package not installed")
            except IndexError:
                print("Nothing provided")
        elif sys.argv[1] == "install-url":
                try:
                    loader = Loader("Installing", "Installed!", 0.09).start()
                    response = requests.get(sys.argv[2])
                    if response.status_code == 200:
                        if platform.system() == "Windows":
                            open(f"{user_profile_dir}\\mbconf\\script", "w").write(response.text)
                        else:
                            open(f"/usr/bin/script", "w").write(response.text)
                    else:
                        print("\nInstallation failed")
                        sys.exit(1)
                    time.sleep(1)
                    loader.stop()
                except IndexError:
                    print("No URL provided")
        elif sys.argv[1] == "update":
            for package in installed:
                install(url, package, installed)
        elif sys.argv[1] == "change-shard":
            try:
                if sys.argv[2] in ("stable", "unstable"):
                    loader = Loader("Updating", "Finished!", 0.09).start()
                    time.sleep(3)
                    content[4] = f"shard = {sys.argv[2]}" + '\n'
                    content[5] = f"url = https://dysprosium-data.github.io/mbpkg/{sys.argv[2]}" + '\n'
                    with open(f"{user_profile_dir}\\mbconf\\mb.conf" if platform.system()=='Windows' else f"{home_dir}/.config/mbconf/mb.conf", 'w') as f:
                        f.writelines(content)
                    installed, content, ver, shard, url = read_conf()
                    for package in installed:
                        install(url, package, installed, True)
                    loader.stop()
                    print(f"Shard set to {sys.argv[2]} and packages updated.")
                else:
                    print(f"Unknown shard. (stable, unstable)")
            except IndexError:
                print("You didnt provide a shard to switch to.")
        else:
            print(f'Unknown command "{sys.argv[1]}"')
    except IndexError:
        print("""Molybdenum usage
mb [command] [data]

install: Installs a package
update: Updates all packages
shard-type: Returns your chosen shard
ver: Returns version
change-shard: Changes shard
remove: Uninstalls a package""")
        check_sudo()
def setup():
    check_sudo()
    print("""Molybdenum setup
Choose shard (can be changed later):
[1] Stable
[2] Unstable""")
    opt = input(": ")
    if opt == "1":
        print("Chosen: Stable shard")
    elif opt == "2":
        print("Chosen: Unstable shard")
    else:
        print("Invalid option")
        sys.kill(1)
    print("Creating config...")
    """
    The config has the following lines for the following data
    4: version
    5: current shard
    6: URL
    """
    config = f"""# Molybdenum config
# Currently, the config locates all the data based of their lines so DONT move the lines!

ver = 0.3
shard = {'stable' if opt=='1' else 'unstable'}
url = https://dysprosium-data.github.io/mbpkg/{'stable' if opt=='1' else 'unstable'}"""
    if platform.system() == "Windows":
        os.mkdir(f"C:\\Users\\{os.getlogin()}\\mbconf")
        os.mkdir(f"C:\\Users\\{os.getlogin()}\\mbconf\\pkgs")
        with open(f"{user_profile_dir}\\mbconf\\mb.conf", "w") as f:
            f.write(config)
        open(f"{user_profile_dir}\\mbconf\\installed", "w").write("\n")
    else:
        os.mkdir(f"{home_dir}/.config/mbconf")
        with open(f"{home_dir}/.config/mbconf/mb.conf", "w") as f:
            f.write(config)
        open(f"{home_dir}/.config/mbconf/installed", "w").write("\n")

    print("okay")


def start():
    global home_dir
    global user_profile_dir
    home_dir = Path.home()
    user_profile_dir = f"C:\\Users\\{os.getlogin()}\\"
    if platform.system() == "Windows":
        if os.path.isdir(f"{user_profile_dir}\\mbconf"):
            main()
        else:
            setup()
    else:
        if os.path.isdir(f"{home_dir}/.config/mbconf"):
            main()
        else:
            setup()
start()
