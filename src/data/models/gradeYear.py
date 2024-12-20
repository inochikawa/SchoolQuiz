from dataclasses import dataclass


@dataclass
class GradeYear:
    code: str
    number: int
    academicYear: int

    @property
    def id(self):
        return f"{self.academicYear}_{self.code}"

    @staticmethod
    def fromDict(value: dict):
        return GradeYear(
            code=value["code"],
            number=value["number"],
            academicYear=int(value["academicYear"]),
        )

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "code": self.code,
            "number": self.number,
            "academicYear": str(self.academicYear),
        }

    def __str__(self):
        return f"GradeYear: {self.id}"
