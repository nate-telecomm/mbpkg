### Molybdenum installer
import sys
import os
import requests
import platform
def root():
    if platform.system() != "Windows":
        if os.path.isdir("/data/data/com.termux/files"):
            return "termux"
        elif os.getuid() != 0:
            print("[#] This script requires root.")
            sys.exit(1)
print("Installing MBPKG")
print(f"[#] OS: {platform.system()}")
if platform.system() == "Windows":
    print("| [#] You are on Windows, therefore the script will only be downloaded")
root()

response = requests.get(f"https://dysprosium-data.github.io/mbpkg/mb.py")
if response.status_code == 200:
    if platform.system() != "Windows":
        if root() == "termux":
            open("/data/data/com.termux/files/usr/bin/mb", "w").write(response.text)
            os.system("chmod +x /data/data/com.termux/files/usr/bin/mb") 
        else:
            open("/usr/bin/mb", "w").write(response.text)
            os.system("chmod +x /usr/bin/mb")
    else:
        open("mb.py", "w").write(response.text)
