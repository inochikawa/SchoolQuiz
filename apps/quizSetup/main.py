from data.services.QuizService import QuizService
from data.models.quiz.Quiz import Quiz
from data.models.quiz.QuizAnswerOption import QuizAnswerOption
from data.models.quiz.QuizQuestion import QuizQuestion
from data.models.quiz.MediaItem import MediaItem
from data.models.quiz.MediaItemType import MediaItemType
import json
import yaml
from uuid import uuid4


def main():
    quizTemplate = createQuizTemplate(totalQuestions=6, defaultNumberOfAnswers=4, classCode="8A")
    print(yaml.dump(quizTemplate, indent=4, sort_keys=False))

    return


def createQuizTemplate(totalQuestions: int, defaultNumberOfAnswers: int, classCode: str) -> dict:
    return Quiz(
        id="",
        classCode=classCode,
        questions=[QuizQuestion(
            id="",
            question="REPLACE",
            hasSingleAnswer=True,
            mediaItems=[MediaItem(type=MediaItemType.Image, path="./file.jpeg")],
            answerOptions=[QuizAnswerOption(id="", text="REPLACE", isCorrect=False)]
        )]
    ).toDict()


if __name__ == "__main__":
    main()
