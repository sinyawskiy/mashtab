# coding=utf-8
import os
import re
import csv
import json

filename_re = re.compile('^(user\d+).csv$')
OUTFILE = 'file.json'

class Command(object):
    def __init__(self, module_name, command_name, function_name):
        self.module_name = module_name
        self.command_name = command_name
        self.function_name = function_name
        self.param = []

    def add_param(self, user_name):
        exist = False
        for user in self.param:
            if user['user'] == user_name:
                exist = True
                break
        if not exist:
            self.param.append({
                'user': user_name
            })

    def get_dict_command(self):
        return {
            'param': [
                user['user'] for user in self.param
            ],
            'function': self.function_name,
            'name': self.command_name,
            'module': self.module_name
        }

    def __eq__(self, other):
        return self.function_name == other.function_name and \
               self.command_name == other.command_name and \
               self.module_name == other.module_name


if __name__ == '__main__':
    commands = []
    for filename in os.listdir('.'):
        if filename_re.match(filename):
            user_name = filename_re.findall(filename)[0]
            with open(filename, 'r') as user_file:
                # module name function
                for row in csv.reader(user_file, delimiter=';'):
                    new_command = Command(*row)
                    exist = False
                    for command in commands:
                        if command == new_command:
                            exist = True
                            command.add_param(user_name)
                            break
                    if not exist:
                        new_command.add_param(user_name)
                        commands.append(new_command)

    with open(OUTFILE, 'w') as json_file:
        json.dump({
            'commands': [command.get_dict_command() for command in commands]
        }, json_file)