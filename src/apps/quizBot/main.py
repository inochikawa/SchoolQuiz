import os
import sys
from dotenv import load_dotenv

# insert root directory into python module search path
rootPath = os.path.dirname(os.path.realpath(__file__ + "./../../../"))
sys.path.insert(0, rootPath)
load_dotenv()

import logging
from src.apps.quizBot.quizBotClient import QuizBotClient
from src.data.cosmosDb.containers import getContainerConfigs
from src.data.cosmosDb.quizCosmosClient import getQuizCosmosClient

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main() -> None:
    ensureCosmosDbContainersAreExist()
    quizBotClient = QuizBotClient()
    quizBotClient.start()


def ensureCosmosDbContainersAreExist():
    quizCosmosClient = getQuizCosmosClient()

    for conf in getContainerConfigs():
        quizCosmosClient.ensureCosmosContainerExists(conf)


if __name__ == "__main__":
    main()
