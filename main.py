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

def select_section(config):
    while True:
        try:
            print("----- sections available (Ctrl+C to go back) -----")
            for s in config.sections(): print(f"[{s}]")
            sec = input("enter section to edit: ").strip()
            if sec in config: return sec
            print(f"section '{sec}' not found\n")
        except KeyboardInterrupt:
            print("\nReturning to menu...")
            return None

def select_key(config, section):
    while True:
        try:
            print(f"----- keys in [{section}] (Ctrl+C to go back) -----")
            for k in config[section]: print(f"{k}={config.get(section, k)}")
            key = input("enter key to edit: ").strip()
            if key in config[section]: return key
            print(f"key '{key}' not found\n")
        except KeyboardInterrupt:
            print("\nReturning to menu...")
            return None

def settings_flow():
    manager = SettingsManager(SETTINGS_INI, BACKUP_SETTINGS_INI)
    manager.display()
    
    while True:
        try:
            choice = input("1=edit\n2=save and exit\nenter choice: ").strip()
            print()
            if choice == "1":
                section = select_section(manager.config)
                if section is None: continue
                
                key = select_key(manager.config, section)
                if key is None: continue
                
                print(f"Current: {key}={manager.config.get(section, key)}")
                try:
                    new_val = input("enter new value (Ctrl+C to cancel): ")
                    manager.update_value(section, key, new_val)
                    print("\nUpdated view:")
                    manager.display()
                except KeyboardInterrupt:
                    print("\nEdit cancelled.")
            
            elif choice == "2":
                manager.save()
                break
            else:
                print("Invalid choice.")
        except KeyboardInterrupt:
            print("\nexiting settings editor...")
            break

def log_flow():
    try:
        path = input("enter file path to the log to search (Ctrl+C to go back): ")
        searcher = LogSearcher(LOG_RESULTS_TXT)
        searcher.search_and_export(path)
    except KeyboardInterrupt:
        print("\nReturning to menu...")

def main():
    while True:
        try:
            prompt = "1=edit settings.ini\n2=search log file\nSelection (Ctrl+C to exit): "
            user_input = input(prompt).strip()
            if user_input == "1":
                settings_flow()
            elif user_input == "2":
                log_flow()
            else:
                print("Invalid selection.\n")
        except KeyboardInterrupt:
            print("\ngoodbye!")
            os._exit(0)

if __name__ == "__main__":
    main()
