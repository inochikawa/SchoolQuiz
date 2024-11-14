from azure.cosmos import CosmosClient, ContainerProxy
import os
from dataclasses import dataclass

from .containers import GradeYearsContainer, QuizContainer, UserAnswersContainer, UserProfileContainer


@dataclass
class QuizCosmosClient:
    _client = CosmosClient(os.environ['COSMOSDB_ACCOUNT_URI'], credential=os.environ['COSMOSDB_ACCOUNT_KEY'])

    def getQuizContainerClient(self) -> ContainerProxy:
        return self._getDatabase().get_container_client(QuizContainer.name)

    def getUserAnswersContainerClient(self) -> ContainerProxy:
        return self._getDatabase().get_container_client(UserAnswersContainer.name)

    def getGradeYearsContainerClient(self) -> ContainerProxy:
        return self._getDatabase().get_container_client(GradeYearsContainer.name)

    def getUserProfilesContainerClient(self) -> ContainerProxy:
        return self._getDatabase().get_container_client(UserProfileContainer.name)

    def _getDatabase(self):
        return self._client.get_database_client("School289")
