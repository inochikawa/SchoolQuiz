charactersToEscape = ["_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"]


def escapeCharacters(text: str) -> str:
    for c in charactersToEscape:
        text = text.replace(c, "\\" + c)

    print(text)
    return text
