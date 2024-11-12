from dataclasses import dataclass

from extensions import getValueOrDefault
from . import QuizQuestion


@dataclass
class Quiz:
    id: str
    topic: str
    questions: list[QuizQuestion]
    gradeYearId: str

    @staticmethod
    def fromDict(value: dict):
        return Quiz(
            id=getValueOrDefault(value, "id", ""),
            gradeYearId=getValueOrDefault(value, "gradeYearId", ""),
            topic=getValueOrDefault(value, "topic", ""),
            questions=list(map(lambda x: QuizQuestion.fromDict(x), getValueOrDefault(value, "questions", [])))
        )

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "gradeYearId": self.gradeYearId,
            "topic": self.topic,
            "questions": list(map(lambda x: x.toDict(), self.questions))
        }
