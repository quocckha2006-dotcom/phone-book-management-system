from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .contact import Contact


class CallHistory:
    VALID_TYPES = {"incoming", "outgoing", "missed", "rejected"}

    def __init__(self, data_file: str | Path):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.calls: List[dict] = []
        self.load_from_json()

    def log_call(
        self,
        phone: str,
        call_type: str,
        date: Optional[str] = None,
        time: Optional[str] = None,
        duration: int = 0,
    ) -> dict:
        cleaned_phone = Contact.normalize_phone(phone)
        normalized_type = str(call_type).strip().lower()

        if normalized_type not in self.VALID_TYPES:
            raise ValueError(
                "Call type must be one of: incoming, outgoing, missed, rejected."
            )

        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        if time is None:
            time = datetime.now().strftime("%H:%M:%S")

        try:
            duration_value = int(duration)
        except (TypeError, ValueError):
            raise ValueError("Duration must be a valid integer in seconds.")

        if duration_value < 0:
            raise ValueError("Duration cannot be negative.")

        record = {
            "phone": cleaned_phone,
            "call_type": normalized_type,
            "date": date,
            "time": time,
            "duration": duration_value,
        }

        self.calls.append(record)
        self.calls = sorted(
            self.calls,
            key=lambda item: (item["date"], item["time"]),
            reverse=True,
        )
        self.save_to_json()
        return record

    def search(self, query: str) -> List[dict]:
        if not query or not str(query).strip():
            return []

        q = str(query).strip().lower()
        results = []

        for record in self.calls:
            if (
                q in record["phone"].lower()
                or q in record["call_type"].lower()
                or q in record["date"].lower()
                or q in record["time"].lower()
            ):
                results.append(record)

        return results

    def delete_call(self, index: int) -> dict:
        if not 0 <= index < len(self.calls):
            raise IndexError("Call index out of range.")

        removed = self.calls.pop(index)
        self.save_to_json()
        return removed

    def save_to_json(self):
        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump({"calls": self.calls}, file, indent=2, ensure_ascii=False)

    def load_from_json(self):
        if not self.data_file.exists():
            self.calls = []
            return

        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            self.calls = []
            return

        self.calls = data.get("calls", [])
