from data.cosmosDb.QuizCosmosClient import QuizCosmosClient
from data.models.UserAnswer import UserAnswer


class UserAnswersService:
    __cosmosClient: QuizCosmosClient = QuizCosmosClient()

    def saveUserAnswer(self, userAnswer: UserAnswer) -> None:
        container = self.__cosmosClient.getUserAnswersContainerClient()
        container.upsert_item(userAnswer.toJson())

    def getAll(self) -> list[UserAnswer]:
        container = self.__cosmosClient.getUserAnswersContainerClient()

        result = []
        items = container.read_all_items()

        for item in items:
            result.append(UserAnswer.fromJson(item))

        return result
