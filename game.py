"""Game logic: pet management, random events and statistics."""
import random

from tamagotchi import Tamagotchi

PET_NAMES = ["Rachid", "Abou", "Djamal"]
ACTIONS = {"feed", "play", "sleep", "heal"}


def create_pets():
    """Return a dictionary {id: Tamagotchi} with the three pets."""
    return {i + 1: Tamagotchi(name) for i, name in enumerate(PET_NAMES)}


def random_event(pet):
    """30% chance of a random event on a living pet."""
    if not pet.alive or random.random() > 0.30:
        return None
    event = random.choice(["sick", "food", "bonus"])
    if event == "sick":
        pet.change_health(-15)
        return f"{pet.name} got sick! (-15 health)"
    if event == "food":
        pet.change_hunger(-15)
        return f"{pet.name} found some food! (-15 hunger)"
    pet.change_health(10)
    return f"{pet.name} feels great! (+10 health)"


def perform_action(pets, pet_id, action):
    """Apply an action to one pet, then let time pass for all pets."""
    if pet_id not in pets:
        raise KeyError(pet_id)
    if action not in ACTIONS:
        raise ValueError(f"Unknown action: {action}")
    getattr(pets[pet_id], action)()  # may raise DeadPetError

    messages = []
    for pet in pets.values():
        pet.pass_time()
        msg = random_event(pet)
        if msg:
            messages.append(msg)
    return messages


# --- statistics ---
def count_alive_dead(pets):
    alive = sum(p.alive for p in pets.values())
    return alive, len(pets) - alive


def average(values):
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def average_health_alive(pets):
    return average(p.health for p in pets.values() if p.alive)


def average_needs(pets):
    living = [p for p in pets.values() if p.alive]
    return (average(p.hunger for p in living),
            average(p.boredom for p in living),
            average(p.exhaustion for p in living))


def display_statistics(pets):
    alive, dead = count_alive_dead(pets)
    hunger, boredom, exhaustion = average_needs(pets)
    print("=== Game statistics ===")
    print(f"  Living pets: {alive} | Dead pets: {dead}")
    print(f"  Average health (living): {average_health_alive(pets):.1f}")
    print(f"  Average hunger:     {hunger:.1f}")
    print(f"  Average boredom:    {boredom:.1f}")
    print(f"  Average exhaustion: {exhaustion:.1f}")