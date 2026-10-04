"""Heroes of the Inheritance Arena.

Every hero has TWO moves, both fixed by the arena:
  "attack"  - basic attack (always available)
  "special" - special ability (usable again after `special_cooldown` rounds)

You CANNOT change these numbers or moves - the arena uses its own copy and
refuses files that try. Your job: write choose_action() = your STRATEGY.
"""


class Character:
    max_hp = 100
    basic = (6, 10)                          # basic attack damage range
    special_name = "Power Strike"
    special = {"damage": (14, 20)}
    special_cooldown = 3                     # rounds until special is ready again

    def __init__(self, name):
        self.name = name
        self.hp = self.max_hp
        self.round = 0
        self.cooldown = 0                    # rounds until special is ready
        self.special_ready = True

    def choose_action(self, enemy):
        """Return "attack" or "special". Override me!
        enemy has: name, hero_type, hp, max_hp, special_ready, last_action"""
        return "attack"


class Warrior(Character):
    max_hp = 85
    basic = (7, 11)
    special_name = "Shield Bash"             # hits AND blocks half of the enemy damage
    special = {"damage": (9, 13), "block": 0.5}
    special_cooldown = 3


class Mage(Character):
    max_hp = 72
    basic = (5, 9)
    special_name = "Fireball"                # huge damage, long cooldown
    special = {"damage": (30, 40)}
    special_cooldown = 5


class Archer(Character):
    max_hp = 93
    basic = (6, 10)
    special_name = "Double Shot"             # two arrows
    special = {"damage": (8, 12), "hits": 2}
    special_cooldown = 3
