import json
import tomllib

from rpgt.core.element import ChoiceElement, RuleSection, TextElement
from rpgt.core.observer import Observer
from rpgt.core.storage import DataStorage


class RulesFactory(Observer):

    def __init__(self, rules_module):
        self.__rules_module = rules_module

        self.__rules = {}
        self.__load_rules()
        self.__db = DataStorage(self.__rules_module["path"])
        self.__all_elements = self.__create_elements()

        pretty_json = json.dumps(self.__rules, indent=4)
        print(pretty_json)

    def __load_rules(self):
        path = self.__rules_module["path"]
        mod_dir = path.joinpath("module")
        if not mod_dir.is_dir():
            raise FileNotFoundError(f"Module directory not found in {path}")

        for child in mod_dir.iterdir():
            if child.is_file() and child.suffix == ".toml":
                with open(child, "rb") as f:
                    data = tomllib.load(f)
                    self.__parse_rule(data)

    def __parse_rule(self, data):
        section_id = data["meta"]["section_id"]
        if section_id not in self.__rules:
            self.__rules[section_id] = {"name": {}, "rules": {}}

        if data["meta"]["type"] == "section":
            self.__rules[section_id]["name"] = data["meta"]["name"]
            if "after" in data["meta"]:
                self.__rules[section_id]["after"] = data["meta"]["after"]
            else:
                self.__rules[section_id]["after"] = None

        if data["meta"]["type"] == "property":
            name = data["property"]["name"]
            self.__rules[section_id]["rules"][name] = {
                "condition": data["condition"],
                "action": data["action"],
                "prompt": data["prompt"],
                "property": data["property"],
                "choice_table": (
                    None if "choice_table" not in data else data["choice_table"]
                ),
            }

    def update(self, payload):
        print("RulesFactory updated with attributes: ", payload)

    @property
    def rules_module(self):
        return self.__rules_module

    def __create_elements(self):
        rule_sections = []
        for section in self.__rules.keys():
            section_data = {
                "section": section,
                "section_name": self.__rules[section]["name"],
            }
            rule_section = RuleSection(section_data)

            for rule in self.__rules[section]["rules"].keys():
                rule_data = {
                    "rule_section": section,
                    "rule_name": rule,
                    "rule": self.__rules[section]["rules"][rule],
                }
                if rule_data["rule"]["prompt"]["type"] == "text":
                    element = TextElement(rule_data)
                    rule_section.add_rule(element)

                if rule_data["rule"]["prompt"]["type"] == "choice":
                    element = ChoiceElement(rule_data, self.__db)
                    rule_section.add_rule(element)

            rule_sections.append(rule_section)

        return rule_sections

    def get_possible(self, character):
        elements = []
        for element in self.__all_elements:
            if element.applicable(character):
                elements.append(element)
        return elements
