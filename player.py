# player.py

from weapons import weapons

class Player:
    def __init__(self, name="Hero"):
        self.name = name
        
        # Base stats
        self.health = 100
        self.stamina = 100
        self.gold = 50
        self.xp = 0
        
        # Inventory can be a list of weapon dictionaries, potions, etc.
        self.inventory = []
        
        # Automatically equip the starter weapon, "Robust Sword", if it exists
        starter_weapon = next((w for w in weapons if w["name"] == "Robust Sword"), None)
        
        # If found, set it as the player's current weapon and add it to inventory
        if starter_weapon:
            self.current_weapon = starter_weapon
            self.inventory.append(starter_weapon)
        else:
            # Fallback if "Robust Sword" wasn't found
            self.current_weapon = None

    def add_item_to_inventory(self, item):
        """
        Add any item (weapon, potion, etc.) to player's inventory.
        """
        self.inventory.append(item)

    def equip_weapon(self, weapon_name):
        """
        Look up a weapon by name in inventory and equip it if found.
        """
        for item in self.inventory:
            if item["name"] == weapon_name:
                self.current_weapon = item
                return f"{item['name']} is now equipped!"
        return f"You do not have {weapon_name} in your inventory."

    def show_inventory(self):
        """
        Returns a string listing all items in inventory by name.
        """
        if not self.inventory:
            return "Your inventory is empty."
        item_names = [i["name"] for i in self.inventory]
        return "Inventory: " + ", ".join(item_names)

    def __str__(self):
        """
        A quick way to inspect the player's main stats and currently equipped weapon.
        """
        weapon_name = self.current_weapon["name"] if self.current_weapon else "None"
        return (
            f"Player: {self.name}\n"
            f"Health: {self.health}\n"
            f"Stamina: {self.stamina}\n"
            f"Gold: {self.gold}\n"
            f"XP: {self.xp}\n"
            f"Current Weapon: {weapon_name}\n"
            f"Inventory: {', '.join(i['name'] for i in self.inventory) or 'Empty'}\n"
        )
