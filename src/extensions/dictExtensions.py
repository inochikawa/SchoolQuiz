def getValueOrDefault(dictionary: dict, valueId: str, defaultValue):
    if valueId in dictionary:
        return dictionary[valueId]

    return defaultValue
