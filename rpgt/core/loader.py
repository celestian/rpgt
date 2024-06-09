from rpgt.core.observer import Observer, Subject


class Loader(Subject, Observer):

    def __init__(self, rules, character):
        super().__init__()
        self._rules = rules
        self._character = character

    def update(self, payload):
        print(f"Loader received: {payload}")
        element = self._rules.get_element(payload["key"])
        if not element.applicable(self._character):
            print(f"ERROR: Element [{payload['key']}] is not applicable")
        element.increment = payload["value"]
        self.notify_observers(element.increment)
