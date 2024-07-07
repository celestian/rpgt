"""rpgt: RPG Toolbox

Usage:
  rpgt [--cfg=<cfg_file>]
  rpgt make_refs cpr <aux_file>
  rpgt prepare [--skills=<skills_file>]
  rpgt (-h | --help)
  rpgt --version

Options:
  --cfg=<cfg_file>  Configuration file [default: ./rpgt.conf].
  --skills=<skills_file>  Skills file [default: ../rpgt_cyberpunk/latex/skills.toml].
  -h --help         Show this screen.
  --version         Show version.
"""

import logging
import sys
from pathlib import Path

from docopt import docopt

from rpgt._version import __version__
from rpgt.core.configuration import Config
from rpgt.core.ui import UI

# from rpgt.core.latex import prepare_skills


def set_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(
        filename=Path("./rpgt.log"), mode="w", encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(levelname)-8s %(lineno)-3d %(module)-20s: %(message)s "
    )
    file_handler.setFormatter(file_formatter)

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(logging.ERROR)
    stream_formatter = logging.Formatter(
        "%(levelname)s: %(message)s {%(module)s:%(lineno)d}"
    )
    stream_handler.setFormatter(stream_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def main():

    args = docopt(__doc__, version=__version__)
    print(f"RPG Tool ({__version__})")

    cfg = Config()
    cfg.initialize(args)

    ui = UI()
    ui.run()

    # if args["prepare"]:
    #     with open(args["--skills"], "rb") as f:
    #         data = tomllib.load(f)
    #         prepare_skills(data)

    sys.exit(0)


if __name__ == "__main__":
    set_logging()
    LOG = logging.getLogger()

    try:
        main()
    except Exception as e:
        LOG.exception("Unexpected exception! %s", e)
