# Design Document: Character Creation System

## Overview

This document outlines the structure and interactions of objects in a character creation system designed for RPG games. The system allows for the dynamic creation of characters based on a set of rules defined in `.toml` files.

## Components

### Rule
- **Purpose:** Aggregates information about a `Condition`, `Element`, and `Action`.
- **Defined In:** `.toml` files for easy management and extensibility.

### Element
- **Purpose:** Represents a single piece of information necessary for character creation, such as a trait, skill, or attribute.

### Action
- **Purpose:** Describes how an `Element` is applied to a character, detailing the modification process.

### Condition
- **Purpose:** Specifies whether it's possible to apply an `Element` to a character, based on current character state or other rules.

### RulesHandler
- **Purpose:** Checks if a specified directory truly contains a set of rules, validates these rules, and returns a `SetOfRules`.
- **Functions:**
  - Verifies rule directory integrity.
  - Validates rules within the directory.
  - Generates a `SetOfRules` based on validated rules.

### Architect
- **Purpose:** Manages the character creation process.
- **Functions:**
  - Requests `Elements`, `Actions`, and `Conditions` from `SetOfRules`.
  - Commands `CharacterRecord` to read from and write to a file.
  - Instructs the `Wizard` on what to ask the user.
  - Processes updates from the `Wizard`.
  - Oversees the `Character` creation and modification process.

### SetOfRules
- **Purpose:** Maintains knowledge of all rules within a specific game system.
- **Functions:**
  - Responds to `Architect` inquiries about applicable `Elements` for a given character.
  - Applies `Elements` to a character using `Actions` upon `Architect`'s request.
  - Communicates application details to the `Architect`, potentially sourcing information from the `Wizard` or `CharacterRecord`.

### Wizard
- **Purpose:** Interfaces with the user, asking questions and collecting responses.
- **Functions:**
  - Presents a list of `Elements` to inquire about to the user, as directed by the `Architect`.
  - Reports responses back to `CharacterRecord` and `Architect`.

### CharacterRecord
- **Purpose:** Maintains a record of steps taken during character creation.
- **Functions:**
  - Stores elements recorded for creating the character.
  - Saves newly acquired elements into the record, as provided by the `Wizard` or resulting from an `Action`.

### Character
- **Purpose:** Holds detailed information about the character.
- **Functions:**
  - Uses JSON data to populate `jinja2` templates, facilitating the export of character data into a readable format.

## Interaction Flow

1. The `Architect` initiates the character creation process by consulting the `SetOfRules` for initial applicable `Elements`.
2. The `Architect` then instructs the `Wizard` to query the user for choices based on these `Elements`.
3. The `Wizard` collects user responses and communicates these back to both the `CharacterRecord` for storage and the `Architect` for further action.
4. The `Architect` requests the `SetOfRules` to apply selected `Elements` to the `Character` using defined `Actions`, considering `Conditions`.
5. This loop continues until the character creation process is deemed complete by the `Architect`, at which point the final character information is compiled and saved by the `CharacterRecord`.

This system leverages a flexible architecture that allows for extensive customization and expansion of character creation rules, elements, and actions, making it highly adaptable to various RPG systems and settings.