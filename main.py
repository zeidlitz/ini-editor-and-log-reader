import configparser
import re
import os
import copy

SETTINGS_INI = "settings.ini"
BACKUP_SETTINGS_INI = f"{SETTINGS_INI}.bak"
LOG_RESULTS_TXT = "log_results.txt"


class SettingsManager:
    def __init__(self, file_path, backup_path):
        self.file_path = file_path
        self.backup_path = backup_path
        self.config = configparser.ConfigParser()
        self.config.read(self.file_path)
        self.original_config = copy.deepcopy(self.config)

    def display(self):
        for section in self.config.sections():
            print(f"[{section}]")
            for key in self.config[section]:
                print(f"{key}={self.config.get(section, key)}")
            print()

    def update_value(self, section, key, value):
        if section in self.config and key in self.config[section]:
            self.config.set(section, key, value)
            return True
        return False

    def save(self):
        print(f"saving to {self.file_path}...")
        with open(self.file_path, "w") as f:
            self.config.write(f)

        print(f"saving original backup to {self.backup_path}...")
        with open(self.backup_path, "w") as f:
            self.original_config.write(f)


class LogSearcher:
    def __init__(self, output_path):
        self.output_path = output_path
        self.pattern = re.compile(r"(?:ERROR|WARNING|\d{1,3}(?:\.\d{1,3}){3})")

    def search_and_export(self, input_path):
        matches = []
        try:
            with open(input_path, "r") as file:
                for line in file:
                    if self.pattern.search(line):
                        matches.append(line)

            print(f"writing matches to {self.output_path}")
            with open(self.output_path, "w") as file:
                file.writelines(matches)
        except FileNotFoundError:
            print("File not found. Please check the path.")


def main():
    try:
        while True:
            prompt = "1=edit settings.ini\n2=search log file\nSelection: "
            user_input = input(prompt).strip()
            if user_input == "1":
                settings_flow()
                break
            elif user_input == "2":
                log_flow()
                break
            else:
                print("Invalid selection. Please enter 1 or 2.\n")
    except KeyboardInterrupt:
        print("\nexiting without saving\ngoodbye!")
        os._exit(1)


def settings_flow():
    manager = SettingsManager(SETTINGS_INI, BACKUP_SETTINGS_INI)
    manager.display()

    while True:
        try:
            choice = int(input("1=edit\n2=save and exit\nenter choice: "))
            print()
            if choice == 1:
                section = select_section(manager.config)
                key = select_key(manager.config, section)
                print(f"{key}={manager.config.get(section, key)}")
                new_val = input("enter new value: ")
                manager.update_value(section, key, new_val)
                manager.display()
            elif choice == 2:
                manager.save()
                os._exit(0)
        except ValueError:
            print("could not parse selection as integer")


def log_flow():
    path = input("enter file path to the log to search: ")
    searcher = LogSearcher(LOG_RESULTS_TXT)
    searcher.search_and_export(path)


def select_section(config):
    while True:
        print("----- sections available -----")
        for s in config.sections():
            print(f"[{s}]")
        sec = input("enter section to edit: ")
        if sec in config:
            return sec
        print("section not found\n")


def select_key(config, section):
    while True:
        print("----- keys available -----")
        for k in config[section]:
            print(f"{k}={config.get(section, k)}")
        key = input("enter key to edit: ")
        if key in config[section]:
            return key
        print("key not found\n")


if __name__ == "__main__":
    main()
