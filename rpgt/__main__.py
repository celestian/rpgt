"""rpgt: RPG Toolbox

Usage:
  rpgt init [--cfg=<cfg_file>]
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

# import tomllib

import sys

from docopt import docopt

from rpgt._version import __version__
from rpgt.core.architect import Architect
from rpgt.core.configuration import Config

# from rpgt.core.latex import prepare_skills


def main():

    args = docopt(__doc__, version=__version__)
    print(f"RPG Tool ({__version__})")
    cfg = Config(args)

    if args["init"]:
        architect = Architect(cfg)
        architect.build_new()

    # if args["prepare"]:
    #     with open(args["--skills"], "rb") as f:
    #         data = tomllib.load(f)
    #         prepare_skills(data)

    sys.exit(0)


if __name__ == "__main__":
    main()
