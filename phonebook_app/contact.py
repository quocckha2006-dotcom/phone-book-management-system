from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field


@dataclass
class Contact:
    name: str
    phone: str
    email: str
    favorite: bool = False
    notes: str = ""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def __post_init__(self):
        self.name = self.validate_name(self.name)
        self.phone = self.normalize_phone(self.phone)
        self.email = self.validate_email(self.email)
        self.notes = self.notes.strip() if self.notes else ""
        self.favorite = bool(self.favorite)

    @staticmethod
    def validate_name(name: str) -> str:
        if name is None:
            raise ValueError("Name cannot be empty.")
        cleaned = str(name).strip()
        if not cleaned:
            raise ValueError("Name cannot be empty.")
        if len(cleaned) < 2:
            raise ValueError("Name must be at least 2 characters long.")
        return cleaned

    @staticmethod
    def normalize_phone(phone: str) -> str:
        if phone is None:
            raise ValueError("Phone number cannot be empty.")
        value = str(phone).strip()
        if not value:
            raise ValueError("Phone number cannot be empty.")

        has_plus = value.startswith("+")
        digits = re.sub(r"\D", "", value)

        if len(digits) < 7 or len(digits) > 15:
            raise ValueError("Phone number must contain between 7 and 15 digits.")

        return f"+{digits}" if has_plus else digits

    @staticmethod
    def validate_email(email: str) -> str:
        if email is None:
            raise ValueError("Email cannot be empty.")
        value = str(email).strip()
        if not value:
            raise ValueError("Email cannot be empty.")

        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.fullmatch(pattern, value):
            raise ValueError("Invalid email format.")

        return value.lower()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "favorite": self.favorite,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Contact":
        return cls(
            id=data.get("id", uuid.uuid4().hex[:8]),
            name=data["name"],
            phone=data["phone"],
            email=data["email"],
            favorite=data.get("favorite", False),
            notes=data.get("notes", ""),
        )
