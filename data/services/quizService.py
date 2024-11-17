from data.cosmosDb import QuizCosmosClient, QuizContainer
from data.cosmosDb.quizCosmosClient import getQuizCosmosClient
from data.models.quiz import Quiz


class QuizService:
    _cosmosClient: QuizCosmosClient = getQuizCosmosClient()

    def saveQuiz(self, quiz: Quiz) -> None:
        container = self._cosmosClient.getContainer(QuizContainer.name)
        container.upsert_item(quiz.toDict())

    def searchByGradeYear(self, gradeYearId: str) -> list[Quiz]:
        container = self._cosmosClient.getContainer(QuizContainer.name)

        query = "select * from c where c.gradeYearId = @gradeYearId"
        items = container.query_items(query=query, enable_cross_partition_query=True, parameters=[
            dict(name="@gradeYearId", value=gradeYearId)
        ])

        return [Quiz.fromDict(x) for x in items]

    def searchByGradeYearAndTopic(self, gradeYearId: str, topic: str) -> Quiz | None:
        container = self._cosmosClient.getContainer(QuizContainer.name)

        query = "select * from c where c.gradeYearId = @gradeYearId and c.topic = @topic"
        items = container.query_items(query=query, enable_cross_partition_query=True, parameters=[
            dict(name="@gradeYearId", value=gradeYearId),
            dict(name="@topic", value=topic),
        ])

        for item in items:
            return Quiz.fromDict(item)

        return None

    def getAll(self) -> list[Quiz]:
        container = self._cosmosClient.getContainer(QuizContainer.name)

        result = []
        items = container.read_all_items()

        for quizItem in items:
            result.append(Quiz.fromDict(quizItem))

        return result
