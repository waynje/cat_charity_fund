from sqlalchemy import Column, String, Text

from app.core.db import DonationCharityBase


class CharityProject(DonationCharityBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return f'Фонд {self.name}'