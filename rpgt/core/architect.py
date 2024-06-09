from rpgt.core.character import Character
from rpgt.core.character_record import CharacterRecordReader, CharacterRecordWriter
from rpgt.core.loader import Loader
from rpgt.core.rules_factory import RulesFactory
from rpgt.core.wizard import Wizard


class Architect:
    def __init__(self):
        self.__character = None

    def load_character(self, file_name):

        self.__character = Character()
        reader = CharacterRecordReader(file_name)
        header = reader.header()
        rules = RulesFactory(header["module_id"])
        loader = Loader(rules, self.__character)

        reader.register_observer(loader)
        loader.register_observer(self.__character)

        print("Architect: Loading a character from the file...")

        reader.read()

        reader.unregister_observer(loader)
        loader.unregister_observer(self.__character)

        print("Architect: Character loaded, entering interactive mode...")

    def build_new(self):

        self.__character = Character()
        wizard = Wizard()
        module_id = wizard.select_rules()
        rules = RulesFactory(module_id)
        writer = CharacterRecordWriter(module_id, rules.character_name_element)

        wizard.register_observer(writer)
        wizard.register_observer(self.__character)

        while True:
            if not wizard.ask(rules, self.__character):
                break
        print("Architect: End of interactive mode...")

        wizard.unregister_observer(writer)
        wizard.unregister_observer(self.__character)
        writer.save()
