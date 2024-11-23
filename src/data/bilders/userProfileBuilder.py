from src.data.models import UserProfile


class UserProfileBuilder:
    _userProfile: UserProfile

    def __init__(self):
        self._userProfile = UserProfile(id="", firstName="", lastName="", gradeYearId="")

    def withFirstName(self, value: str):
        self._userProfile.firstName = value
        return self

    def withLastName(self, value: str):
        self._userProfile.lastName = value
        return self

    def witGradeYearId(self, value: str):
        self._userProfile.gradeYearId = value
        return self

    def build(self) -> UserProfile:
        return self._userProfile
