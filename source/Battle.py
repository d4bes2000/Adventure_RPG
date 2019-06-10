import pygame
import Attack as A
import Defend as D
import Spell as S
import random


class Battle(object):

    def __init__(self, hero, enemy):
        self.hero = hero
        self.enemy = enemy
        # Lists of player options
        self.action_dict = {(0, 0): hero.weapon.attack_dict, (1, 0): hero.weapon.defend_dict,
                            (0, 1): hero.spell_dict, (1, 1): hero.item_dict}
        self.current_dict = self.action_dict
        self.previous_dict = None
        self.cursor = [0, 0]
        # Other attributes
        self.action_queue = []
        self.in_combat = True

    def display_battle(self, large_font, small_font, display_width, display_height):
        """
        :param large_font: font
        :param small_font: font
        :param display_width: int
        :param display_height: int
        :return: surface of battle screen
        """
        # Creates temp surface and blits components of battle screen
        temp = pygame.Surface((display_width * (2/3), display_height * (2/3)))
        temp.fill((255, 0, 0))
        temp.blit(self.display_hud(temp, large_font, small_font), (0, 0))
        temp.blit(self.display_info(temp, small_font), (temp.get_width() * (3 / 4), 0))
        temp.blit(self.display_enemy_info(temp, large_font), (0, temp.get_height() * (1/4)))
        temp.blit(self.display_menu(temp, large_font), (0, temp.get_height() * (3/4)))

        # Checks if both hero and enemy have completed turn
        player_action = self.player_turn()
        enemy_action = self.enemy_turn()

        # If hero and enemy have finished turns
        if player_action and enemy_action:
            # Checks to see if hero has escaped
            if isinstance(player_action, D.Defend) and player_action.calculate_damage == "Escape":
                self.end_battle(None)
            # If both hero and enemy are attacking, whoever has higher speed attacks first
            if isinstance(player_action, (A.Attack, S.Spell)) and isinstance(enemy_action, (A.Attack, S.Spell)):
                if self.hero.speed >= self.enemy.speed:
                    self.enemy.health -= player_action.get_power() * self.hero.attack
                    self.check_outcome()
                    self.hero.health -= enemy_action.get_power() * self.enemy.attack
                    self.check_outcome()
                else:
                    self.hero.health -= enemy_action.get_power() * self.enemy.attack
                    self.check_outcome()
                    self.enemy.health -= player_action.get_power() * self.hero.attack
                    self.check_outcome()

            # If hero is attacking and enemy is defending
            elif isinstance(player_action, (A.Attack, S.Spell)) and isinstance(enemy_action, D.Defend):
                damage = enemy_action.calculate_damage(player_action.get_power() * self.hero.attack)
                self.enemy.health -= damage
                self.check_outcome()

            # If hero is defending and enemy is attacking
            elif isinstance(player_action, D.Defend) and isinstance(enemy_action, (A.Attack, S.Spell)):
                damage = player_action.calculate_damage(enemy_action.get_power() * self.enemy.attack)
                self.hero.health -= damage
                self.check_outcome()

            # If both hero and enemy are attacking, nothing happens
            elif isinstance(player_action, D.Defend) and isinstance(enemy_action, D.Defend):
                pass

            # Reset attributes for next turnas
            self.current_dict = self.action_dict
            self.previous_dict = None
            self.cursor = [0, 0]

            # Regen hero energy and mana
            self.hero.energy += self.hero.energy_regen
            self.hero.mana += self.hero.mana_regen
            # Makes sure to not go over max
            if self.hero.energy > self.hero.max_energy:
                self.hero.energy = self.hero.max_energy
            if self.hero.mana > self.hero.max_mana:
                self.hero.mana = self.hero.max_mana

        return temp

    def player_turn(self):
        """
        Allows user to use menus in order to complete turn
        """
        try:
            if self.action_queue[0] == "Up" and self.cursor[1] == 1:
                self.cursor[1] -= 1
            elif self.action_queue[0] == "Down" and self.cursor[1] == 0:
                self.cursor[1] += 1
            elif self.action_queue[0] == "Left" and self.cursor[0] == 1:
                self.cursor[0] -= 1
            elif self.action_queue[0] == "Right" and self.cursor[0] == 0:
                self.cursor[0] += 1
            elif self.action_queue[0] == "Q":
                if self.previous_dict is not None:
                    self.current_dict = self.previous_dict
                    self.previous_dict = None
                    self.cursor = [0, 0]
            elif self.action_queue[0] == "E":
                self.action_queue.remove("E")  # Prevents accidental double clicking
                if self.current_dict == self.action_dict:
                    self.previous_dict = self.current_dict
                    self.current_dict = self.current_dict[tuple(self.cursor)]
                    self.cursor = [0, 0]
                elif self.current_dict == (self.hero.weapon.attack_dict or self.hero.weapon.defend_dict):
                    # Get attack/defend info
                    action = self.current_dict[tuple(self.cursor)]
                    if self.hero.energy - action.energy_cost >= 0:
                        self.hero.energy -= action.energy_cost
                        self.hero.mana -= action.mana_cost
                        return self.current_dict[tuple(self.cursor)]
                    else:
                        pass

        except:
            pass

    def handle_user_input(self, event):
        """
        Adds actions to queue based on key press
        :param event: keypress
        """
        try:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.action_queue.append("Up")
                elif event.key == pygame.K_s:
                    self.action_queue.append("Down")
                elif event.key == pygame.K_a:
                    self.action_queue.append("Left")
                elif event.key == pygame.K_d:
                    self.action_queue.append("Right")
                elif event.key == pygame.K_q:
                    self.action_queue.append("Q")
                elif event.key == pygame.K_e:
                    self.action_queue.append("E")

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.action_queue.remove("Up")
                elif event.key == pygame.K_s:
                    self.action_queue.remove("Down")
                elif event.key == pygame.K_a:
                    self.action_queue.remove("Left")
                elif event.key == pygame.K_d:
                    self.action_queue.remove("Right")
                elif event.key == pygame.K_q:
                    self.action_queue.remove("Q")
                elif event.key == pygame.K_e:
                    self.action_queue.remove("E")
        except:
            pass

    def display_hud(self, surface, large_font, small_font):
        """
        Creates a surface for the battle hud
        :param surface: surface of battle screen
        :param large_font: font created in main()
        :param small_font: font created in main()
        :return: surface of battle hud
        """
        hud = pygame.Surface((surface.get_width() * (3/4), surface.get_height() * (1/4)))
        hud.fill((255, 255, 255))

        # Health Bar
        width = (self.hero.health / self.hero.max_health) * hud.get_width()
        pygame.draw.rect(hud, (0, 255, 0), (0, hud.get_height() * (0/4), width, hud.get_height() * (2/4)))
        string = "Health:  " + str(self.hero.health) + " / " + str(self.hero.max_health)
        self.render_text(string, large_font, hud, 2/4, 0/4, offset=3)  # 3 makes up for blank pixels for chars such as j

        # Energy Bar
        width = (self.hero.energy / self.hero.max_energy) * hud.get_width()
        pygame.draw.rect(hud, (255, 255, 0), (0, hud.get_height() * (2/4), width, hud.get_height() * (1/4)))
        string = "Energy:  " + str(self.hero.energy)
        self.render_text(string, small_font, hud, 1/4, 2/4)

        # Mana Bar
        width = (self.hero.mana / self.hero.max_mana) * hud.get_width()
        pygame.draw.rect(hud, (0, 0, 255), (0, hud.get_height() * (3/4), width, hud.get_height() * (1/4)))
        string = "Mana:  " + str(self.hero.mana)
        self.render_text(string, small_font, hud, 1/4, 3/4)

        return hud

    def display_info(self, surface, font):
        info = pygame.Surface((surface.get_width() * (1/4), surface.get_height() * (1/4)))
        info.fill((0, 0, 0))

        # If player is at the action menu, basic info is displayed
        if self.current_dict == self.action_dict:
            pass
        elif self.current_dict == self.hero.weapon.attack_dict:
            # Power info
            string = "Pwr:  " + str(self.current_dict[tuple(self.cursor)].power)
            self.render_text(string, font, info, 1/4, 0/4, color=(255, 255, 255))

            # Cost info
            string = "Cost:  " + str(self.current_dict[tuple(self.cursor)].energy_cost)
            self.render_text(string, font, info, 1/4, 1/4, color=(255, 255, 255))

            # Accuracy info
            string = "Acc:  " + str(self.current_dict[tuple(self.cursor)].accuracy)
            self.render_text(string, font, info, 1/4, 2/4, color=(255, 255, 255))

        return info

    def display_enemy_info(self, surface, font):
        enemy_info = pygame.Surface((surface.get_width(), surface.get_height() * (2/4)))
        enemy_info.fill((255, 255, 255))

        # Enemy health bar
        width = (self.enemy.health / self.enemy.max_health) * enemy_info.get_width()
        pygame.draw.rect(enemy_info, (255, 0, 0), (0, enemy_info.get_height() * (3/4),
                                                   width, enemy_info.get_height() * (1/4)))
        string = self.enemy.name + ":  " + str(self.enemy.health) + " / " + str(self.enemy.max_health)
        self.render_text(string, font, enemy_info, 1/4, 3/4)

        return enemy_info

    def display_menu(self, surface, font):
        """
        Creates a surface for the battle menu
        :param surface: surface of battle screen
        :param font: font created in main()
        :return: surface of battle menu
        """
        # Creates menu and options
        menu = pygame.Surface((surface.get_width(), surface.get_height() * (1/4)))
        menu.fill((0, 0, 0))
        for key, value in zip(self.current_dict.keys(), self.current_dict.values()):
            try:
                string = value["Text"]
            except:
                if isinstance(value, (A.Attack, D.Defend)):
                    string = value.get_name()

            text = font.render(string, False, (255, 255, 255))

            if isinstance(key, tuple):
                menu.blit(text, (key[0] * (menu.get_width() / 2) + 10, key[1] * (menu.get_height() / 2) + 3))

        # Creates cursor
        cursor = font.render(">", False, (255, 255, 255))
        menu.blit(cursor, (self.cursor[0] * (menu.get_width() / 2) + 3, self.cursor[1] * (menu.get_height() / 2) + 3))

        return menu

    @staticmethod
    def render_text(string, font, surface, surf_frac, surf_loc, color=(0, 0, 0), offset=0):
        text = font.render(string, False, color)
        text_height = font.size(string)[1] - offset
        vertical_offset = (surface.get_height() * surf_frac - text_height) / 2
        surface.blit(text, (3, surface.get_height() * surf_loc + vertical_offset))


    def enemy_turn(self):
        """
        Decides enemy action
        :return: A.Attack or D.Defend instance
        """
        possible_actions = []
        for attack, defend in zip(self.enemy.attack_dict.values(), self.enemy.defend_dict.values()):
            if attack:
                possible_actions.append(attack)
            if defend:
                possible_actions.append(defend)
        num = random.randrange(0, len(possible_actions))

        return possible_actions[num]

    def check_outcome(self):
        """
        Checks if battle is over
        """
        if self.hero.health <= 0:
            outcome = "Defeat"
            self.end_battle(outcome)
        elif self.enemy.health <= 0:
            outcome = "Victory"
            self.end_battle(outcome)

    def end_battle(self, outcome):
        if outcome:  # Hero has either won or lost battle
            if outcome == "Defeat":
                self.in_combat = False
            elif outcome == "Victory":
                self.in_combat = False

        else:  # Hero uses escape
            self.in_combat = False
