from dataclasses import dataclass


@dataclass
class QuizAnswerOption:
    id: str
    text: str
    isCorrect: bool

    @staticmethod
    def fromDict(value: dict):
        return QuizAnswerOption(id=value["id"], text=value["text"], isCorrect=value["isCorrect"])

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "isCorrect": self.isCorrect
        }
