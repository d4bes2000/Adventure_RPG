class Attack(object):

    def __init__(self, name, power, accuracy, energy_cost):
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.energy_cost = energy_cost
        self.mana_cost = 0

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_power(self):
        """Returns the power multiplier instead of power number"""
        return int(self.power / 10)

