from data.cosmosDb import QuizCosmosClient
from data.models import UserProfile


class UserProfileService:
    _cosmosClient: QuizCosmosClient = QuizCosmosClient()

    def save(self, item: UserProfile) -> None:
        container = self._cosmosClient.getUserProfilesContainerClient()
        container.upsert_item(item.toDict())

    def getAll(self) -> list[UserProfile]:
        container = self._cosmosClient.getUserProfilesContainerClient()

        result = []
        items = container.read_all_items()

        for item in items:
            result.append(UserProfile.fromDict(item))

        return result
