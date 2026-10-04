from base import Warrior, Mage, Archer   # choose your parent class!


class MyHero(Warrior):          # <- change Warrior to Mage or Archer if you want
    """Your hero. Rename the class however you like.

    Your hero's attack and special ability are FIXED by the arena - you cannot
    change them (the arena rejects files that try). What you program is the
    STRATEGY: every round decide which move to use.
    """

    def choose_action(self, enemy):
        # About YOU:
        #   self.hp, self.max_hp, self.round
        #   self.special_ready  -> True when your special can be used
        #   self.cooldown       -> rounds until it is ready
        # About the ENEMY:
        #   enemy.name, enemy.hero_type ("Warrior", "Mage", ...)
        #   enemy.hp, enemy.max_hp
        #   enemy.special_ready, enemy.last_action ("attack"/"special"/"none")
        #
        # Return "attack" or "special".

        if self.special_ready and enemy.hp < 40:
            return "special"
        return "attack"

    # IDEAS:
    # - when is the best moment for your special? Right away, or later?
    # - react to enemy.hero_type or enemy.special_ready
    # - your own helper methods and attributes are allowed (use __init__ + super().__init__(name))
    # - use super().choose_action(enemy) to ask the parent what it would do
