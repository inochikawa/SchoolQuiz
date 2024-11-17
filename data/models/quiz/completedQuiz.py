from dataclasses import dataclass
from datetime import datetime


@dataclass
class CompletedQuizQuestion:
    question: str
    maximumPoints: float
    userPoints: float
    correctAnswers: list[str]
    userAnswers: list[str]

    @staticmethod
    def fromDict(value: dict):
        return CompletedQuizQuestion(
            question=value.get("question", ""),
            maximumPoints=value.get("maximumPoints", 0),
            userPoints=value.get("userPoints", 0),
            correctAnswers=value.get("correctAnswers", []),
            userAnswers=value.get("userAnswers", []),
        )

    def toDict(self) -> dict:
        return {
            "question": self.question,
            "maximumPoints": self.maximumPoints,
            "userPoints": self.userPoints,
            "correctAnswers": self.correctAnswers,
            "userAnswers": self.userAnswers,
        }


@dataclass
class CompletedQuiz:
    id: str
    userId: str
    completedDate: datetime
    questions: list[CompletedQuizQuestion]
    mark: int

    @staticmethod
    def fromDict(value: dict):
        return CompletedQuiz(
            id=value.get("id", ""),
            userId=value.get("userId", ""),
            mark=value.get("mark", 0),
            completedDate=datetime.fromisoformat(value.get("completedDate")),
            questions=[CompletedQuizQuestion.fromDict(x) for x in value.get("questions", [])]
        )

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "userId": self.userId,
            "mark": self.mark,
            "completedDate": self.completedDate.isoformat(),
            "questions": [x.toDict() for x in self.questions]
        }
