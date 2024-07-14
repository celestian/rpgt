# RPGT User Manual

## What is rpgt for?

The rpgt app will help you play your favorite role-playing game. Thanks to rpgt, you
can easily create a character, generate a character sheet, and gives you the option to
use rules that you write down yourself. Let's see how rule modules are created.

## Rules Module

A rule module is any directory whose contents must meet several rules.

```
.
├── module
│   ├── build_method
│   │   └── methods.toml
│   ├── build_method.toml
│   ├── init
│   │   ├── age.toml
│   │   ├── name.toml
│   │   ├── role.toml
│   │   └── sex.toml
│   ├── init.toml
│   ├── lifepath
│   │   └── temperament.toml
│   └── lifepath.toml
└── module.toml
```

All files are written in [TOML](https://toml.io/en/) format. Depending on the content,
we can distinguish several types of files:
* module
* section
* element

A key feature of rpgt is that it doesn't try to save character state. Instead, it works
with the character creation record. And it is able to generate a target character sheet
from it. In other words, for the character creation record to make sense, you also need
to know the specific rules module. The advantage of this approach is that we can edit
the character later (as they gains story experience), and still exactly according
to the rules.

### Module

The module serves to hold the entire set of rules.

| key                    | value type | table      | meaning                                             |
| ---                    | ---        | ---        | ---                                                 |
| type                   | string     | meta       | type of TOML file (`module`)                        |
| id                     | string     | meta       | reference name of the module                        |
| name                   | string     | meta       | human name of the module                            |
| version                | integer    | meta       | version of the module                               |
| character_name_element | string     | parameters | variable in which the character name will be stored |

#### Module example

```TOML
[meta]
type = "module"
id = "cpr"
name = "Cyberpunk Red"
version = 1

[parameters]
character_name_elememt = "handle"
```


### Section

Sections help with the organization of individual parts and it is possible to define
their order.

| key                    | value type | table      | meaning                                             |
| ---                    | ---        | ---        | ---                                                 |
| type                   | string     | meta       | type of TOML file (`section`)                       |
| id                     | string     | meta       | reference name of the section                       |
| name                   | string     | meta       | human name of the section                           |
| after (*)              | string     | meta       | applicable after given section                      |
> (*) optional

#### Section example

```TOML
[meta]
type = "section"
id = "build_method"
name = "Build Method"
after = "init"
```

### Element

Elements are key elements, as they define the individual rules that we apply to
the character. We can also define the order for them.

| key                    | value type   | table      | meaning                                             |
| ---                    | ---          | ---        | ---                                                 |
| type                   | string       | meta       | type of TOML file (`element`)                       |
| section_id             | string       | meta       | reference to the section                            |
| key                    | string       | meta       | name (computer readible) of character element       |
| after (*)              | string       | meta       | applicable after given element                      |
| eval                   | string       | condition  | python code of applicable condition                 |
| eval                   | string       | action     | applicable python code on the character             |
| question               | string       | prompt     | question showed to user when asking on the element  |
| type                   | string       | prompt     | type answer (`text`, `select`)                      |
| reference (*)          | integer      | prompt     | page number in the rule book                        |
| count (*, `select`)    | integer      | prompt     | how many answers need to be selected                |
| answers (`select`)     | string array | prompt     | possible answers to the question                    |
> (*) optional
> (`select`) applicable only for type `select`

#### Element example (simple)

```TOML
[meta]
type = "element"
section_id = "build_method"
key = "build_method"
element_type = "string"

[condition]
eval = "character.get_attribute($name) is None"

[prompt]
question = "Choose a method of making a character:"
reference = 40
type = "select"
count = 1
answers = [
    "Streetrats",
    "Edgerunners",
    "Complete Packages"
]

[action]
eval = "character.set_attribute($name, $value)"
```

In some cases we want to set a different page number (`prompt.reference`) for
each answer. In this case, we need to use TOML's array and it looks like this.

| key             | value type | array   | meaning                                  |
| ---             | ---        | ---     | ---                                      |
| answer          | string     | answers | possible answers to the question         |
| description (*) | string     | answers | more details / explanation of the answer |
| reference (*)   | integer    | answers | page number in the rule book             |
> (*) optional

#### Element example (complicated answers)

```TOML
[meta]
type = "element"
section_id = "init"
key = "role"
element_type = "string"
after = "sex"

[condition]
eval = "character.get_attribute($name) is None"

[action]
eval = "character.set_attribute($name, $value)"

[prompt]
question = "Choose a character role:"
type = "select"
count = 1

[[answers]]
answer = "Tech"
description = "Renegade mechanics and supertech inventors; the people who make the Dark Future run."
reference = 33

[[answers]]
answer = "Medtech"
description = "Unsanctioned street doctors and cyberware medics, patching up meat and metal alike."
reference = 34
```

## Macros of Element

In `eval` of `condition` and `action` you can use macros which provides dynamic values
from the element definition or user interaction.

| macro    | meaning                                            |
| ---      | ---                                                |
| `$name`  |  name of element (`key`)                           |
| `$value` |  obtained data from user (type of `element_type`)  |

Also we can used built-in methods on character object.

| method                            | class       | meaning                                       |
| ---                               | ---         | ---                                           |
| `set_attribute(self, key, value)` | `character` | set the `value` to the `key` of `character`   |
| `get_attribute(self, key)`        | `character` | get the `value` from the `key` of `character` |
