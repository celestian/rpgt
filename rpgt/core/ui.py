import tomllib

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from rpgt.core.architect import Architect
from rpgt.core.configuration import Config


class UI:
    def __init__(self):
        pass

    def _saved_characters(self):

        def is_valid(data):
            if "meta" not in data:
                return False
            if "type" not in data["meta"]:
                return False
            if data["meta"]["type"] != "character":
                return False
            return True

        characters = []
        cfg = Config()
        dir_content = cfg.char_dir.iterdir()
        for file in [x for x in dir_content if x.is_file() and x.suffix == ".toml"]:
            with open(file, "rb") as f:
                try:
                    data = tomllib.load(f)
                except tomllib.TOMLDecodeError:
                    print(f"ERROR: {file} is not a valid TOML file")
                    continue
                if not is_valid(data):
                    continue
                character = Choice(value=file, name=data["meta"]["name"])
                characters.append(character)
        return characters

    def run(self):
        message = "Main menu:"
        print("-" * (len(message) + 2))
        action = inquirer.select(
            message=message,
            choices=[
                Choice(value="new", name="New character"),
                Choice(value="load", name="Load character"),
                Choice(value="quit", name="Quit"),
            ],
            default="new",
        ).execute()

        match action:
            case "new":
                architect = Architect()
                architect.build_new()
                self.run()
            case "load":
                architect = Architect()

                character_file = inquirer.fuzzy(
                    message="Select character:",
                    choices=self._saved_characters(),
                ).execute()
                architect.load_character(character_file)
                self.run()
            case "quit":
                return
            case _:
                print("ERROR: Invalid action")
