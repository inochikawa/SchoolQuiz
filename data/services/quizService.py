from data.cosmosDb import QuizCosmosClient
from data.models.quiz import Quiz


class QuizService:
    _cosmosClient: QuizCosmosClient = QuizCosmosClient()

    def saveQuiz(self, quiz: Quiz) -> None:
        container = self._cosmosClient.getQuizContainerClient()
        container.upsert_item(quiz.toDict())

    def getAll(self) -> list[Quiz]:
        container = self._cosmosClient.getQuizContainerClient()

        result = []
        items = container.read_all_items()

        for quizItem in items:
            result.append(Quiz.fromDict(quizItem))

        return result
