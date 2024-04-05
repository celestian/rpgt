"""rpgt: RPG Toolbox

Usage:
  rpgt [--cfg=<cfg_file>]
  rpgt make_refs cpr <aux_file>
  rpgt (-h | --help)
  rpgt --version

Options:
  --cfg=<cfg_file>  Configuration file [default: ./rpgt.conf].
  -h --help         Show this screen.
  --version         Show version.
"""

from docopt import docopt

from rpgt._version import __version__
from rpgt.core.configuration import Config


def main():

    args = docopt(__doc__, version=__version__)
    print(f"RPG Tool ({__version__})")
    Config(args)


if __name__ == "__main__":
    main()
