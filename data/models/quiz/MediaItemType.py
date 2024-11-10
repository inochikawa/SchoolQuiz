from enum import Enum


class MediaItemType(Enum):
    Image = 1
    Video = 2
    Gif = 3

    def fromDict(self) -> int:
        return self.value
