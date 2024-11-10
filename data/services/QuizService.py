from data.cosmosDb.QuizCosmosClient import QuizCosmosClient
from data.models.quiz.Quiz import Quiz


class QuizService:
    __cosmosClient: QuizCosmosClient = QuizCosmosClient()

    def saveQuiz(self, quiz: Quiz) -> None:
        container = self.__cosmosClient.getQuizContainerClient()
        container.upsert_item(quiz.toDict())

    def getAll(self) -> list[Quiz]:
        container = self.__cosmosClient.getQuizContainerClient()

        result = []
        items = container.read_all_items()

        for quizItem in items:
            result.append(Quiz.fromDict(quizItem))

        return result
