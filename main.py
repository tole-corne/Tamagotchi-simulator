"""Entry point: interactive command-line menu."""
import game
import storage
from tamagotchi import DeadPetError

MENU = """
===== TAMAGOTCHI SIMULATOR =====
1. Select a Tamagotchi
2. Care for selected pet (feed / play / sleep / heal)
3. Display selected pet's status
4. Display game statistics
5. Save or load a game
6. Quit
"""

ACTION_MENU = {"1": "feed", "2": "play", "3": "sleep", "4": "heal"}


def ask_int(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Invalid input: please enter a number.")
        return None


def select_pet(pets):
    for pid, pet in pets.items():
        print(f"  {pid}. {pet.name} ({'alive' if pet.alive else 'dead'})")
    pid = ask_int("Pet number: ")
    if pid is None:
        return None
    if pid not in pets:
        print("This pet does not exist.")
        return None
    print(f"Selected: {pets[pid].name}")
    return pid


def care_menu(pets, selected):
    if selected is None:
        print("Select a Tamagotchi first (option 1).")
        return
    print("1. Feed  2. Play  3. Sleep  4. Heal")
    choice = input("Action: ").strip()
    if choice not in ACTION_MENU:
        print("Invalid action.")
        return
    try:
        events = game.perform_action(pets, selected, ACTION_MENU[choice])
    except DeadPetError as err:
        print(err)
        return
    except (KeyError, ValueError):
        print("Invalid pet or action.")
        return
    print(f"Done: {ACTION_MENU[choice]}.")
    for msg in events:
        print("EVENT:", msg)
    pets[selected].display_status()


def save_or_load(pets):
    """Returns the (possibly new) pets dictionary."""
    choice = input("1. Save  2. Load: ").strip()
    if choice == "1":
        try:
            storage.save_game(pets)
            print(f"Game saved to {storage.DEFAULT_FILE}.")
        except OSError as err:
            print("Could not save the game:", err)
    elif choice == "2":
        try:
            pets = storage.load_game()
            print("Game loaded.")
        except FileNotFoundError:
            print("No save file found.")
        except ValueError as err:
            print("Could not load the game:", err)
    else:
        print("Invalid option.")
    return pets


def main():
    pets = game.create_pets()
    selected = None
    while True:
        print(MENU)
        choice = input("Your choice: ").strip()
        if choice == "1":
            selected = select_pet(pets) or selected
        elif choice == "2":
            care_menu(pets, selected)
        elif choice == "3":
            if selected is None:
                print("Select a Tamagotchi first (option 1).")
            else:
                pets[selected].display_status()
        elif choice == "4":
            game.display_statistics(pets)
        elif choice == "5":
            pets = save_or_load(pets)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid menu option.")


if __name__ == "__main__":
    main()