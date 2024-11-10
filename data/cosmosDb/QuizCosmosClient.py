from azure.cosmos import CosmosClient, ContainerProxy
import os
from dataclasses import dataclass
from .QuizContainer import QuizContainer
from .UserAnswersContainer import UserAnswersContainer


@dataclass
class QuizCosmosClient:
    __client = CosmosClient(os.environ['COSMOSDB_ACCOUNT_URI'], credential=os.environ['COSMOSDB_ACCOUNT_KEY'])

    def getQuizContainerClient(self) -> ContainerProxy:
        containerConfigs = QuizContainer()
        return self.__getDatabase().get_container_client(containerConfigs.name)

    def getUserAnswersContainerClient(self) -> ContainerProxy:
        containerConfigs = UserAnswersContainer()
        return self.__getDatabase().get_container_client(containerConfigs.name)

    def __getDatabase(self):
        return self.__client.get_database_client("School289")
