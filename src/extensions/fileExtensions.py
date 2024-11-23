def readFile(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


def writeToFile(path: str, content: str) -> None:
    with open(path, "w") as file:
        file.write(content)
