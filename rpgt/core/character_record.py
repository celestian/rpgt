import os
import tempfile
import tomllib

from rpgt.core.configuration import Config
from rpgt.core.observer import Observer, Subject


class CharacterRecordWriter(Observer):

    def __init__(self, module_id, character_name_elememt, file_name=None):
        self._file_exists = os.path.exists(file_name) if file_name else False
        self._module_id = module_id
        self._character_name_elememt = character_name_elememt
        self._character_name = None
        self._commits = []
        self._file_name = file_name

    def _create_content(self):
        content = []
        content.append("[meta]")
        content.append("type = 'character'")
        content.append(f"module_id = '{self._module_id}'")
        content.append(f"name = '{self._character_name}'")
        content.append("")
        for commit in self._commits:
            content.append("[[character]]")
            content.append(f'key = "{commit["key"]}"')
            if commit["type"] == "string":
                content.append(f'value = "{commit["value"]}"')
            elif commit["type"] == "integer":
                content.append(f'value = {commit["value"]}')
            content.append("")

        return " \n".join(content)

    def update(self, payload):
        self._commits.append(
            {"key": payload["key"], "value": payload["value"], "type": payload["type"]}
        )
        if payload["key"] == self._character_name_elememt:
            self._character_name = payload["value"]

    def save(self):
        content = self._create_content()
        mode = "a" if self._file_exists else "w"
        if self._file_name is None:
            with tempfile.NamedTemporaryFile(
                mode=mode,
                suffix=".toml",
                prefix="char_",
                dir=Config().char_dir,
                delete=False,
            ) as f:
                f.write(content)
                self._file_name = f.name
        else:
            with open(self._file_name, encoding=mode) as f:
                f.write(content)

        print("> Character was saved to the file:")
        print(f">     {self._file_name}")


class CharacterRecordReader(Subject):

    def __init__(self, file_name):
        super().__init__()
        self.__data = None
        self.__load(file_name)

    def __load(self, file_name):
        with open(file_name, "rb") as f:
            self.__data = tomllib.load(f)
        if self.__data["meta"]["type"] != "character":
            raise ValueError("Not a character record")

    def header(self):
        return self.__data["meta"]

    def read(self):
        for commit in self.__data["character"]:
            self.notify_observers(commit)
