from dataclasses import dataclass


@dataclass
class UserProfile:
    id: str
    firstName: str
    lastName: str
    gradeYearId: str

    @property
    def fullName(self) -> str:
        return f"{self.firstName} {self.lastName}"

    @staticmethod
    def fromDict(value: dict):
        return UserProfile(
            id=value["id"],
            firstName=value["firstName"],
            lastName=value["lastName"],
            gradeYearId=value["gradeYearId"],
        )

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "gradeYearId": self.gradeYearId,
        }

    def __str__(self):
        return f"UserProfile: {self.fullName}, {self.gradeYearId}"
