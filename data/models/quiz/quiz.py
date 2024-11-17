from dataclasses import dataclass
from datetime import datetime, timezone

from .quizQuestion import QuizQuestion


@dataclass
class Quiz:
    id: str
    topic: str
    questions: list[QuizQuestion]
    gradeYearId: str
    availableFromDate: datetime | None
    availableToDate: datetime | None

    @property
    def isAvailable(self) -> bool:
        if self.availableFromDate is None and self.availableToDate is None:
            return True

        now = datetime.now(tz=timezone.utc)

        if self.availableFromDate is not None and self.availableToDate is None:
            return self.availableFromDate <= now

        if self.availableFromDate is None and self.availableToDate is not None:
            return self.availableToDate > now

        return self.availableFromDate <= now < self.availableToDate

    @staticmethod
    def fromDict(value: dict):
        availableToDateString = value.get("availableToDate")
        availableFromDateString = value.get("availableFromDate")

        return Quiz(
            id=value.get("id", ""),
            gradeYearId=value.get("gradeYearId", ""),
            topic=value.get("topic", ""),
            questions=list(map(lambda x: QuizQuestion.fromDict(x), value.get("questions", []))),
            availableToDate=datetime.fromisoformat(availableToDateString) if availableToDateString else None,
            availableFromDate=datetime.fromisoformat(availableFromDateString) if availableFromDateString else None
        )

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "gradeYearId": self.gradeYearId,
            "topic": self.topic,
            "questions": list(map(lambda x: x.toDict(), self.questions)),
            "availableToDate": self.availableToDate.isoformat() if self.availableToDate else None,
            "availableFromDate": self.availableFromDate.isoformat() if self.availableFromDate else None,
        }


