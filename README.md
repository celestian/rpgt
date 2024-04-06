# RPG Toolbox (rpgt)

## About the Project

RPG Toolbox (rpgt) is a universal character creation tool for various RPG systems, designed to support a wide range of game rules and systems. Its unique capability to read and interpret user-defined rules allows players and character creators to easily adapt and generate characters for their favorite games. As a terminal application, RPG Toolbox focuses on efficiency and flexibility, while for complex data such as tables, it provides outputs in PDF format, generated using LaTeX.

### Main Features

* **User-Defined Rules**: Import rules for any RPG system in TOML format. The examples how to do that is included.
* **Support for Various Systems**: Flexibility to work with different game systems, from traditional fantasy RPGs to modern and sci-fi.
* **PDF Output**: Clear presentation of character information and rules in a PDF file, generated using LaTeX, for easy sharing and printing.
* **Terminal Interface**: Quick and efficient character creation directly from the command line.
* **Community Modules and Extensions**: Support for sharing user modules, rules, and extensions.

### Technologies

* **Programming Languages**: Python for application logic, LaTeX for formatting output documents.
* **Data and Configuration**: TOML for rule definitions, SQLite3 for data storage.
* **Interface and Utility Tools**: docopt for command-line parsing, InquirerPy for interactive terminal prompts. And behave for testing.

### Who Is RPG Toolbox For?

RPG Toolbox is aimed at a wide range of users, from beginners to experienced players and Dungeon Masters. Thanks to its flexibility and modular nature, it's ideal for those who want to experiment with their own game systems or adapt existing rules.


### How to Contribute

RPG Toolbox welcomes contributions from developers, designers, testers, and content creators. Here are some ways you can support the project:

* **Development and Coding**: Help with developing new features, fixing bugs, or improving performance.
* **Rules and Documentation**: Create or contribute to rule sets, modules, and documentation.
* **Testing**: Test the application across different environments and with various game systems to help ensure stability and compatibility.
* **Suggestions and Feedback**: Provide suggestions for improvements or new features, share your experiences using the tool.


## For Developers

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
