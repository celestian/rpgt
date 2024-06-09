from rpgt.core.element import RuleSection, SelectElement, TextElement
from rpgt.core.observer import Subject
from rpgt.core.storage import DataStorage


class RulesFactory(Subject):

    def __init__(self, module_id):
        super().__init__()
        self.__module_id = module_id
        self.__db = DataStorage()
        self.__sections = []
        self.__load_rules()

    def __create_element(self, element_data):
        element = None
        if element_data["prompt_type"] == "text":
            question = self.__db.get_question(element_data["id"])
            element = TextElement(element_data, question)
        elif element_data["prompt_type"] == "select":
            question = self.__db.get_question(element_data["id"])
            answers = self.__db.get_answers(question["id"])
            element = SelectElement(element_data, question, answers)
        else:
            raise ValueError(f"Unknown element type: {element_data['prompt_type']}")
        return element

    def __load_rules(self):
        sections = self.__db.get_sections(self.__module_id)
        for section in sections:
            rule_section = RuleSection(section)
            elements = self.__db.get_elements(section["id"])
            for element in elements:
                rule_element = self.__create_element(element)
                rule_section.add_element(rule_element)
            self.__sections.append(rule_section)

    def get_possible(self, character):
        sections = []
        for section in self.__sections:
            if section.applicable(character):
                sections.append(section)
        return sections

    def get_element(self, element_key):
        element_data = self.__db.get_element(element_key)
        return self.__create_element(element_data)

    @property
    def character_name_element(self):
        return self.__db.get_character_name_element(self.__module_id)
