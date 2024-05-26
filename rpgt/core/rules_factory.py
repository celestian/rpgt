import json

from rpgt.core.element import RuleSection, SelectElement, TextElement
from rpgt.core.observer import Observer
from rpgt.core.storage import DataStorage


class RulesFactory(Observer):

    def __init__(self, module_id):
        self.__module_id = module_id
        self.__db = DataStorage()
        self.__sections = []
        self.__load_rules()

    def __load_rules(self):
        sections = self.__db.get_sections(self.__module_id)
        for section in sections:
            rule_section = RuleSection(section)
            elements = self.__db.get_elements(section["id"])
            for element in elements:
                if element["prompt_type"] == "text":
                    question = self.__db.get_question(element["id"])
                    rule_element = TextElement(element, question)
                elif element["prompt_type"] == "select":
                    question = self.__db.get_question(element["id"])
                    answers = self.__db.get_answers(question["id"])
                    rule_element = SelectElement(element, question, answers)
                else:
                    raise ValueError(f"Unknown element type: {element['prompt_type']}")
                rule_section.add_element(rule_element)
            self.__sections.append(rule_section)

    def update(self, payload):
        print("RulesFactory updated with attributes: ", payload)

    def get_possible(self, character):
        sections = []
        for section in self.__sections:
            if section.applicable(character):
                sections.append(section)
        return sections
