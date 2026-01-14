import os
import sys
import time
import traceback

import Setup.setup as setup
import modules.Attack.core as core
import utils.utils as includes


def max_index(dictionary):
    """
    returns the bigger index < 98 on the current menu
    :param dictionary:
    :return: maxIndex: int
    """
    if dictionary.get(98):
        del dictionary[98]
    elif dictionary.get(99):
        del dictionary[99]
    return max(list(dictionary.keys()))


class Directory:

    def __init__(self, dict_data: dict, flag: int):
        self.dict = dict_data
        self.flag = flag
        self.old_flag = None

    def show(self):
        for key in self.dict:
            print("%d) %s" % (key, self.dict[key]))

    def change_directory(self, new_dict: dict, new_flag: str):
        self.old_flag = self.flag
        self.dict = new_dict
        self.flag = new_flag

    @staticmethod
    def clear_screen():
        os.system(includes.command(setup.commands, 'clear'))


class Router:

    def __init__(self, dire, directories, links, attack):
        self.dire = dire
        self.attack = attack
        self.dirS = directories
        self.links = links

    def start(self):
        while 1:

            self.dire.show()
            try:
                x = int(input(">> "))
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(0)
            except ValueError:
                print("\n[-] Input must be an integer\n")
                continue
            except Exception as e:
                print("\n[-] Exception occored\n")
                print(e)
                includes.exception_handler(traceback.format_exc(), "controller/")
                raise Exception

            if x == 99:
                sys.exit(0)
            elif x == 98:
                self.dire.change_directory(self.dirS[self.dire.old_flag], self.dire.old_flag)
                self.dire.clear_screen()
                continue
            elif x > max_index(self.dire.dict):
                print('\n[-]', x, "is not a valid argument\n")
                continue
            if any(self.links[i][0] in list(self.dire.dict.values()) and x == self.links[i][1] for i in
                   range(len(self.links))):
                self.dire.change_directory(self.dirS[x], x)
            else:
                self.attack.name = self.dire.dict[x]
                self.attack.run()

            self.dire.clear_screen()


class Attack:

    def __init__(self, dire):
        self.name = ""
        self.dire = dire

    def run(self):
        attack = core.Core(self.name)
        attack.run()
