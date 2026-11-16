"""Tamagotchi class: one virtual pet with four status values (0-100)."""


class DeadPetError(Exception):
    """Raised when an action is attempted on a dead pet."""


def clamp(value):
    """Keep a status value between 0 and 100."""
    return max(0, min(100, value))


class Tamagotchi:
    """hunger, boredom, exhaustion: 0 is good, 100 is bad.
    health: 100 is good, 0 means the pet dies."""

    def __init__(self, name, hunger=20, health=100, boredom=20,
                 exhaustion=20, alive=True):
        self.name = name
        self.hunger = hunger
        self.health = health
        self.boredom = boredom
        self.exhaustion = exhaustion
        self.alive = alive

    def _check_alive(self):
        if not self.alive:
            raise DeadPetError(f"{self.name} is dead and cannot do anything.")

    def _check_death(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False

    # --- player actions ---
    def feed(self):
        self._check_alive()
        self.hunger = clamp(self.hunger - 30)

    def play(self):
        self._check_alive()
        self.boredom = clamp(self.boredom - 30)
        self.hunger = clamp(self.hunger + 15)
        self.exhaustion = clamp(self.exhaustion + 15)

    def sleep(self):
        self._check_alive()
        self.exhaustion = clamp(self.exhaustion - 40)
        self.hunger = clamp(self.hunger + 10)

    def heal(self):
        self._check_alive()
        self.health = clamp(self.health + 30)

    # --- time and events ---
    def pass_time(self):
        """Needs grow; each need >= 80 costs 10 health."""
        if not self.alive:
            return
        self.hunger = clamp(self.hunger + 5)
        self.boredom = clamp(self.boredom + 5)
        self.exhaustion = clamp(self.exhaustion + 5)
        critical = sum(v >= 80 for v in
                       (self.hunger, self.boredom, self.exhaustion))
        self.health = clamp(self.health - 10 * critical)
        self._check_death()

    def change_health(self, amount):
        if self.alive:
            self.health = clamp(self.health + amount)
            self._check_death()

    def change_hunger(self, amount):
        if self.alive:
            self.hunger = clamp(self.hunger + amount)

    # --- display / JSON ---
    def display_status(self):
        state = "alive" if self.alive else "DEAD"
        print(f"--- {self.name} ({state}) ---")
        print(f"  Hunger:     {self.hunger}/100")
        print(f"  Health:     {self.health}/100")
        print(f"  Boredom:    {self.boredom}/100")
        print(f"  Exhaustion: {self.exhaustion}/100")

    def to_dict(self):
        return {"name": self.name, "hunger": self.hunger,
                "health": self.health, "boredom": self.boredom,
                "exhaustion": self.exhaustion, "alive": self.alive}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], int(data["hunger"]), int(data["health"]),
                   int(data["boredom"]), int(data["exhaustion"]),
                   bool(data["alive"]))