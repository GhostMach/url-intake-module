# url-intake-module
Allows a terminal user to input a single URL or a list of URLs from an Excel spreadsheet or text file.

## Installation
Prior to running the script, the following python packages or modules should (already) be installed on the system:
- os
- re
- pandas

Use the following terminal command to install above packages:
```python
python -m pip install package_name
```

## Usage
Import the "url-intake-module" into an existing python (web-scraping) script and then create a constructor function from the module by assigning it to a variable as noted below:
```python
import intake_mod

example_variable = intake_mod.accept_input()
```
**Note:** to enter a file path, please copy and paste full file path into terminal. E.g., in the Windows OS (right-click) context menu, choose "Copy as path". 

## Features
- Accepts .csv, .xlsx, and .txt files.
- Outputs a URL(s) entered as a "list" object.
- Ignores whitespace and duplicate URL entries while validating the syntax of each URL string entered; i.e. if link has "http://" or "https://" prepended, etc.
- If a file path is entered, the script validates the file directory.
- If three unsuccesful attempts are captured in the terminal, the script will exit without outputting a list object.

## Etcetera
Script has been validated to work in Python 3.10
