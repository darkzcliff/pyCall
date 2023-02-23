"""
    Beta. v1.0
"""

import json, re
import pathlib, os

def user_usage():
        print(""" Usage :
        <*> -add <path> as <alias>              : add path of program and call it uses alias.
        <*> -rename <alias> to <new-alias>      : rename current alias to the new one.
        <*> -repath <old-path> to <new-path>    : replace old path of program to the new one.
        <*> -rm <alias>                         : remove program.
        <*> -ls                                 : show list of programs.
        <*> ex                                  : exit -- end terminal session.
        """)

class console:
    def __init__(self, path, alias):
        self.path = path
        self.alias = alias

    def check_file(self):
        location = pathlib.Path("programs.json")
        if location.exists() and os.path.getsize(location) == 0:
            self.default_json()

        elif location.exists():
            with open("programs.json", 'r') as file:
                data = json.load(file)
                data.append({
                    "alias": "{}".format(self.alias),
                    "path": "{}".format(self.path),
                },)
            with open("programs.json", 'w') as write_file:
                json.dump(data, write_file, indent=4)

        else:
            self.default_json(self)

    def default_json(self):
        set_format = self.format_json()
        object = json.dumps(set_format, indent=4)

        with open("programs.json", 'w') as opened:
            opened.write(object)
            opened.close()

    def format_json(self):
        return { 
            "alias": "{}".format(self.alias), 
            "path": "{}".format(self.path),
            },

    def run_program(cmd):
        with open("programs.json", 'r') as read_file:
            data = json.load(read_file)
            for name in data:
                if(name['alias'] == cmd):
                    # print(name['alias'], name['path'])
                    launch = '\"{}\"'.format(name['path'])
                    os.system(launch)


class filter:
    def separate_input(user_input):
        if user_input[0:4] == "-add":
            filter.add_command(user_input)

        elif user_input[0:3] == "-rm":
            filter.remove_command(user_input)
        
        elif user_input[0:7] == "-rename":
            filter.update_alias(user_input)

        elif user_input[0:7] == "-repath":
            filter.update_path(user_input)

        elif user_input == "-ls":
            filter.show_list()

        else: 
            console.run_program(user_input)

    def add_command(arg):
        rep = arg.replace('\'', '\"')
        separator = rep.split('\"')
        if separator[0] == "-add ":
            identity = separator[2].split(' ')
            reg = re.search('[\W]', identity[2]) # check if string got special characters
            if identity[1] == "as" and bool(reg) == False:
                con = console(separator[1].replace('/', '\\'), identity[2])
                con.check_file()
            elif bool(reg) == True:
                print("Special characters are forbid")
            elif identity[2] == "ex":
                print("Can't use 'ex' as alias.")

    def remove_command(arg):
        separator = arg.split(" ")
        if separator[0] == "-rm":
            with open("programs.json", 'r') as read_file:
                data = json.load(read_file)
                for index, name in enumerate(data):
                    if name['alias'] == separator[1]:
                        data.pop(index)
                        read_file.close()
                        break
            
            with open("programs.json", 'w') as write_file:
                target = json.dumps(data, indent=4)
                write_file.write(target)
                write_file.close()

    def update_alias(arg):
        separator = arg.split(" ")
        if separator[0] == "-rename" and separator[2] == "to":
            with open("programs.json", 'r') as get_update:
                data = json.load(get_update)
                for name in data:
                    if name['alias'] == separator[1]:
                        name['alias'] = name['alias'].replace(f"{name['alias']}", separator[3])
                        break
            
            with open("programs.json", 'w') as apply_update:
                json.dump(data, apply_update, indent=4)
                apply_update.close()

    def update_path(arg):
        separator = arg.split(" ")
        if separator[0] == "-repath" and separator[2] == "to":
            with open("programs.json", 'r') as get_update:
                data = json.load(get_update)
                for name in data:
                    if name['path'] == separator[1]:
                        name['path'] = name['path'].replace(f"{name['path']}", separator[3])
                        break
            
            with open("programs.json", 'w') as apply_update:
                json.dump(data, apply_update, indent=4)
                apply_update.close()

    def show_list():
        with open("programs.json", 'r') as f:
            db = json.load(f)
            for program in db:
                print(program['alias'], " <> ", program['path'])
            f.close()


if __name__ == '__main__':
    while True:
        try:
            user = input('>> ')
            if user == 'ex':
                break
            else:
                filter.separate_input(user)
        except:
            continue