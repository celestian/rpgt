import configparser
import logging
from pathlib import Path


class Config:

    __cgf_tmpl = [
        "[rpgt]",
        "# Log level (debug, info, warning, error, critical)",
        "log_level = info\n",
        "# Directory where the characters are stored",
        "char_dir = ./characters\n",
        "# Directories where the modules are stored (separated by comma)",
        "mod_dirs = ./modules\n",
    ]

    def __init__(self, args):
        self.__cfg = {}
        self.__cfg_file = Path(args["--cfg"]).resolve()
        self.__parse()
        self.__check()
        self.__setup_logging()

    def __parse(self):
        cfg_parser = configparser.ConfigParser()

        if not self.__cfg_file.exists():
            with open(self.__cfg_file, "w", encoding="utf-8") as f:
                for line in self.__cgf_tmpl:
                    f.write(line + "\n")
            print(f"Configuration file [{self.__cfg_file}] created")
        cfg_parser.read(self.__cfg_file)
        print(f"Configuration [{self.__cfg_file}] loaded")

        for section in cfg_parser.sections():
            self.__cfg[section] = {}
            for key in cfg_parser.options(section):
                self.__cfg[section][key] = cfg_parser.get(section, key)

        self.__cfg["rpgt"]["char_dir"] = Path(self.__cfg["rpgt"]["char_dir"]).resolve()

        mod_dirs = self.__cfg["rpgt"]["mod_dirs"].split(",")
        self.__cfg["rpgt"]["mod_dirs"] = []
        for directory in mod_dirs:
            self.__cfg["rpgt"]["mod_dirs"].append(Path(directory.strip()).resolve())

    def __check(self):
        def create_dir_if_not_exists(directory):
            dir_path = Path(directory)
            if not dir_path.exists():
                dir_path.mkdir()

        for directory in self.mod_dirs:
            create_dir_if_not_exists(directory)
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
            filemode="a",
            encoding="utf-8",
            # format="%(levelname)s %(message)s",
            format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
            level=log_levels[self.__cfg["rpgt"]["log_level"]],
        )

    @property
    def char_dir(self):
        return self.__cfg["rpgt"]["char_dir"]

    @property
    def mod_dirs(self):
        return self.__cfg["rpgt"]["mod_dirs"]
