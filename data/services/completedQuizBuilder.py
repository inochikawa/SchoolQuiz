from datetime import datetime, timezone

from data.models import UserAnswer
from data.models.quiz import Quiz
from data.models.quiz.completedQuiz import CompletedQuizQuestion, CompletedQuiz
from data.services.calculator import getQuizMark, getQuizQuestionPoints


class CompletedQuizBuilder:
    @staticmethod
    def buildFromQuizAndUserAnswers(quiz: Quiz, userAnswers: list[UserAnswer], userId: str):
        userAnswersDict: dict[str, UserAnswer] = {}

        for userAnswer in userAnswers:
            userAnswersDict[userAnswer.questionId] = userAnswer

        defaultUserAnswer = UserAnswer(answerIds=[], questionId="", quizId="", quizTimestamp=0.0)
        return CompletedQuiz(
            id=quiz.id,
            userId=userId,
            completedDate=datetime.now(tz=timezone.utc),
            mark=getQuizMark(quiz, userAnswers),
            questions=[CompletedQuizQuestion(
                question=question.question,
                maximumPoints=question.points,
                userPoints=getQuizQuestionPoints(question, userAnswers),
                userAnswers=[x.text for x in question.answerOptions if x.id in userAnswersDict.get(question.id, defaultUserAnswer).answerIds],
                correctAnswers=[x.text for x in question.answerOptions if x.isCorrect]
            ) for question in quiz.questions]
        )