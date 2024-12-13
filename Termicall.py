import re
import os
import json
import pathlib
from colorama import Fore, Style, init

init(autoreset=True)


def user_usage(*args):
    """Display the list of available commands."""
    print(Fore.CYAN + Style.BRIGHT + "\n          [ Command List ]")
    print("""
          <*> -help                               : Show command list.
          <*> -add "<path>" as <alias>            : Add a program path with an alias.
          <*> -rename <alias> to <new-alias>      : Rename an existing alias.
          <*> -repath "<old-path>" to "<new-path>": Update the path of a program.
          <*> -rm <alias>                         : Remove a program by alias.
          <*> -ls                                 : Show the list of registered programs.
          <*> ex                                  : Exit the terminal session.
          """)
    print(Fore.CYAN + Style.BRIGHT + "          [ Examples ]")
    print("""
          > -help
          > -add "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" as google
          > -rename google to chrome
          > -rm chrome
          """)


class Console:
    """Console utility for managing programs and aliases."""
    FILE_PATH = "programs.json"
    
    def __init__(self, path: str, alias: str):
        self.path = path
        self.alias = alias

    @staticmethod
    def file_exists():
        """Ensure the JSON file exists and initialize if empty."""
        file_path = pathlib.Path(Console.FILE_PATH)
        if not file_path.exists() or os.path.getsize(file_path) == 0:
            with file_path.open("w") as f:
                json.dump([], f, indent=4)

    @staticmethod
    def read_data():
        """Read data from the JSON file."""
        Console.file_exists()
        with open(Console.FILE_PATH, "r") as f:
            return json.load(f)

    @staticmethod
    def write_data(data):
        """Write data to the JSON file."""
        with open(Console.FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)

    def add_program(self):
        """Add a new program with alias."""
        data = self.read_data()
        if any(entry["alias"] == self.alias for entry in data):
            print(Fore.RED + f"Alias '{self.alias}' already exists!")
            return

        data.append({"alias": self.alias, "path": self.path})
        self.write_data(data)
        print(Fore.GREEN + f"Program added with alias: '{self.alias}'")

    def show_list(*args):
        """Show the list of programs."""
        Console.file_exists()
        with open("programs.json", "r") as f:
            data = json.load(f)

        if data:
            print("Registered programs:")
            for entry in data:
                print(f"{entry['alias']} -> {entry['path']}")
        else:
            print("No programs registered.")

    @staticmethod
    def run_program(alias: str):
        """Run a program by its alias."""
        data = Console.read_data()
        for entry in data:
            if entry["alias"] == alias:
                os.system(f'"{entry["path"]}"')
                return
        print(Fore.RED + f"No program found with alias: '{alias}'")


class Filter:
    """Filter and process user input commands."""

    @staticmethod
    def separate_input(user_input: str):
        """Parse and execute user input commands."""
        commands = {
            "-add": Filter.add_command,
            "-rm": Filter.remove_command,
            "-rename": Filter.update_alias,
            "-repath": Filter.update_path,
            "-ls": Console.show_list,
            "-help": user_usage,
        }

        for cmd, func in commands.items():
            if user_input.startswith(cmd):
                func(user_input)
                return

        Console.run_program(user_input)

    @staticmethod
    def add_command(arg: str):
        """Add a new program."""
        match = re.match(r'-add "(.*?)" as (\w+)', arg)
        if match:
            path, alias = match.groups()
            if alias.lower() == "ex":
                print(Fore.RED + "Cannot use 'ex' as an alias.")
                return
            Console(path.replace("/", "\\"), alias).add_program()
        else:
            print(Fore.YELLOW + "Invalid syntax. Use: -add \"<path>\" as <alias>")

    @staticmethod
    def remove_command(arg: str):
        """Remove a program by alias."""
        match = re.match(r"-rm (\w+)", arg)
        if match:
            alias = match.group(1)
            data = Console.read_data()
            new_data = [entry for entry in data if entry["alias"] != alias]

            if len(data) == len(new_data):
                print(Fore.RED + f"No program found with alias: '{alias}'")
            else:
                Console.write_data(new_data)
                print(Fore.GREEN + f"Program with alias '{alias}' removed.")
        else:
            print(Fore.YELLOW + "Invalid syntax. Use: -rm <alias>")

    @staticmethod
    def update_alias(arg: str):
        """Rename an alias."""
        match = re.match(r"-rename (\w+) to (\w+)", arg)
        if match:
            old_alias, new_alias = match.groups()
            data = Console.read_data()

            for entry in data:
                if entry["alias"] == old_alias:
                    entry["alias"] = new_alias
                    Console.write_data(data)
                    print(Fore.GREEN + f"Alias '{old_alias}' renamed to '{new_alias}'.")
                    return

            print(Fore.RED + f"No program found with alias '{old_alias}'")
        else:
            print(Fore.YELLOW + "Invalid syntax. Use: -rename <alias> to <new-alias>")

    @staticmethod
    def update_path(arg: str):
        """Update the path of a program."""
        match = re.match(r'-repath "(.*?)" to "(.*?)"', arg)
        if match:
            old_path, new_path = match.groups()
            data = Console.read_data()

            for entry in data:
                if entry["path"] == old_path:
                    entry["path"] = new_path
                    Console.write_data(data)
                    print(Fore.GREEN + f"Path updated from '{old_path}' to '{new_path}'.")
                    return

            print(Fore.RED + f"No program found with path: '{old_path}'")
        else:
            print(Fore.YELLOW + "Invalid syntax. Use: -repath \"<old-path>\" to \"<new-path>\"")


if __name__ == "__main__":
    user_usage()
    while True:
        try:
            user_input = input(">> ").strip()
            if user_input.lower() == "ex":
                break
            Filter.separate_input(user_input)
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
