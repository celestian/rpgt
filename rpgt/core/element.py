from abc import ABC, abstractmethod

from InquirerPy import inquirer
from InquirerPy.base.control import Choice


class RuleSection:

    def __init__(self, data):
        self.id = data["section"]
        self.name = data["section_name"]
        self.__rules = []

    def add_rule(self, rule):
        self.__rules.append(rule)

    def get_rules(self):
        return self.__rules

    def applicable(self, character):
        applicable = False
        for rule in self.__rules:
            applicable += rule.applicable(character)
        return applicable


class ElementABC(ABC):

    def __init__(self, rule):
        self._rule = rule
        self._increment = None

    def applicable(self, character):
        def eval_expression(expression, local_vars, allowed_names):
            code = compile(expression, "<string>", "eval")
            for name in code.co_names:
                if name not in allowed_names:
                    raise NameError(f"Use of [{name}] not allowed in rules!")

            return eval(code, {"__builtins__": {}}, local_vars)

        local_vars = {}
        local_vars["character"] = character
        local_vars[self._rule["rule_name"]] = self._rule["rule_name"]

        allowed_names = []
        allowed_names.append("get_attribute")
        allowed_names.extend(local_vars.keys())

        expression = self._rule["rule"]["condition"]["eval"]
        expression = expression.replace("$name", self._rule["rule"]["property"]["name"])
        return eval_expression(expression, local_vars, allowed_names)

    @abstractmethod
    def prompt(self):
        raise NotImplementedError

    @abstractmethod
    def action(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def increment(self):
        raise NotImplementedError


class TextElement(ElementABC):

    def prompt(self):
        question = self._rule["rule"]["prompt"]["question"]
        self._increment = inquirer.text(message=question).execute()

    def action(self):
        raise NotImplementedError

    @property
    def increment(self):
        if self._increment is None:
            self.prompt()

        increment = {
            "key": self._rule["rule"]["property"]["name"],
            "value": self._increment,
            "type": self._rule["rule"]["property"]["type"],
            "action": self._rule["rule"]["action"]["eval"],
        }
        return increment


class ChoiceElement(ElementABC):

    def __init__(self, rule, db=None):
        super().__init__(rule)
        self.__db = db
        self.__choices = []
        self.__load_choices()

    def __load_choices(self):
        table = self._rule["rule"]["prompt"]["choice_table"]
        rows = self.__db.query(f"SELECT * FROM {table}")
        for row in rows.fetchall():
            self.__choices.append(
                Choice(
                    row["name"], name=f"{row['name']} -- {row['desc']} | p.{row['ref']}"
                )
            )

    def prompt(self):
        question = self._rule["rule"]["prompt"]["question"]
        self._increment = inquirer.select(
            message=question,
            choices=self.__choices,
        ).execute()

    def action(self):
        raise NotImplementedError

    @property
    def increment(self):
        if self._increment is None:
            self.prompt()

        increment = {
            "key": self._rule["rule"]["property"]["name"],
            "value": self._increment,
            "type": self._rule["rule"]["property"]["type"],
            "action": self._rule["rule"]["action"]["eval"],
        }
        return increment
