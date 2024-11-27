from dataclasses import dataclass


@dataclass
class UserProfileSettings:
    canViewAnswers: bool
    canEditProfile: bool

    @staticmethod
    def fromDict(value: dict):
        return UserProfileSettings(
            canViewAnswers=value["canViewAnswers"],
            canEditProfile=value["canEditProfile"],
        )

    def toDict(self) -> dict:
        return {
            "canViewAnswers": self.canViewAnswers,
            "canEditProfile": self.canEditProfile,
        }


@dataclass
class UserProfile:
    id: str
    firstName: str
    lastName: str
    gradeYearId: str
    userName: str
    settings: UserProfileSettings

    @property
    def fullName(self) -> str:
        return f"{self.firstName} {self.lastName}"

    @staticmethod
    def fromDict(value: dict):
        settings = value.get("")
        return UserProfile(
            id=value["id"],
            firstName=value["firstName"],
            lastName=value["lastName"],
            gradeYearId=value["gradeYearId"],
            userName=value["userName"],
            settings=UserProfileSettings.fromDict(value.get("settings")) if value.get("settings") else UserProfileSettings(canViewAnswers=True, canEditProfile=True)
        )

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "gradeYearId": self.gradeYearId,
            "userName": self.userName,
            "settings": self.settings.toDict()
        }

    def __str__(self):
        return f"UserProfile: {self.fullName}, {self.gradeYearId}"
