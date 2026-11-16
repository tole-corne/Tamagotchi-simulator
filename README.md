# Tamagotchi-simulator



A command-line Tamagotchi game in Python, built for the EPITA *Introduction to Python Programming* project (2026-2027).

The player takes care of three virtual pets: feed, play, sleep, heal. Random events, statistics and JSON save/load are included.

## Run

Requires Python 3.8+. No external libraries.

```
python main.py
```

## Project structure

| File | Role |
|------|------|
| `main.py` | Interactive menu |
| `tamagotchi.py` | `Tamagotchi` class and `DeadPetError` |
| `game.py` | Pet creation, time evolution, random events, statistics |
| `storage.py` | Save and load the game with JSON |

## Game rules

All values go from 0 to 100. A pet dies when its health reaches 0.

| Action | Effect |
|--------|--------|
| Feed | hunger -30 |
| Play | boredom -30, hunger +15, exhaustion +15 |
| Sleep | exhaustion -40, hunger +10 |
| Heal | health +30 |

**Time:** after each action, every living pet gains +5 hunger, boredom and exhaustion. Each of these at 80 or more costs 10 health.

**Random events** (30% chance per living pet after each action):
- Sick: health -15
- Found food: hunger -15
- Health bonus: health +10

## Menu

1. Select a Tamagotchi
2. Feed / play / sleep / heal the selected pet
3. Display the selected pet's status
4. Display game statistics
5. Save or load a game (`savegame.json`)
6. Quit

## Error handling

Invalid menu options and inputs, nonexistent pets, actions on dead pets, and missing or corrupted save files are all handled without crashing.

## Author

Rachid, EPITA MSc in Artificial Intelligence Systems
