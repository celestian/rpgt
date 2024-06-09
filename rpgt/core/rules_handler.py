import logging
import tomllib

from rpgt.core.storage import DataStorage


class RulesHandler:

    def __init__(self, dirs):
        self.__db = DataStorage()
        self.__module_id = None

        for directory in dirs:
            self.__scan(directory)
            self.__module_id = None
        self.__db.process()

    def __scan(self, directory):

        def is_valid(data):
            if "meta" not in data:
                return False
            if "type" not in data["meta"]:
                return False
            return True

        logging.info("Scanning directory: %s", directory)
        is_main_directory = False
        dir_content = directory.iterdir()
        for file in [x for x in dir_content if x.is_file() and x.suffix == ".toml"]:
            logging.debug("Scanning file: %s", file)
            with open(file, "rb") as f:
                data = tomllib.load(f)
                if not is_valid(data):
                    continue
                if data["meta"]["type"] == "module":
                    self.__load_module(data)
                    self.__module_id = data["meta"]["id"]
                    is_main_directory = True
                if data["meta"]["type"] == "section":
                    self.__load_section(data)
                if data["meta"]["type"] == "element":
                    self.__load_element(data)

        if is_main_directory:
            self.__scan(directory.joinpath("module"))
        else:
            dir_content = directory.iterdir()
            for subdir in [x for x in dir_content if x.is_dir()]:
                self.__scan(subdir)

    def __load_module(self, data):
        logging.info("Loading module: %s", data["meta"]["name"])
        payload = {
            "id": data["meta"]["id"],
            "name": data["meta"]["name"],
            "version": data["meta"]["version"],
            "character_name_elememt": data["parameters"]["character_name_elememt"],
        }
        self.__db.add_module(payload)

    def __load_section(self, data):
        logging.info("Loading section: %s", data["meta"]["name"])
        payload = {
            "id": data["meta"]["id"],
            "name": data["meta"]["name"],
            "after": None if "after" not in data["meta"] else data["meta"]["after"],
            "module_id": self.__module_id,
        }
        self.__db.add_section(payload)

    def __load_element(self, data):
        logging.info("Loading element: %s", data["meta"]["key"])
        payload = {
            "id": data["meta"]["key"],
            "after": None if "after" not in data["meta"] else data["meta"]["after"],
            "element_type": data["meta"]["element_type"],
            "prompt_type": data["prompt"]["type"],
            "prompt_count": (
                None if "count" not in data["prompt"] else data["prompt"]["count"]
            ),
            "condition": data["condition"]["eval"],
            "action": data["action"]["eval"],
            "section_id": data["meta"]["section_id"],
        }
        self.__db.add_element(payload)

        question = {
            "question": data["prompt"]["question"],
            "element_id": data["meta"]["key"],
            "reference": (
                None
                if "reference" not in data["prompt"]
                else data["prompt"]["reference"]
            ),
        }
        answers = []
        if "answers" in data["prompt"] and "answers" not in data:
            for answer in data["prompt"]["answers"]:
                answers.append(
                    {
                        "answer": answer,
                    }
                )
        elif "answers" not in data["prompt"] and "answers" in data:
            for answer in data["answers"]:
                answers.append(
                    {
                        "answer": answer["answer"],
                        "description": (
                            None
                            if "description" not in answer
                            else answer["description"]
                        ),
                        "reference": (
                            None if "reference" not in answer else answer["reference"]
                        ),
                    }
                )
        elif "answers" in data["prompt"] and "answers" in data:
            print(f"Wrong format of answers in element: {data['meta']['key']}")
        self.__db.add_question_answers(question, answers)
