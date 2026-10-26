from __future__ import annotations

import zipfile
from datetime import datetime
from pathlib import Path
from typing import Union


class BackupManager:
    def __init__(
        self,
        backup_dir: Union[str, Path],
        contacts_file: Union[str, Path],
        call_history_file: Union[str, Path],
    ):
        self.backup_dir = Path(backup_dir)
        self.contacts_file = Path(contacts_file)
        self.call_history_file = Path(call_history_file)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self) -> Path:
        if not self.contacts_file.exists() and not self.call_history_file.exists():
            raise FileNotFoundError("No data files available to back up.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"phonebook_backup_{timestamp}.zip"

        with zipfile.ZipFile(backup_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            if self.contacts_file.exists():
                archive.write(self.contacts_file, arcname=self.contacts_file.name)
            if self.call_history_file.exists():
                archive.write(self.call_history_file, arcname=self.call_history_file.name)

        return backup_path

    def restore_backup(self, backup_path: Union[str, Path]) -> None:
        zip_file = Path(backup_path)

        if not zip_file.exists():
            raise FileNotFoundError(f"Backup file not found: {zip_file}")

        with zipfile.ZipFile(zip_file, "r") as archive:
            for member in archive.namelist():
                if member.endswith("contacts.json"):
                    self.contacts_file.parent.mkdir(parents=True, exist_ok=True)
                    self.contacts_file.write_bytes(archive.read(member))
                elif member.endswith("call_history.json"):
                    self.call_history_file.parent.mkdir(parents=True, exist_ok=True)
                    self.call_history_file.write_bytes(archive.read(member))
