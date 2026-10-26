# Phone Book Management System

A complete Python-based phone book application built using Object-Oriented Programming (OOP).

Features:
- Add, delete, and edit contacts
- Search by name, phone number, or email
- Sort contacts alphabetically
- Mark/unmark favorite contacts
- Group contacts by first letter or display favorites
- Manage call history
- Export contacts to CSV and DOCX
- Persistent storage using JSON
- Backup and restore support
- Windows-compatible command-line interface

Project structure:
- `phonebook_app/`
  - `__init__.py`
  - `contact.py`
  - `phonebook.py`
  - `callhistory.py`
  - `backup_manager.py`
  - `main.py`
- `requirements.txt`
- `README.md`

Requirements:
- Python 3.10+
- `python-docx` package

Setup on Windows (VS Code):
1. Open VS Code.
2. Open the project folder.
3. Open a terminal in VS Code.
4. Create a virtual environment:
   `py -m venv .venv`
5. Activate it:
   `.\.venv\Scripts\Activate.ps1`
6. Install dependencies:
   `pip install -r requirements.txt`
7. Run the app:
   `python -m phonebook_app.main`

If PowerShell blocks activation, run this once in the terminal:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

Application menu:
1. Add contact
2. Delete contact
3. Edit contact
4. Sort contacts alphabetically
5. Search contacts
6. Mark/unmark favorites
7. Group contacts by letter / show favorites
8. Add call log
9. View call history
10. Export contacts to CSV
11. Export contacts to DOCX
12. Create backup
13. Restore backup
14. Exit

Data storage:
- `data/contacts.json`
- `data/call_history.json`
- `backups/` for zip backups

This project is designed to run correctly on Windows and can be opened directly in Visual Studio Code.
