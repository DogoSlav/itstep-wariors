from base import Mage


class FireWizard(Mage):
    """Mage. Naive strategy: Fireball whenever possible.
    Can you improve it so it beats the Iron Knight?
    (Hint: what does the knight's Shield Bash do, and when does he use it?)"""

    def choose_action(self, enemy):
        if self.special_ready:
            return "special"
        return "attack"
