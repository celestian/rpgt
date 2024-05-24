from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from rpgt.core.observer import Subject


class Wizard(Subject):

    def select_rules(self, cfg):
        choices = []
        for rule in cfg.rules:
            choices.append(Choice(value=rule, name=rule["name"]))

        selected_rules = inquirer.select(
            message="By what rules do we build a character?",
            choices=choices,
        ).execute()

        return selected_rules

    def ask(self, rules, character):

        elements = rules.get_possible(character)
        for element in elements:
            for rule in element.get_rules():
                rule.prompt()
                character.update(rule.increment)
                print("Increment: ", rule.increment)

        return False
