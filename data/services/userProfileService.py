from data.cosmosDb import QuizCosmosClient
from data.models import UserProfile
from azure.cosmos.exceptions import CosmosResourceNotFoundError


class UserProfileService:
    _cosmosClient: QuizCosmosClient = QuizCosmosClient()

    def save(self, item: UserProfile) -> None:
        container = self._cosmosClient.getUserProfilesContainerClient()
        container.upsert_item(item.toDict())

    def get(self, userId: str, gradeYearId: str) -> UserProfile | None:
        container = self._cosmosClient.getUserProfilesContainerClient()

        try:
            item = container.read_item(userId, gradeYearId)
            return UserProfile.fromDict(item)
        except CosmosResourceNotFoundError:
            return None

    def searchById(self, userId: str) -> UserProfile | None:
        container = self._cosmosClient.getUserProfilesContainerClient()

        query = "select * from c where c.id = @userId"
        items = container.query_items(query=query, enable_cross_partition_query=True, parameters=[
            dict(name="@userId", value=userId)
        ])

        for item in items:
            return UserProfile.fromDict(item)

        return None

    def getAll(self) -> list[UserProfile]:
        container = self._cosmosClient.getUserProfilesContainerClient()

        result = []
        items = container.read_all_items()

        for item in items:
            result.append(UserProfile.fromDict(item))

        return result
