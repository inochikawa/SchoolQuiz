from data.cosmosDb import QuizCosmosClient, UserProfileContainer
from data.cosmosDb.quizCosmosClient import getQuizCosmosClient
from data.models import UserProfile
from azure.cosmos.exceptions import CosmosResourceNotFoundError


class UserProfileService:
    _cosmosClient: QuizCosmosClient = getQuizCosmosClient()

    def save(self, item: UserProfile) -> None:
        container = self._cosmosClient.getContainer(UserProfileContainer.name)
        container.upsert_item(item.toDict())

    def get(self, userId: str, gradeYearId: str) -> UserProfile | None:
        container = self._cosmosClient.getContainer(UserProfileContainer.name)

        try:
            item = container.read_item(userId, gradeYearId)
            return UserProfile.fromDict(item)
        except CosmosResourceNotFoundError:
            return None

    def searchById(self, userId: str) -> UserProfile | None:
        container = self._cosmosClient.getContainer(UserProfileContainer.name)

        query = "select * from c where c.id = @userId"
        items = container.query_items(query=query, enable_cross_partition_query=True, parameters=[
            dict(name="@userId", value=userId)
        ])

        for item in items:
            return UserProfile.fromDict(item)

        return None

    def getAll(self) -> list[UserProfile]:
        container = self._cosmosClient.getContainer(UserProfileContainer.name)

        result = []
        items = container.read_all_items()

        for item in items:
            result.append(UserProfile.fromDict(item))

        return result
