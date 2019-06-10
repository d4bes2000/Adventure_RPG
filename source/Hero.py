import pygame
import Battle
import Weapon
import Enemy
import random


class Hero(object):

    def __init__(self, name, spawn_point):
        # Sprite attributes
        self.hero = pygame.image.load("Sprites/Character_Animations/Walking_Frame1.png")
        # Walking animation images; index 4 is to keep track of next frame
        self.up = ["Sprites/Character_Animations/Walking_Frame9.png",
                   "Sprites/Character_Animations/Walking_Frame10.png",
                   "Sprites/Character_Animations/Walking_Frame11.png",
                   "Sprites/Character_Animations/Walking_Frame12.png",
                   0]
        self.down = ["Sprites/Character_Animations/Walking_Frame1.png",
                     "Sprites/Character_Animations/Walking_Frame2.png",
                     "Sprites/Character_Animations/Walking_Frame3.png",
                     "Sprites/Character_Animations/Walking_Frame4.png",
                     0]
        self.left = ["Sprites/Character_Animations/Walking_Frame13.png",
                     "Sprites/Character_Animations/Walking_Frame14.png",
                     "Sprites/Character_Animations/Walking_Frame15.png",
                     "Sprites/Character_Animations/Walking_Frame16.png",
                     0]
        self.right = ["Sprites/Character_Animations/Walking_Frame5.png",
                      "Sprites/Character_Animations/Walking_Frame6.png",
                      "Sprites/Character_Animations/Walking_Frame7.png",
                      "Sprites/Character_Animations/Walking_Frame8.png",
                      0]
        self.animations = (self.up, self.down, self.left, self.right)
        self.width = 16
        self.height = 24
        self.x_loc = spawn_point[0]
        self.x_change = 0
        self.y_loc = spawn_point[1] - (self.height - self.width)  # Offsets extra sprite height
        self.y_change = 0
        self.action_queue = []
        self.moving = False
        # TODO: Set initial self.direction based on spawn point.
        self.direction = None

        # Hero attributes
        self.name = name
        self.combat_chance = 0
        # Hero battle attributes
        self.level = 1
        self.max_health = 100
        self.health = 100
        self.max_energy = 100
        self.energy = 100
        self.energy_regen = 10
        self.passive_energy_regen = 1
        self.max_mana = 100
        self.mana = 100
        self.mana_regen = 10
        self.passive_mana_regen = 1
        self.attack = 10
        self.magic = 10
        self.speed = 10
        self.weapon = Weapon.Sword("Basic Sword")
        self.spell_dict = {"Text": "Spell"}
        self.item_dict = {"Text": "Item"}

    def handle_user_input(self, event):
        """
        Adds actions to queue based on key press
        :param event: keypress
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.action_queue.append("Up")
            elif event.key == pygame.K_s:
                self.action_queue.append("Down")
            elif event.key == pygame.K_a:
                self.action_queue.append("Left")
            elif event.key == pygame.K_d:
                self.action_queue.append("Right")

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.action_queue.remove("Up")
            elif event.key == pygame.K_s:
                self.action_queue.remove("Down")
            elif event.key == pygame.K_a:
                self.action_queue.remove("Left")
            elif event.key == pygame.K_d:
                self.action_queue.remove("Right")

    def get_info(self, tile_grid):
        """
        Returns hero location tuple and image
        :param tile_grid: Tile_Grid created in Renderer.__init__ when map is first read
        :return: surface containing hero sprite
        :return: tuple (x, y) hero location
        :return: string of map filename
        :return: battle instance
        """
        # Sets index of animation counter based on the length of the first list in self.animations
        animation_counter = len(self.animations[0]) - 1
        # If hero is not at a base animation then self.moving is True and next animation is set.
        for list in self.animations:
            # If hero not at base animation
            if list[animation_counter] != 0:
                list[animation_counter] += 1
                # Checks if list should loop back to base animation
                if list[animation_counter] == 4:
                    list[animation_counter] = 0
                self.hero = pygame.image.load(list[list[animation_counter]])
                self.moving = True
                break
            # If hero is back to base animation
            else:
                self.moving = False

        # If hero is at base animation then next action in queue is executed
        if self.moving is False:
            # Checking the next action in queue for movement
            possible_movements = tile_grid.check_obstacles((self.x_loc, self.y_loc), self.width, self.height)
            self.x_change = 0
            self.y_change = 0
            try:
                ppa = int(self.width / (len(self.animations[0]) - 1))  # Pixels per animation
                if self.action_queue[0] == "Up":
                    if "Up" in possible_movements:
                        self.up[animation_counter] = 1
                        self.hero = pygame.image.load(self.up[self.up[animation_counter]])
                        self.x_change = 0
                        self.y_change = -ppa
                        self.moving = True
                    else:
                        self.hero = pygame.image.load(self.up[self.up[animation_counter]])
                elif self.action_queue[0] == "Down":
                    if "Down" in possible_movements:
                        self.down[animation_counter] = 1
                        self.hero = pygame.image.load(self.down[self.down[animation_counter]])
                        self.x_change = 0
                        self.y_change = ppa
                        self.moving = True
                    else:
                        self.hero = pygame.image.load(self.down[self.down[animation_counter]])
                elif self.action_queue[0] == "Left":
                    if "Left" in possible_movements:
                        self.left[animation_counter] = 1
                        self.hero = pygame.image.load(self.left[self.left[animation_counter]])
                        self.x_change = -ppa
                        self.y_change = 0
                        self.moving = True
                    else:
                        self.hero = pygame.image.load(self.left[self.left[animation_counter]])
                elif self.action_queue[0] == "Right":
                    if "Right" in possible_movements:
                        self.right[animation_counter] = 1
                        self.hero = pygame.image.load(self.right[self.right[animation_counter]])
                        self.x_change = ppa
                        self.y_change = 0
                        self.moving = True
                    else:
                        self.hero = pygame.image.load(self.right[self.right[animation_counter]])
                else:
                    self.x_change = 0
                    self.y_change = 0
                self.direction = self.action_queue[0]
            # If there is no action in queue
            except:
                pass
        # Adjusts location of hero based on movement calculated
        if self.direction == "Up" or self.direction == "Down":
            self.y_loc += self.y_change

        elif self.direction == "Left" or self.direction == "Right":
            self.x_loc += self.x_change

        # If hero is squarely on a tile instead of being in transition
        if (self.x_loc % tile_grid.tile_size == 0 and
            (self.y_loc + self.height - self.width) % tile_grid.tile_size == 0 and
            self.moving is True):  # Hero has just reached new tile
            map, battle = self.check_new_tile(tile_grid)
            # Passive resource regeneration
            self.energy += self.passive_energy_regen
            if self.energy > self.max_energy:
                self.energy = self.max_energy
            self.mana += self.passive_mana_regen
            if self.mana > self.max_mana:
                self.mana = self.max_mana

            return self.hero, (self.x_loc, self.y_loc), map, battle

        return self.hero, (self.x_loc, self.y_loc), None, None

    def check_new_tile(self, tile_grid):
        battle = None
        # Checks new location of hero to see if it is a combat area
        boolean = tile_grid.check_combat_area((self.x_loc, self.y_loc), self.width, self.height)
        if boolean is True:
            number = random.randint(0, 99)
            if number < self.combat_chance:
                battle = Battle.Battle(self, Enemy.Wolf(100, 100, 100, 1, 1, 1))
                self.combat_chance = 0
            else:
                self.combat_chance += 1

        # Checks new location of hero to see if it is a load point
        boolean, tile = tile_grid.check_load_points((self.x_loc, self.y_loc), self.width, self.height)
        # Returns hero sprite, hero_loc, and map_name / None
        if boolean is True:
            self.x_loc = tile.new_loc_x * tile_grid.tile_size
            self.y_loc = (tile.new_loc_y * tile_grid.tile_size) - (self.height - self.width)  # Extra hero height
            return tile.new_map, battle
        else:
            return None, battle
