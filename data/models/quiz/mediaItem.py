from dataclasses import dataclass
from . import MediaItemType


@dataclass
class MediaItem:
    path: str
    type: MediaItemType

    @staticmethod
    def fromDict(value: dict):
        return MediaItem(path=value["path"], type=MediaItemType(value["type"]))

    def toDict(self) -> dict:
        return {
            "path": self.path,
            "type": self.type.fromDict()
        }
