class QuizContainer:
    name = "quizzes"
    partitionKey = "/gradeYearId"


class GradeYearsContainer:
    name = "grade-years"
    partitionKey = "/academicYear"


class UserAnswersContainer:
    name = "user-answers"
    partitionKey = "/quizId"


class UserProfileContainer:
    name = "user-profiles"
    partitionKey = "/gradeYearId"
