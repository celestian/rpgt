from rpgt.core.character import Character
from rpgt.core.observer import Observer, Subject
from rpgt.core.rules_factory import RulesFactory
from rpgt.core.wizard import Wizard


class CharacterRecordReader(Subject):

    def __init__(self):
        super().__init__()
        self.__data = [
            {"name": "John Doe"},
            {"class": "Warrior"},
            {"level": 5},
            {"experience": 1000},
        ]
        self.__readed = 0

    def read(self):
        if self.__readed < len(self.__data):
            self._update = self.__data[self.__readed]
            self.__readed += 1
            self.notify_observers()
            return True

        return False


class CharacterRecordWriter(Observer):

    def __init__(self, rules_module):
        self.__rules_module = rules_module

    def update(self, payload):
        # Logika pro aktualizaci záznamu postavy
        print(f"CharacterRecordWriter: Postava aktualizována s atributy: {payload}")


class Architect:
    def __init__(self, cfg):
        self.__cfg = cfg
        self.__character = None

    def load_character(self, file_name):

        # todo: tohle je spatne, rules se musi vycist extra
        rules_module = self.__character.get_attribute("rules")
        rules = RulesFactory(rules_module, self.__character)
        reader = CharacterRecordReader()

        reader.register_observer(self.__character)
        self.__character.register_observer(rules)

        print("Architect: Loading a character from the file...")

        while True:
            if not reader.read():
                break

        reader.unregister_observer(self.__character)
        self.__character.unregister_observer(rules)

        del reader
        # print("Architect: Character loaded, entering interactive mode...")

    def build_new(self):

        self.__character = Character()
        wizard = Wizard()
        rules = RulesFactory(wizard.select_rules(self.__cfg))
        writer = CharacterRecordWriter(rules.rules_module)

        wizard.register_observer(writer)
        wizard.register_observer(self.__character)
        self.__character.register_observer(rules)

        while True:
            if not wizard.ask(rules, self.__character):
                break
        print("Architect: End of interactive mode...")

        wizard.unregister_observer(writer)
        wizard.unregister_observer(self.__character)
        self.__character.unregister_observer(rules)

        del writer
