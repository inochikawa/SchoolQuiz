from dataclasses import dataclass


@dataclass
class UserAnswer:
    quizId: str
    questionId: str
    answerIds: list[str]

    @staticmethod
    def fromDict(value: dict):
        return UserAnswer(
            quizId=value["quizId"],
            questionId=value["questionId"],
            answerIds=value["answerIds"],
        )

    def toDict(self) -> dict:
        return {
            "quizId": self.quizId,
            "questionId": self.questionId,
            "answerIds": self.answerIds
        }
