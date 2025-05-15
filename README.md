# STS-Bot
A package that allows an LLM to play slay the spire (sts).

This project is still WIP.

## Remarks:
Any LLM from the Qwen3 family can control sts, but unfortunatly it does not make smart choices (yet).
The reason is that the gamestate representation in the prompt needs to be specialized for the various cases, e.g. combat, map, shop, etc.

## Mod Requirements

- ModTheSpire
- BaseMod
- CommunicationMod

## Setup
- install the mods
- create the conda environment: `conda env create -f conda-recipe.yaml`
- serve an LLM model of your choice with Ollama
- add the model_id and api_base from the served model to `voiceagent/helper/constants.py`
- install the voiceSTS: `pip install -e .`
### CommunicationMod
- adapt `config.properties`:
    - path to python from the conda environment
    - path to `pipe.sh`
    - path to `sts_input` and `sts_output`
- add `config.properties` to the config of the CommunicationMod:
    - On Mac: `~/Library/Preferences/ModTheSpire/CommunicationMod/config.properties`

## Climb the spire
### Let an LLM make decisions:
- `python main.py`
- start Slay the Spire with the mods (debug mode recommended)

### Manually make decisions:
- `python manual_run.py`
- start Slay the Spire with the mods (debug mode recommended)

## Requirements:
- Python 3.11
- ollama
- Qwen model of your choice
