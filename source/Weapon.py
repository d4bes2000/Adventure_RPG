import Item
import Attack as A
import Defend as D


class Weapon(Item.Item):

    def __init__(self, name):
        super().__init__(name)


class Sword(Weapon):

    def __init__(self, name):
        super().__init__(name)
        self.attack_dict = self.create_attack_dict()
        self.defend_dict = self.create_defend_dict()

    @staticmethod
    def create_attack_dict():
        attack_dict = {(0, 0): A.Attack("Stab", 10, 90, 8),
                       (1, 0): A.Attack("Slash", 20, 60, 14),
                       (0, 1): A.Attack("Leaping Strike", 30, 70, 20),
                       (1, 1): A.Attack("Flurry", 40, 80, 30),
                       "Text": "Attack"}

        return attack_dict

    @staticmethod
    def create_defend_dict():
        defend_dict = {(0, 0): D.Damage_Reduce("Block", 50, 5),
                       (1, 0): D.Damage_Cancel("Dodge", 70, 15),
                       (0, 1): D.Damage_Cancel("Parry", 30, 25),
                       (1, 1): D.Damage_Cancel("Escape", 90, 0),
                       "Text": "Defend"}
        return defend_dict


class Greatsword(Weapon):

    def __init__(self, name):
        super().__init__(name)


class Axe(Weapon):

    def __init__(self, name):
        super().__init__(name)


class Hammer(Weapon):

    def __init__(self, name):
        super().__init__(name)


class Bow(Weapon):

    def __init__(self, name):
        super().__init__(name)


class Spear(Weapon):

    def __init__(self, name):
        super().__init__(name)


class Staff(Weapon):

    def __init__(self, name):
        super().__init__(name)


class Daggers(Weapon):

    def __init__(self, name):
        super().__init__(name)


class Wand(Weapon):

    def __init__(self, name):
        super().__init__(name)


class Shield(Weapon):

    def __init__(self, name):
        super().__init__(name)
