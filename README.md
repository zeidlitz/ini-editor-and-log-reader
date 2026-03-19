# log utility & settings manager

A interactive Python command-line tool designed for managing configuration files and matching pre-defined regular expresions in log files

---

## features

* **Interactive Configuration Editor**: Load, view, and modify `settings.ini` files directly from the terminal.
* **Automatic Backups**: Automatically creates a `.bak` file whenever you save changes to your settings.
* **Smart Log Filtering**: Scans log files using Regular Expressions (Regex) to extract:
    * `ERROR` and `WARNING` flags.
    * IPv4 Addresses (e.g., `192.168.1.1`).
* **Result Export**: Consolidates all filtered log entries into a clean `log_results.txt` file.

---

## requirements

* **Python 3.10+**: This script utilizes the `match/case` structural pattern matching introduced in Python 3.10.
* **Standard Libraries**: No external dependencies (uses `configparser`, `re`, and `os`).

---

## usage

1.  **Run the script**:
    ```bash
    python main.py
    ```
2.  **Select an Action**:
    * **Option 1 (Edit settings.ini)**:
        * The script displays current sections and keys.
        * Follow the prompts to select a section and key to update.
        * Select **Save and Exit** to commit changes and create a backup.
    * **Option 2 (Search log file)**:
        * Provide the full path to a log file.
        * The script will extract critical lines and save them to `log_results.txt`.

---

## file structure

| File | Description |
| :--- | :--- |
| `settings.ini` | The primary configuration file (must exist to use Option 1). |
| `settings.ini.bak` | The backup file created upon saving changes. |
| `log_results.txt` | The output file for filtered log data. |

---

## important Notes

* **Keyboard Interrupt**: You can exit the program at any time using `Ctrl+C`. This will exit without saving any pending changes.
* **File Permissions**: Ensure the script has read/write permissions for the directory it is running in to generate logs and backups.

---

**Developed with Python**
