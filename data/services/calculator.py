from data.models.quiz.quiz import Quiz
from data.models.quiz.quizQuestion import QuizQuestion
from data.models.userAnswer import UserAnswer


def getQuizMark(quiz: Quiz, userAnswers: list[UserAnswer], maxMarkPoint: int = 12) -> int:
    answeredPoints = getQuizAnsweredPoints(quiz, userAnswers)

    quizPoints = 0

    for question in quiz.questions:
        quizPoints = quizPoints + question.points

    return int(round(maxMarkPoint * answeredPoints / quizPoints, 0))


def getQuizAnsweredPoints(quiz: Quiz, userAnswers: list[UserAnswer]) -> float:
    totalPoints = 0

    for question in quiz.questions:
        totalPoints = totalPoints + getQuizQuestionPoints(question, userAnswers)

    return totalPoints


def getQuizQuestionPoints(question: QuizQuestion, userAnswers: list[UserAnswer]) -> float:
    userAnswersDict: dict[str, UserAnswer] = {}
    for userAnswer in userAnswers:
        userAnswersDict[userAnswer.questionId] = userAnswer

    if not question.id in userAnswersDict:
        return 0

    userAnswerIds = userAnswersDict[question.id].answerIds
    correctAnswerIds = [x.id for x in question.answerOptions if x.isCorrect]

    correctlyAnsweredItems = 0

    for userAnswerId in userAnswerIds:
        if userAnswerId in correctAnswerIds:
            correctlyAnsweredItems = correctlyAnsweredItems + 1

    return question.points * correctlyAnsweredItems / len(correctAnswerIds)
