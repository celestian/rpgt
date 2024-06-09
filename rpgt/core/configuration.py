import logging
import sys
import tomllib
from pathlib import Path

from rpgt.core.rules_handler import RulesHandler
from rpgt.core.singleton import Singleton


class Config(metaclass=Singleton):

    def __init__(self):
        self.__cfg = {}
        self.__cfg_file = None

    def initialize(self, args):
        if self.__cfg_file is None:
            self.__cfg_file = Path(args["--cfg"]).resolve()

            self.__parse()
            self.__check()
            self.__setup_logging()
            logging.info("Configuration [%s] loaded", self.__cfg_file)
            RulesHandler(self.__cfg["rpgt"]["mod_dirs"])

    def __parse(self):
        if not self.__cfg_file.exists():
            print(f"Configuration file [{self.__cfg_file}] is missing")
            sys.exit(1)

        with open(self.__cfg_file, "rb") as f:
            self.__cfg = tomllib.load(f)

        self.__cfg["rpgt"]["char_dir"] = Path(self.__cfg["rpgt"]["char_dir"]).resolve()

        self.__cfg["rpgt"]["mod_dirs"] = [
            Path(dir).resolve() for dir in self.__cfg["rpgt"]["mod_dirs"]
        ]

    def __check(self):
        def create_dir_if_not_exists(directory):
            dir_path = Path(directory)
            if not dir_path.exists():
                dir_path.mkdir()

        create_dir_if_not_exists(self.char_dir)

    def __setup_logging(self):

        log_levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }

        logging.basicConfig(
            filename=Path("./rpgt.log"),
            filemode="w",
            encoding="utf-8",
            format="%(levelname)s %(message)s",
            level=log_levels[self.__cfg["rpgt"]["log_level"]],
        )

    @property
    def char_dir(self):
        return self.__cfg["rpgt"]["char_dir"]
