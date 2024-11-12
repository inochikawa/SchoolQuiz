from data.services.QuizService import QuizService
from data.models.quiz.Quiz import Quiz
from data.models.quiz.QuizAnswerOption import QuizAnswerOption
from data.models.quiz.QuizQuestion import QuizQuestion
from data.models.quiz.MediaItem import MediaItem
from data.models.quiz.MediaItemType import MediaItemType
import json
import yaml
from uuid import uuid4
import argparse

from extensions import FileExtensions


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Setup quiz')

    parser.add_argument("--saveNewQuiz", dest="saveNewQuiz", help="Provide a YAML structure of quiz to save into DB", required=False, action='store_true')

    parsedArgs = parser.parse_args()

    return parsedArgs


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


def saveNewQuiz(yamlPath: str) -> None:
    quizService = QuizService()
    content = FileExtensions.readFile(yamlPath)
    quizData = yaml.safe_load(content)
    quiz = Quiz.fromDict(quizData)

    quiz.id = str(uuid4())

    for question in quiz.questions:
        question.id = str(uuid4())
        for answerOption in question.answerOptions:
            answerOption.id = str(uuid4())

    quizService.saveQuiz(quiz)
    pass


def main():
    args = parseArgs()

    if args.saveNewQuiz:
        saveNewQuiz(input("Input path to YAML: "))
        return

    return


if __name__ == "__main__":
    main()
