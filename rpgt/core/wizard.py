from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from rpgt.core.observer import Subject
from rpgt.core.storage import DataStorage


class Wizard(Subject):

    def select_rules(self):
        storage = DataStorage()
        choices = []
        for rule in storage.get_modules():
            title = f"{rule['name']} (v{rule['version']})"
            choices.append(Choice(value=rule["id"], name=title))

        selected_rules = inquirer.select(
            message="Choose the rules for character creation?",
            choices=choices,
        ).execute()
        return selected_rules

    def ask(self, rules, character):
        sections = rules.get_possible(character)
        for section in sections:
            for element in section.get_elements():
                element.prompt()
                self.notify_observers(element.increment)

        return False
