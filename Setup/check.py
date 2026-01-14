import os
import re
import sys
import time
from importlib import import_module
from pathlib import Path

import Setup.setup as setup
from utils.version import get_version


IMPORT_ALIASES = {
    "beautifulsoup4": "bs4",
    "python-nmap": "nmap",
}


def read_libs():
    modules = []
    slash = setup.commands['slash'][os.name]
    f = open('Setup' + slash + '/requirements.txt', 'r')
    for line in f:
        if line != "\n" and "LIBRERY" not in line:
            module = line.split(' ----> ')[0].strip(" ")
            package = line.split(' ----> ')[1].strip("\n").strip(" ")
            modules.append((module, package))
    return modules


def read_requirements():
    with open('requirements.txt', 'r') as f:
        for line in f:
            yield line.strip("\n")


def check(fun):
    """
    Check the libraries, if they are not istalled, it asks if to install the packeges automatically
    :return: void
    """

    def wrapper():
        logs_dir = Path('Logs')
        if not logs_dir.is_dir():
            print('[-] Logs directory does not exist, creating it')
            os.mkdir(str(logs_dir))

        mod = list(read_requirements())
        exceptions = []
        for item in mod:
            try:
                line = item.split("#", 1)[0].strip()
                if not line:
                    continue

                pkg = re.split(r"[<>=!~]+", line, maxsplit=1)[0]
                module_name = IMPORT_ALIASES.get(pkg, pkg)

                import_module(module_name)

            except ImportError:
                exceptions.append(item)

        if len(exceptions) > 0:
            print("[-] The following libraries are missing")
            time.sleep(1)
            for item in exceptions:
                print('\t%s' % item)
            print("\n")

            print('''To install the packeges needed:
                            python -m pip install <package name> \n ''')
            show = '''To install the packages manually:\n
                        \t python pip install <package name>\n If you want the program to install the packages
                         automatically, the following commands will be performed'''
            print(show)
            for item in exceptions:
                command = f"python -m pip install '{item}'"
                print(f'\t{command}')

            a = str(input('Do you want to install the packages atomatically???? y/n '))
            if str(a) == 'y':
                os.system(f"python -m pip install -r requirements.txt")
            elif a == 'n':
                # os.execv(sys.executable, [sys.executable] + sys.argv)
                print("[-] Install all packages if you want all functionalities to work")
                time.sleep(2)
                return fun()
            else:
                print('answer not valid')
                print('You need to answer yes (y) or no (n)')
                exit(0)

        print('[+] All the necessary packages are present')
        time.sleep(2)
        return fun()

    return wrapper
