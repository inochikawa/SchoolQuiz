from azure.cosmos import CosmosClient, ContainerProxy
import os
from dataclasses import dataclass

from . import GradeYearsContainer, QuizContainer, UserAnswersContainer, UserProfileContainer


@dataclass
class QuizCosmosClient:
    __client = CosmosClient(os.environ['COSMOSDB_ACCOUNT_URI'], credential=os.environ['COSMOSDB_ACCOUNT_KEY'])

    def getQuizContainerClient(self) -> ContainerProxy:
        return self.__getDatabase().get_container_client(QuizContainer.name)

    def getUserAnswersContainerClient(self) -> ContainerProxy:
        return self.__getDatabase().get_container_client(UserAnswersContainer.name)

    def getGradeYearsContainerClient(self) -> ContainerProxy:
        return self.__getDatabase().get_container_client(GradeYearsContainer.name)

    def getUserProfilesContainerClient(self) -> ContainerProxy:
        return self.__getDatabase().get_container_client(UserProfileContainer.name)

    def __getDatabase(self):
        return self.__client.get_database_client("School289")
