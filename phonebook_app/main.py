from __future__ import annotations

from pathlib import Path

from .backup_manager import BackupManager
from .callhistory import CallHistory
from .contact import Contact
from .phonebook import PhoneBook

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONTACTS_FILE = DATA_DIR / "contacts.json"
CALL_HISTORY_FILE = DATA_DIR / "call_history.json"
BACKUPS_DIR = BASE_DIR / "backups"

DATA_DIR.mkdir(parents=True, exist_ok=True)
BACKUPS_DIR.mkdir(parents=True, exist_ok=True)


def show_menu():
    print("\n" + "=" * 48)
    print("PHONE BOOK MANAGEMENT SYSTEM")
    print("=" * 48)
    print("1. Add contact")
    print("2. Delete contact")
    print("3. Edit contact")
    print("4. Sort contacts alphabetically")
    print("5. Search contacts")
    print("6. Mark / Unmark favorite")
    print("7. Group contacts by letter / Show favorites")
    print("8. Add call log")
    print("9. View call history")
    print("10. Export contacts to CSV")
    print("11. Export contacts to DOCX")
    print("12. Create backup")
    print("13. Restore backup")
    print("14. Exit")
    print("=" * 48)


def prompt_yes_no(message: str) -> bool:
    answer = input(message).strip().lower()
    return answer in {"y", "yes", "1", "true"}


def print_contact(contact: Contact):
    star = "★" if contact.favorite else " "
    print(f"{star} {contact.name} | {contact.phone} | {contact.email} | {contact.notes}")


def add_contact(phonebook: PhoneBook):
    name = input("Enter contact name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email address: ").strip()
    favorite = prompt_yes_no("Mark as favorite? (y/n): ")
    notes = input("Notes (optional): ").strip()

    contact = Contact(name=name, phone=phone, email=email, favorite=favorite, notes=notes)
    phonebook.add_contact(contact)
    print("Contact added successfully.")


def delete_contact(phonebook: PhoneBook):
    query = input("Enter name, phone number, or email to delete: ").strip()
    results = phonebook.search(query)
    if not results:
        raise ValueError("No contact found.")

    for index, contact in enumerate(results, start=1):
        print(f"{index}. {contact.name} - {contact.phone}")

    choice = int(input("Select contact number to delete: ")) - 1
    if choice < 0 or choice >= len(results):
        raise ValueError("Invalid selection.")

    deleted = phonebook.delete_contact(results[choice].name)
    print(f"Deleted contact: {deleted.name}")


def edit_contact(phonebook: PhoneBook):
    query = input("Enter contact name, phone number, or email to edit: ").strip()
    results = phonebook.search(query)

    if not results:
        raise ValueError("No contact found.")

    for index, contact in enumerate(results, start=1):
        print(f"{index}. {contact.name} - {contact.phone}")

    choice = int(input("Select contact number to edit: ")) - 1
    if choice < 0 or choice >= len(results):
        raise ValueError("Invalid selection.")

    selected = results[choice]

    print("Enter new values. Press Enter to keep the current value.")
    new_name = input(f"Name [{selected.name}]: ").strip() or selected.name
    new_phone = input(f"Phone [{selected.phone}]: ").strip() or selected.phone
    new_email = input(f"Email [{selected.email}]: ").strip() or selected.email
    new_notes = input(f"Notes [{selected.notes}]: ").strip() or selected.notes
    new_favorite = input(f"Favorite? (y/n) [{selected.favorite}]: ").strip().lower()

    if new_favorite in {"y", "yes"}:
        favorite_value = True
    elif new_favorite in {"n", "no", ""}:
        favorite_value = selected.favorite
    else:
        raise ValueError("Favorite answer must be y/yes or n/no.")

    updated = phonebook.edit_contact(
        query=selected.name,
        name=new_name,
        phone=new_phone,
        email=new_email,
        notes=new_notes,
        favorite=favorite_value,
    )

    print(f"Updated contact: {updated.name}")


def sort_contacts(phonebook: PhoneBook):
    contacts = phonebook.sort_contacts()
    if not contacts:
        print("No contacts to sort.")
        return

    for contact in contacts:
        print_contact(contact)


def search_contacts(phonebook: PhoneBook):
    query = input("Enter name, phone, or email to search: ").strip()
    results = phonebook.search(query)

    if not results:
        print("No matching contacts found.")
        return

    for contact in results:
        print_contact(contact)


