from dataclasses import dataclass
from .QuizQuestion import QuizQuestion


@dataclass
class Quiz:
    id: str
    classCode: str
    questions: list[QuizQuestion]

    @staticmethod
    def fromDict(value: dict):
        return Quiz(
            id=value["id"],
            classCode=value["classCode"],
            questions=list(map(lambda x: QuizQuestion.fromDict(x), value["questions"]))
        )

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "classCode": self.classCode,
            "questions": list(map(lambda x: x.toDict(), self.questions))
        }
