import pygame
import pytmx
import struct
import Tile_Grid


class Renderer(object):

    def __init__(self, filename):
        """
        Loads map data
        :param filename: string
        """
        self.tilemap = pytmx.util_pygame.load_pygame(filename, pixelalpha=True)
        self.size = (self.tilemap.width * self.tilemap.tilewidth, self.tilemap.height * self.tilemap.tileheight)
        # Creates a tile grid that holds locations of obstacles, spawn points, and exits
        self.tile_grid = Tile_Grid.Tile_Grid(self.tilemap)

    def render(self, surface, hero_image, hero_loc):
        """
        Reads and sorts the data from the map / tmx file
        :param surface: surface to blit images to
        :param hero_image: surface containing hero sprite
        :param hero_loc: tuple (x, y) hero location
        """
        # Converts tilemap background color from hex to rgb and fills the surface
        if self.tilemap.background_color:
            hex = self.tilemap.background_color[1:]
            surface.fill(struct.unpack("BBB", bytes.fromhex(hex)))

        # Iterates through each layer of the tilemap
        for layer in self.tilemap.visible_layers:
            # If the layer is a tile layer
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tilemap.get_tile_image_by_gid(gid)
                    if tile:
                        # Tile is scaled with the size multiplier and is blitted to the surface
                        tile = pygame.transform.scale(tile, (self.tilemap.tilewidth, self.tilemap.tileheight))
                        surface.blit(tile, (x * self.tilemap.tilewidth, y * self.tilemap.tileheight))
                # A blank layer named "Hero" so that the hero sprite is rendered on the correct layer
                if layer.name == "Hero":
                    surface.blit(hero_image, hero_loc)

            # If layer is an object layer with obstacles, spawn points, or exits
            elif isinstance(layer, pytmx.TiledObjectGroup):
                # These layers are only need when self.tile_grid is created in Renderer.__init__
                pass

    def display_map(self, hero_image, hero_loc, size_multiplier):
        """
        Runs the rendering function and returns map surface and location
        :param hero_image: surface with image loaded from png file in Hero
        :param hero_loc: tuple (x, y) hero location
        :param size_multiplier: int for scaling map
        :return: surface
        :return: tuple (x, y) camera offset
        """
        # Temporary surface is created and passed to self.render along with hero_image and hero_loc
        temp = pygame.Surface(self.size)
        self.render(temp, hero_image, hero_loc)

        # Returns surface with map centered around hero
        # TODO: Allow camera zoom to change based on variables
        return temp, ((-hero_loc[0] + 112) * size_multiplier, (-hero_loc[1] + 84) * size_multiplier)
