"""Save and load the game state as JSON."""
import json

from tamagotchi import Tamagotchi

DEFAULT_FILE = "savegame.json"


def save_game(pets, filename=DEFAULT_FILE):
    data = {str(pid): pet.to_dict() for pid, pet in pets.items()}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_game(filename=DEFAULT_FILE):
    """Raises FileNotFoundError if missing, ValueError if invalid."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        pets = {int(pid): Tamagotchi.from_dict(d) for pid, d in data.items()}
    except json.JSONDecodeError as err:
        raise ValueError("Save file is not valid JSON.") from err
    except (KeyError, TypeError, AttributeError) as err:
        raise ValueError("Save file has missing or invalid data.") from err
    if len(pets) != 3:
        raise ValueError("Save file must contain exactly three pets.")
    return pets