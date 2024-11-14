import logging

from apps.quizBot.quizBotClient import QuizBotClient

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main() -> None:
    quizBotClient = QuizBotClient()
    quizBotClient.start()


if __name__ == "__main__":
    main()