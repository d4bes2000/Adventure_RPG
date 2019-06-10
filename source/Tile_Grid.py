import pytmx
import Tile


class Tile_Grid(object):

    def __init__(self, tilemap):
        self.tile_size = tilemap.tilewidth
        # Creates dict; key: (x, y); value: Tile instance
        self.tile_dict = {}
        for x in range(tilemap.width):
            for y in range(tilemap.height):
                self.tile_dict[(x, y)] = Tile.Tile(x, y)

        # Iterates through all visible layers in tilemap
        for layer in tilemap.visible_layers:
            # All layers that contain obstacles, spawn points, and exits are object layers
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "Obstacles":
                    for obstacle in layer:
                        # Converts obstacle measurements from pixels to tiles
                        obstacle.x /= self.tile_size
                        obstacle.y /= self.tile_size
                        obstacle.width /= self.tile_size
                        obstacle.height /= self.tile_size

                        # Iterates through each tile in the obstacle and sets Tile.obstacle to True
                        for x in range(int(obstacle.width)):
                            for y in range(int(obstacle.height)):
                                self.tile_dict[(int(obstacle.x + x), int(obstacle.y + y))].set_obstacle(True)

                elif layer.name == "Load Points":
                    for obstacle in layer:
                        # Converts obstacle measurements from pixels to tiles
                        obstacle.x /= self.tile_size
                        obstacle.y /= self.tile_size

                        # Gets data from load point and inputs it to corresponding tile
                        new_map = str(obstacle.new_map)
                        new_loc_x = int(obstacle.new_loc_x)
                        new_loc_y = int(obstacle.new_loc_y)
                        self.tile_dict[(int(obstacle.x), int(obstacle.y))].set_load_point(new_map, new_loc_x, new_loc_y)

                elif layer.name == "Combat Areas":
                    for obstacle in layer:
                        # Converts obstacle measurements from pixels to tiles
                        obstacle.x /= self.tile_size
                        obstacle.y /= self.tile_size
                        obstacle.width /= self.tile_size
                        obstacle.height /= self.tile_size

                        # Iterates through each tile in the obstacle and sets Tile.obstacle to True
                        for x in range(int(obstacle.width)):
                            for y in range(int(obstacle.height)):
                                self.tile_dict[(int(obstacle.x + x), int(obstacle.y + y))].set_combat_area(True)

                else:
                    pass

            # Tile layers are handled in the renderer and are not needed for the tile grid
            else:
                pass

    def check_obstacles(self, hero_loc, hero_width, hero_height):
        """
        Checks surrounding tiles for available movements
        :param hero_loc: tuple (x, y) in pixels, not tiles
        :param hero_width: int
        :param hero_height: int
        :return: list of possible movements
        """
        possible_movements = []

        # Converts hero_loc from pixels to tiles
        hero_x = int(hero_loc[0] / 16)
        hero_y = int((hero_loc[1] + (hero_height - hero_width)) / 16)  # Makes up for the extra sprite height

        # Checking up
        tile = self.tile_dict.get((hero_x, hero_y - 1))
        if tile:
            if tile.obstacle is False:
                possible_movements.append("Up")
        # Checking down
        tile = self.tile_dict.get((hero_x, hero_y + 1))
        if tile:
            if tile.obstacle is False:
                possible_movements.append("Down")
        # Checking left
        tile = self.tile_dict.get((hero_x - 1, hero_y))
        if tile:
            if tile.obstacle is False:
                possible_movements.append("Left")
        # Checking right
        tile = self.tile_dict.get((hero_x + 1, hero_y))
        if tile:
            if tile.obstacle is False:
                possible_movements.append("Right")

        return possible_movements

    def check_load_points(self, hero_loc, hero_width, hero_height):
        """
        Checks hero location for a load point that would transport to a new location
        :param hero_loc: tuple (x, y) in pixels, not tiles
        :param hero_width: int
        :param hero_height: int
        :return: boolean if tile is a load point or not
        :return: tile
        """
        # Converts hero_loc from pixels to tiles
        hero_x = int(hero_loc[0] / self.tile_size)
        hero_y = int((hero_loc[1] + (hero_height - hero_width)) / self.tile_size)  # Extra sprite height

        # Checking current tile location
        tile = self.tile_dict.get((hero_x, hero_y))
        assert tile, "Invalid location"
        return tile.load_point, tile

    def check_combat_area(self, hero_loc, hero_width, hero_height):
        """
        Checks hero location to see if tile is a combat area
        :param hero_loc: tuple (x, y) in pixels, not tiles
        :param hero_width: int
        :param hero_height: int
        :return: boolean if tile is a combat area or not
        """
        # Converts hero_loc from pixels to tiles
        hero_x = int(hero_loc[0] / self.tile_size)
        hero_y = int((hero_loc[1] + (hero_height - hero_width)) / self.tile_size)  # Extra sprite height

        # Checking current tile location
        tile = self.tile_dict.get((hero_x, hero_y))
        assert tile, "Invalid location"
        return tile.combat_area
