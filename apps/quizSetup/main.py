from data.services import QuizService
from data.models.quiz import Quiz
from data.models.quiz import QuizAnswerOption
from data.models.quiz import QuizQuestion
from data.models.quiz import MediaItem
from data.models.quiz import MediaItemType
import json
import yaml
from uuid import uuid4
import argparse

from extensions import readFile


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Setup quiz')

    parser.add_argument("--saveNewQuiz", dest="saveNewQuiz", help="Provide a YAML structure of quiz to save into DB", required=False, action='store_true')

    parsedArgs = parser.parse_args()

    return parsedArgs


def createQuizTemplate(totalQuestions: int, defaultNumberOfAnswers: int, classCode: str) -> dict:
    return Quiz(
        id="",
        gradeYearId="",
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
    content = readFile(yamlPath)
    quizData = yaml.safe_load(content)
    quiz = Quiz.fromDict(quizData)

    quiz.id = str(uuid4())
    quiz.gradeYearId = "2024_11А"
    quiz.topic = "Some interesting topic"

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
