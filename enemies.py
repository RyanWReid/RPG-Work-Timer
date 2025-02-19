import random

class Enemy:
    def __init__(self, name, hp, attack, dialog, xp_range):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.dialog = dialog
        self.xp_range = xp_range

    def attack_player(self):
        return self.attack

    def speak(self):
        return random.choice(self.dialog)

    def get_xp_drop(self):
        """Return a random amount of XP within the enemy's XP range."""
        return random.randint(self.xp_range[0], self.xp_range[1])

# List of enemies
ENEMIES = [
    # name,   hp, attack, dialog,             xp_range
    Enemy("Goblin",      30,  5,  ["You can't defeat me!", "Give me your gold!", "Hehe, let's fight!"], (5, 10)),
    Enemy("Wolf",        40,  7,  ["*Growls*", "You smell like food.", "You are in my territory now!"], (8, 15)),
    Enemy("Bandit",      50, 10,  ["Hand over your coins!", "You won't escape!", "This is a stick-up!"], (10, 20)),
    Enemy("Slime",       25,  4,  ["*Blorp*", "*Squish*", "Gloop gloop!"], (4, 8)),
    Enemy("Zombie",      60,  8,  ["Brains...", "Urrghhh...", "Join us..."], (12, 18)),
    Enemy("Skeleton",    45,  6,  ["*Rattle rattle*", "Time to be boned!", "I have no flesh, but I have fight!"], (7, 14)),
    Enemy("Orc",         70, 12,  ["You are weak!", "Orcs fear nothing!", "I will smash you!"], (20, 30)),
    Enemy("Giant Rat",   35,  5,  ["Squeak!", "The sewers belong to me!", "You'll regret this!"], (5, 10)),
    Enemy("Dark Mage",   55,  9,  ["Darkness consumes all...", "You dare challenge me?", "Feel my wrath!"], (15, 25)),
    Enemy("Fire Elemental", 65, 11, ["Burn!", "You can't escape the flames!", "You will turn to ashes!"], (18, 28))
]

def get_random_enemy():
    return random.choice(ENEMIES)
