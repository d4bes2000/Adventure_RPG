import Attack as A
import Defend as D


class Enemy(object):

    def __init__(self, max_health, mana, energy, attack, magic, speed):
        self.health = max_health
        self.max_health = max_health
        self.mana = mana
        self.energy = energy
        self.attack = attack
        self.magic = magic
        self.speed = speed


class Wolf(Enemy):

    def __init__(self, max_health, mana, energy, attack, magic, speed):
        super().__init__(max_health, mana, energy, attack, magic, speed)
        self.name = "Wolf"
        self.attack_dict = self.create_attack_dict()
        self.defend_dict = self.create_defend_dict()

    @staticmethod
    def create_attack_dict():
        attack_dict = {(0, 0): A.Attack("Bite", 20, 90, 8),
                       (1, 0): A.Attack("Lunge", 40, 60, 14),
                       (0, 1): None,
                       (1, 1): None}

        return attack_dict

    @staticmethod
    def create_defend_dict():
        defend_dict = {(0, 0): D.Damage_Reduce("Stand Ground", 50, 5),
                       (1, 0): D.Damage_Cancel("Evade", 70, 15),
                       (0, 1): None,
                       (1, 1): None}

        return defend_dict
