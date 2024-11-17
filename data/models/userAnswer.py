from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserAnswer:
    quizId: str
    questionId: str
    answerIds: list[str]
    quizTimestamp: float

    @staticmethod
    def fromDict(value: dict):
        return UserAnswer(
            questionId=value.get("id", ""),
            quizId=value.get("quizId", ""),
            answerIds=value.get("answerIds", []),
            quizTimestamp=value.get("quizTimestamp", 0)
        )

    def toDict(self) -> dict:
        return {
            "id": self.questionId,
            "quizId": self.quizId,
            "answerIds": self.answerIds,
            "quizTimestamp": self.quizTimestamp
        }
