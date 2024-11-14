from dataclasses import dataclass
from extensions import getValueOrDefault
from .mediaItem import MediaItem
from .quizAnswerOption import QuizAnswerOption


@dataclass
class QuizQuestion:
    id: str
    question: str
    mediaItems: list[MediaItem]
    hasSingleAnswer: bool
    answerOptions: list[QuizAnswerOption]
    points: int

    @staticmethod
    def fromDict(value: dict):
        return QuizQuestion(
            id=getValueOrDefault(value, "id", ""),
            question=getValueOrDefault(value, "question", ""),
            hasSingleAnswer=getValueOrDefault(value, "hasSingleAnswer", True),
            points=getValueOrDefault(value, "points", 0),
            mediaItems=list(map(lambda x: MediaItem.fromDict(x), getValueOrDefault(value, "mediaItems", []))),
            answerOptions=list(map(lambda x: QuizAnswerOption.fromDict(x), getValueOrDefault(value, "answerOptions", []))),
        )

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "question": self.question,
            "hasSingleAnswer": self.hasSingleAnswer,
            "points": self.points,
            "mediaItems": list(map(lambda x: x.toDict(), self.mediaItems)),
            "answerOptions": list(map(lambda x: x.toDict(), self.answerOptions))
        }
