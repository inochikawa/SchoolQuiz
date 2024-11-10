from dataclasses import dataclass
from .MediaItem import MediaItem
from .QuizAnswerOption import QuizAnswerOption


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
            id=value["id"],
            question=value["question"],
            hasSingleAnswer=value["hasSingleAnswer"],
            points=value["points"],
            mediaItems=list(map(lambda x: MediaItem.fromDict(x), value["mediaItems"])),
            answerOptions=list(map(lambda x: QuizAnswerOption.fromDict(x), value["answerOptions"])),
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
