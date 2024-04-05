# rpgt
RPG Toolbox

## Dev setup

Install Python and necessary programs (tested on Linux Mint 21.3 Virginia)
```
sudo apt install git tig mc
sudo apt install python3.11-full python3-pip nox python3-nox
```

You can use the script to configure `git`
```
# edit the script
vim contrib/git_config.sh

# apply
cp contrib/git_config.sh ./git_config.sh
chmod +x ./git_config.sh
./git_config.sh
rm ./git_config.sh
```

We set up a virtual environment with all libraries using
```
nox -s dev
source .venv/bin/activate

# to run the program
python rpgt

# to format source code
black features/ rpgt/

# to fix imports order
isort features/ rpgt/

# to cancel virtual env
deactivate
```

To run all tests, type
```
nox
```

## Resources
- [conventional commits](https://www.conventionalcommits.org)
- [setuptools](https://setuptools.pypa.io/en/latest/userguide/index.html)
- [nox](https://nox.thea.codes/en/stable/)
- [behave](https://behave.readthedocs.io)
- [docopt](http://docopt.org/)
- [inquirerpy](https://inquirerpy.readthedocs.io/en/latest/index.html)
