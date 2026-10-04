from base import Warrior


class IronKnight(Warrior):
    """Warrior. Strategy: use Shield Bash right when the enemy is about to
    use a big special, because the bash blocks half of the damage."""

    def choose_action(self, enemy):
        if not self.special_ready:
            return "attack"
        # enemy special is ready too -> block it! Otherwise wait a little.
        if enemy.special_ready or enemy.hp < 30:
            return "special"
        return "attack"
