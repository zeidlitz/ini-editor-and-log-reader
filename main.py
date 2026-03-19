import configparser
import re
import os

SETTINGS_INI = "settings.ini"
BACKUP_SETTINGS_INI = f"{SETTINGS_INI}.bak"
LOG_RESULTS_TXT = "log_results.txt"


def main():
    try:
        while True:
            prompt = "1=edit settings.ini\n2=search log file\nSelection: "
            user_input = input(prompt).strip()
            match user_input:
                case "1":
                    edit_settings_file()
                    break
                case "2":
                    search_log_file()
                    break
                case _:
                    print("Invalid selection. Please enter 1 or 2.\n")
    except KeyboardInterrupt:
        print("\nexiting without saving")
        print("goodbye!")
        os._exit(1)


def edit_settings_file():
    config = configparser.ConfigParser()
    config.read(SETTINGS_INI)
    display_config(config)
    config_menu(config)


def config_menu(config):
    config_backup = config
    while True:
        try:
            user_input = int(input("1=edit\n2=save and exit\nenter choice: "))
            print()
        except ValueError:
            print("could not parse selection as integer")
            continue
        match user_input:
            case 1:
                edit_config(config)
            case 2:
                save_config_and_exit(config_backup, config)


def edit_config(config):
    section_to_edit = select_section(config)
    key_to_edit = select_key(config, section_to_edit)
    new_value = input("enter new value: ")
    config.set(section_to_edit, key_to_edit, new_value)
    display_config(config)
    config_menu(config)


def select_section(config):
    for section in config.sections():
        print(section)
    section_to_edit = input("select section to edit: ")
    try:
        config[section_to_edit]
    except KeyError:
        print("section not found")
        print()
        select_section(config)
    return section_to_edit


def select_key(config, section_to_edit):
    for key in config[section_to_edit]:
        print(f"{key}={config.get(section_to_edit, key)}")
    key_to_edit = input("select key to edit: ")
    if key_to_edit not in config[section_to_edit]:
        print("key not found")
        select_key(config, section_to_edit)
    return key_to_edit


def save_config_and_exit(config_backup, config):
    print(f"saving to {SETTINGS_INI}...")
    with open(SETTINGS_INI, "w") as configfile:
        config.write(configfile)
    print(f"saving backup to {BACKUP_SETTINGS_INI} ...")
    with open(BACKUP_SETTINGS_INI, "w") as configfile:
        config_backup.write(configfile)
    os._exit(1)


def display_config(config):
    for section in config.sections():
        print(f"[{section}]")
        for key in config[section]:
            print(f"{key}={config.get(section, key)}")
        print()


def search_log_file():
    file_path = input("enter file path to the log to search: ")
    log_pattern = re.compile(r"(?:ERROR|WARNING|\d{1,3}(?:\.\d{1,3}){3})")
    matches = []
    try:
        with open(file_path, "r") as file:
            for _, line in enumerate(file, 1):
                if log_pattern.search(line):
                    matches.append(line)
    except FileNotFoundError:
        print("File not found. Please check the path.")

    print(f"writing matches to {LOG_RESULTS_TXT}")
    with open(LOG_RESULTS_TXT, "w") as file:
        for line in matches:
            file.write(line)


if __name__ == "__main__":
    main()
