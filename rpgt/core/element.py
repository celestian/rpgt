from abc import ABC, abstractmethod

from InquirerPy import inquirer
from InquirerPy.base.control import Choice


class RuleSection:

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.__elements = []

    def add_element(self, rule):
        self.__elements.append(rule)

    def get_elements(self):
        return self.__elements

    def applicable(self, character):
        applicable = False
        for element in self.__elements:
            applicable += element.applicable(character)
        return applicable


class ElementABC(ABC):

    def __init__(self, rule, question):
        self._rule = rule
        self._question = question["question"]
        if question["reference"]:
            self._question += f' (p.{question["reference"]})'
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
        local_vars[self._rule["id"]] = self._rule["id"]

        allowed_names = []
        allowed_names.append("get_attribute")
        allowed_names.extend(local_vars.keys())

        expression = self._rule["condition"]
        expression = expression.replace("$name", self._rule["id"])
        return eval_expression(expression, local_vars, allowed_names)

    @abstractmethod
    def prompt(self):
        raise NotImplementedError

    @property
    def increment(self):
        if self._increment is None:
            self.prompt()

        increment = {
            "key": self._rule["id"],
            "value": self._increment,
            "type": self._rule["element_type"],
            "action": self._rule["action"],
        }
        return increment


class TextElement(ElementABC):

    def prompt(self):
        self._increment = inquirer.text(message=self._question).execute()


class SelectElement(ElementABC):

    def __init__(self, rule, question, answers):
        super().__init__(rule, question)
        self.__choices = []

        for answer in answers:
            name = answer["answer"]
            if answer["description"]:
                name += f' :: {answer["description"]}'
            if answer["reference"]:
                name += f' | (p.{answer["reference"]})'
            self.__choices.append(Choice(answer["answer"], name=name))

    def prompt(self):
        self._increment = inquirer.select(
            message=self._question,
            choices=self.__choices,
        ).execute()
