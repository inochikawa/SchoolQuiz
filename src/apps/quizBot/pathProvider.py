import os


def getFileAbsolutePath(path: str) -> str:
    currentPath = os.path.dirname(__file__)
    return os.path.join(currentPath, path)
