from dataclasses import dataclass
from datetime import datetime


@dataclass
class AcademicYear:
    year: int
    startDate: datetime
    endDate: datetime

    @property
    def name(self) -> str:
        return f"{self.year} - {self.year + 1}"

    @staticmethod
    def fromDict(value: dict):
        return AcademicYear(
            year=int(value["id"]),
            startDate=datetime.fromisoformat(value["startDate"]),
            endDate=datetime.fromisoformat(value["endDate"]),
        )

    def toDict(self) -> dict:
        return {
            "id": self.year,
            "startDate": self.startDate.isoformat(),
            "endDate": self.endDate.isoformat(),
        }

    def __str__(self):
        return self.name
