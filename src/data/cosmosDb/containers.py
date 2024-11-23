class ContainerBase:
    name: str
    partitionKey: str
    partitionKeyValue: str | None


class QuizContainer(ContainerBase):
    name = "quizzes"
    partitionKey = "/gradeYearId"


class GradeYearsContainer(ContainerBase):
    name = "grade-years"
    partitionKey = "/academicYear"


class UserProfileContainer(ContainerBase):
    name = "user-profiles"
    partitionKey = "/gradeYearId"


class AcademicYearsContainer(ContainerBase):
    name = "academic-years"
    partitionKey = "/partitionKey"
    partitionKeyValue = "SolePartition"


class CompletedQuizzesContainer(ContainerBase):
    name = "completed-quizzes"
    partitionKey = "/userId"


def getContainerConfigs() -> list[ContainerBase]:
    return [
        QuizContainer(),
        GradeYearsContainer(),
        UserProfileContainer(),
        AcademicYearsContainer(),
        CompletedQuizzesContainer()
    ]
