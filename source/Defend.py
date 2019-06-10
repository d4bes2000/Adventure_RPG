import random


class Defend(object):

    def __init__(self, name, energy_cost):
        self.name = name
        self.energy_cost = energy_cost
        self.mana_cost = 0

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name


class Damage_Reduce(Defend):

    def __init__(self, name, reduction, energy_cost):
        super().__init__(name, energy_cost)
        self.reduction = reduction

    def calculate_damage(self, damage):
        damage *= (self.reduction / 100)
        return int(damage)


class Damage_Cancel(Defend):

    def __init__(self, name, probability, energy_cost):
        super().__init__(name, energy_cost)
        self.probability = probability

    def calculate_damage(self, damage):
        num = random.randint(0, 99)
        if num < self.probability:
            if self.name == "Escape":
                return "Escape"
            else:
                return 0
        else:
            return damage