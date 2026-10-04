from base import Mage


class SmartWizard(Mage):
    """Mage. Does not throw Fireball into a Shield Bash: if the enemy Warrior
    has his special ready, the Fireball would be half blocked - so wait."""

    def choose_action(self, enemy):
        if not self.special_ready:
            return "attack"
        if enemy.hero_type == "Warrior" and enemy.special_ready and self.hp > 30:
            return "attack"          # wait one round
        return "special"
