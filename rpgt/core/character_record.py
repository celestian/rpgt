from tomlkit import parse


class CharacterRecord:
    def __init__(self, character):
        self.__elements = []
        self.__character = character

    def load(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            data = f.read()
            doc = parse(data)
            self.__elements = doc["elements"]
            self.__character.update(doc["character"])

    def update(self, element_key, element_value):
        element = {"key": element_key, "value": element_value}
        self.__elements.append(element)
        self.__character.update(element)
