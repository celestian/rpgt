from rpgt.core.observer import Observer, Subject


class Character(Subject, Observer):

    def __init__(self):
        super().__init__()
        self.__attributes = {}

    def __apply(self, element):
        def eval_expression(expression, local_vars, allowed_names):
            code = compile(expression, "<string>", "eval")
            for name in code.co_names:
                if name not in allowed_names:
                    raise NameError(f"Use of [{name}] not allowed in character!")

            return eval(code, {"__builtins__": {}}, local_vars)

        local_vars = {}
        local_vars["character"] = self
        local_vars[element["key"]] = element["key"]
        local_vars["value"] = element["value"]

        allowed_names = []
        allowed_names.append("get_attribute")
        allowed_names.append("set_attribute")
        allowed_names.extend(local_vars.keys())

        expression = element["action"]
        expression = expression.replace("$name", element["key"])
        expression = expression.replace("$value", "value")
        eval_expression(expression, local_vars, allowed_names)

    def set_attribute(self, key, value):
        self.__attributes[key] = value

    def get_attribute(self, key):
        return self.__attributes.get(key, None)

    def update(self, payload):
        self.__apply(payload)
        self._update = self.__attributes
        self.notify_observers()
