class QuizContainer:
    name = "quizes"
    partitionKey = "/classCode"


class GradeYearsContainer:
    name = "grade-years"
    partitionKey = "/academicYear"


class UserAnswersContainer:
    name = "user-answers"
    partitionKey = "/quizId"


class UserProfileContainer:
    name = "user-profiles"
    partitionKey = "/yearGradeId"
