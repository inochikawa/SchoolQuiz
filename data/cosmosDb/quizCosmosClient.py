from functools import cache
import logging
from azure.cosmos import CosmosClient, ContainerProxy, PartitionKey
import os

from data.cosmosDb.containers import ContainerBase


class QuizCosmosClient:
    _client = CosmosClient(os.environ['COSMOSDB_ACCOUNT_URI'], credential=os.environ['COSMOSDB_ACCOUNT_KEY'])
    _logger = logging.getLogger("QuizCosmosClient")

    def getContainer(self, name: str) -> ContainerProxy:
        return self._getDatabase().get_container_client(name)

    def _getDatabase(self):
        return self._client.get_database_client("School289")

    def ensureCosmosContainerExists(self, containerConfigs: ContainerBase):
        self._logger.info("Ensure %s CosmosDB container exists", containerConfigs.name)
        self._getDatabase().create_container_if_not_exists(id=containerConfigs.name, partition_key=PartitionKey(containerConfigs.partitionKey))


@cache
def getQuizCosmosClient() -> QuizCosmosClient:
    logging.getLogger("getQuizCosmosClient").info("Creating a new instance of CosmosDB client")
    return QuizCosmosClient()
