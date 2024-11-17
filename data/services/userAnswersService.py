from data.cosmosDb import QuizCosmosClient, UserAnswersContainer
from data.cosmosDb.quizCosmosClient import getQuizCosmosClient
from data.models import UserAnswer


class UserAnswersService:
    _cosmosClient: QuizCosmosClient = getQuizCosmosClient()

    def saveUserAnswer(self, userAnswer: UserAnswer) -> None:
        container = self._cosmosClient.getContainer(UserAnswersContainer.name)
        container.upsert_item(userAnswer.toDict())

    def getAll(self) -> list[UserAnswer]:
        container = self._cosmosClient.getContainer(UserAnswersContainer.name)

        result = []
        items = container.read_all_items()

        for item in items:
            result.append(UserAnswer.fromDict(item))

        return result