def favorite_toggle(phonebook: PhoneBook):
    query = input("Enter name, phone, or email: ").strip()
    results = phonebook.search(query)

    if not results:
        print("No contact found.")
        return

    target = results[0]
    print(f"Current favorite status for {target.name}: {target.favorite}")

    mark = prompt_yes_no("Mark as favorite? (y/n): ")
    if mark:
        phonebook.mark_favorite(target.name)
        print(f"{target.name} is now a favorite contact.")
    else:
        phonebook.unmark_favorite(target.name)
        print(f"{target.name} was removed from favorites.")


def group_contacts(phonebook: PhoneBook):
    print("1. Group contacts alphabetically")
    print("2. Show favorites")
    choice = input("Select option: ").strip()

    if choice == "1":
        groups = phonebook.group_by_letter()
        if not groups:
            print("No contacts available.")
            return

        for letter in sorted(groups):
            print(f"\n[{letter}]")
            for contact in groups[letter]:
                print_contact(contact)

    elif choice == "2":
        favorites = phonebook.get_favorites()
        if not favorites:
            print("No favorite contacts.")
            return

        for contact in favorites:
            print_contact(contact)
    else:
        print("Invalid option.")


def add_call_log(call_history: CallHistory):
    phone = input("Enter phone number: ").strip()
    call_type = input("Call type (incoming/outgoing/missed/rejected): ").strip().lower()
    duration_text = input("Duration in seconds (optional, press Enter for 0): ").strip() or "0"
    try:
        record = call_history.log_call(phone, call_type, duration=int(duration_text))
    except ValueError as exc:
        raise ValueError(str(exc))
    print("Call recorded successfully.")
    print(record)


def view_call_history(call_history: CallHistory):
    records = call_history.calls
    if not records:
        print("No call history found.")
        return

    for index, record in enumerate(records):
        print(
            f"{index}. {record['date']} {record['time']} | "
            f"{record['call_type']} | {record['phone']} | {record['duration']}s"
        )


def export_contacts(phonebook: PhoneBook):
    print("1. Export to CSV")
    print("2. Export to DOCX")
    action = input("Select export type: ").strip()

    if action == "1":
        default_path = BASE_DIR / "exports" / "contacts.csv"
        user_path = input(f"CSV output path [{default_path}]: ").strip() or str(default_path)
        output = phonebook.export_csv(user_path)
        print(f"Contacts exported to: {output}")
    elif action == "2":
        default_path = BASE_DIR / "exports" / "contacts.docx"
        user_path = input(f"DOCX output path [{default_path}]: ").strip() or str(default_path)
        output = phonebook.export_docx(user_path)
        print(f"Contacts exported to: {output}")
    else:
        print("Invalid export option.")


def create_backup(backup_manager: BackupManager):
    backup_path = backup_manager.create_backup()
    print(f"Backup created: {backup_path}")


def restore_backup(backup_manager: BackupManager):
    path = input("Enter backup file path: ").strip()
    backup_manager.restore_backup(path)
    print("Backup restored successfully.")


def main():
    phonebook = PhoneBook(CONTACTS_FILE)
    call_history = CallHistory(CALL_HISTORY_FILE)
    backup_manager = BackupManager(BACKUPS_DIR, CONTACTS_FILE, CALL_HISTORY_FILE)

    while True:
        show_menu()
        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                add_contact(phonebook)
            elif choice == "2":
                delete_contact(phonebook)
            elif choice == "3":
                edit_contact(phonebook)
            elif choice == "4":
                sort_contacts(phonebook)
            elif choice == "5":
                search_contacts(phonebook)
            elif choice == "6":
                favorite_toggle(phonebook)
            elif choice == "7":
                group_contacts(phonebook)
            elif choice == "8":
                add_call_log(call_history)
            elif choice == "9":
                view_call_history(call_history)
            elif choice == "10":
                export_contacts(phonebook)
            elif choice == "11":
                export_contacts(phonebook)
            elif choice == "12":
                create_backup(backup_manager)
            elif choice == "13":
                restore_backup(backup_manager)
            elif choice == "14":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please choose from the menu.")

        except (ValueError, FileNotFoundError, IndexError, OSError) as exc:
            print(f"Error: {exc}")
        except Exception as exc:
            print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
