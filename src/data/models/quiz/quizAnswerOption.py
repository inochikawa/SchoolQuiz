from dataclasses import dataclass
from src.extensions import getValueOrDefault


@dataclass
class QuizAnswerOption:
    id: str
    text: str
    isCorrect: bool

    @staticmethod
    def fromDict(value: dict):
        return QuizAnswerOption(
            id=getValueOrDefault(value, "id", ""),
            text=getValueOrDefault(value, "text", ""),
            isCorrect=getValueOrDefault(value, "isCorrect", False))

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "isCorrect": self.isCorrect
        }
