import tomllib


class RulesHandler:

    def __init__(self, dirs):
        self.__rules = []
        self.__scan_rules(dirs)

    def __scan_rules(self, dirs):
        for wdir in dirs:
            for child in wdir.iterdir():
                if child.is_file() and child.suffix == ".toml":
                    with open(child, "rb") as f:
                        data = tomllib.load(f)
                        if data["meta"]["type"] == "module":
                            module = {
                                "path": child.parent,
                                "name": data["meta"]["name"],
                                "id": data["meta"]["id"],
                                "version": data["meta"]["version"],
                            }
                            self.__rules.append(module)

    @property
    def rules(self):
        return self.__rules
