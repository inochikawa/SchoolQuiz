from data.cosmosDb import QuizCosmosClient
from data.models import UserAnswer


class UserAnswersService:
    _cosmosClient: QuizCosmosClient = QuizCosmosClient()

    def saveUserAnswer(self, userAnswer: UserAnswer) -> None:
        container = self._cosmosClient.getUserAnswersContainerClient()
        container.upsert_item(userAnswer.toJson())

    def getAll(self) -> list[UserAnswer]:
        container = self._cosmosClient.getUserAnswersContainerClient()

        result = []
        items = container.read_all_items()

        for item in items:
            result.append(UserAnswer.fromJson(item))

        return result
