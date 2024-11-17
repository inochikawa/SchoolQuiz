from datetime import datetime, date

from data.cosmosDb import QuizCosmosClient, CompletedQuizzesContainer
from data.cosmosDb.quizCosmosClient import getQuizCosmosClient
from data.models.quiz.completedQuiz import CompletedQuiz


class CompletedQuizService:
    _cosmosClient: QuizCosmosClient = getQuizCosmosClient()

    def save(self, item: CompletedQuiz) -> None:
        container = self._cosmosClient.getContainer(CompletedQuizzesContainer.name)
        container.upsert_item(item.toDict())

    def searchByUser(self, userId: str) -> list[CompletedQuiz]:
        container = self._cosmosClient.getContainer(CompletedQuizzesContainer.name)

        query = "select * from c where c.userId = @userId"
        items = container.query_items(query=query, enable_cross_partition_query=True, parameters=[
            dict(name="@userId", value=userId)
        ])

        return [CompletedQuiz.fromDict(x) for x in items]

    def searchByCompletedDate(self, searchStartDate: date, searchEndDate: date) -> list[CompletedQuiz]:
        container = self._cosmosClient.getContainer(CompletedQuizzesContainer.name)

        query = "select * from c where c.completedDate >= @searchStartDate and c.completedDate <= @searchEndDate"
        items = container.query_items(query=query, enable_cross_partition_query=True, parameters=[
            dict(name="@searchStartDate", value=searchStartDate.isoformat()),
            dict(name="@searchEndDate", value=searchEndDate.isoformat()),
        ])

        return [CompletedQuiz.fromDict(x) for x in items]

    def getAll(self) -> list[CompletedQuiz]:
        container = self._cosmosClient.getContainer(CompletedQuizzesContainer.name)

        result = []
        items = container.read_all_items()

        for quizItem in items:
            result.append(CompletedQuiz.fromDict(quizItem))

        return result
