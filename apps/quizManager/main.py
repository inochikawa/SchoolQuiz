import logging
import os.path
from datetime import datetime, timezone, timedelta

from data.services import QuizService, CompletedQuizService, UserProfileService, GradeYearService
from data.models.quiz import Quiz
from data.models.quiz import QuizAnswerOption
from data.models.quiz import QuizQuestion
from data.models.quiz import MediaItem
from data.models.quiz import MediaItemType
import json
import yaml
from uuid import uuid4
import argparse
import csv
from io import StringIO

from extensions import readFile

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
logger = logging.getLogger("quizManager")


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Setup quiz')

    parser.add_argument("--saveNewQuiz", dest="saveNewQuiz", help="Provide a YAML structure of quiz to save into DB", required=False, action='store_true')
    parser.add_argument("--exportReport", dest="exportReport", help="Exports a CSV report of completed quizzes", required=False, action='store_true')

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
    quizData: list[dict] = yaml.safe_load(content)

    for quiz in quizData:
        quizItem = Quiz.fromDict(quiz)

        quizItem.id = str(uuid4())

        for question in quizItem.questions:
            question.id = str(uuid4())

            if not question.points or question.points == 0:
                question.points = 1

            for answerOption in question.answerOptions:
                answerOption.id = str(uuid4())

        quizService.saveQuiz(quizItem)

    pass


def exportReport():
    service = CompletedQuizService()
    userService = UserProfileService()
    gradeYearService = GradeYearService()
    startDate = datetime.now(tz=timezone.utc).date()
    endDate = startDate + + timedelta(days=1)
    items = service.searchByCompletedDate(startDate, endDate)
    formattedRows = []

    for x in items:
        userProfile = userService.searchById(x.userId)
        gradeYear = gradeYearService.searchById(userProfile.gradeYearId)
        row = {
            "academicYear": gradeYear.academicYear,
            "gradeCode": gradeYear.code,
            "user": userProfile.fullName,
            "topic": x.topic,
            "mark": x.mark,
            "completedDate": x.completedDate.strftime("%Y-%m-%d %H:%M"),
        }
        formattedRows.append(row)

    fileName = "./localOutput/quizzes-report-" + startDate.isoformat() + ".csv"

    logger.info("CSV Report for today in file %s", fileName)

    fileMode = "w" if os.path.isfile(fileName) else "x"

    with open(fileName, fileMode) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["academicYear", "gradeCode", "user", "topic", "mark", "completedDate"])
        writer.writeheader()
        writer.writerows(formattedRows)


def main():
    args = parseArgs()

    if args.saveNewQuiz:
        saveNewQuiz(input("Input path to YAML: "))
        return

    if args.exportReport:
        exportReport()
        return

    return


if __name__ == "__main__":
    main()
