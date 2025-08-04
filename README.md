# Acronyms and initialisms aggregator 

[![build](https://github.com/theobori/pycronyms/actions/workflows/build.yml/badge.svg)](https://github.com/theobori/pycronyms/actions/workflows/build.yml)

[![built with nix](https://builtwithnix.org/badge.svg)](https://builtwithnix.org)

This GitHub repository is a fun project, the main purpose of which is to maintain JSON files containing acronyms and initialism. These JSON files are generated using the Python module pycronyms, which exposes a library as well as a CLI.

## Definition

It's important to clarify what an acronym is before reading any further.

An abbreviation is the reduction of a word to a few letters.
An initialism is an abbreviation made up of initial letters.
An Acronym is an acronym pronounced like a word.

## How it works

Acronym generation depends on the acronym providers implemented in the project. At present, the following providers are available.
- [Wikipédia](pycronyms/providers/wikipedia.py)
- [Custom](pycronyms/providers/custom.py)

Each acronym is associated with a language and an associated category. Acronym providers don't have to implement every combination of language and category. They can implement the ones they want.

The library's entry point is the `Pycronyms` class, which manages acronym providers and can retrieve all possible acronyms.

### Acronyms

In the library, acronyms and initialisms are represented by Python objects called `Acronym`. These are [Pydantic](https://docs.pydantic.dev/latest/)data models which normalize the values and check that the acronym conforms. For example, the name of the acronym must match its meaning.

## Logging

Several Python `Logger` objects are used in the module and are disabled by default. Here are their names.

| name | Description |
| - | - |
| `pycronyms.aggregator` | It gives informations about the fetched acronyms in the `Pycronyms` class.  |

The `pycronyms.aggregator` provider could be enabled as shown below. We know that the `disabled` attribute of the `Logger` object is supposed to be read-only, but this is a simple solution for now.

```python
import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger("pycronyms.aggregator")
logger.disabled = False
logger.setLevel(logging.DEBUG)
```

## Usage

### CLI

Once installed, you can run the following command line.

```bash
pycronyms --help
```

Here are a few examples.

```bash
# Generations
pycronyms generate
pycronyms generate --dir output_dir

# Guess game
pycronyms guess --category computer_science --language en
pycronyms guess --category computer_science --language en --name CPU
pycronyms guess --category computer_science --language en --dir custom_generation_dir
```

### Module

If you're looking for examples of how to use the library, you can have a look at the [cli](pycronyms/cli) folder.

## Contribute

If you want to help the project, you can follow the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).

