from data.models.quiz.Quiz import Quiz
from data.models.UserAnswer import UserAnswer


class Calculator:

    @staticmethod
    def getQuizMark(quiz: Quiz, userAnswers: dict[str, UserAnswer]) -> float:
        answeredPoints = Calculator.__getQuizAnsweredPoints(quiz, userAnswers)

        maxMark = 12
        quizPoints = 0

        for question in quiz.questions:
            quizPoints = quizPoints + question.points

        return maxMark * answeredPoints / quizPoints

    @staticmethod
    def __getQuizAnsweredPoints(quiz: Quiz, userAnswers: dict[str, UserAnswer]) -> float:
        totalPoints = 0

        for question in quiz.questions:

            if not question.id in userAnswers:
                continue

            userAnswerIds = userAnswers[question.id].answerIds
            correctAnswerIds = [x.id for x in question.answerOptions if x.isCorrect]

            correctlyAnsweredItems = 0

            for userAnswerId in userAnswerIds:
                if userAnswerId in correctAnswerIds:
                    correctlyAnsweredItems = correctlyAnsweredItems + 1

            totalPoints = totalPoints + (question.points * correctlyAnsweredItems / len(correctAnswerIds))

        return totalPoints
