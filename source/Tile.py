class Tile(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.obstacle = False
        # Load point attributes
        self.load_point = False
        self.new_map = None
        self.new_loc_x = None
        self.new_loc_y = None
        # Combat area attributes
        self.combat_area = False  # If set to true then tile has chance of starting a battle
        self.possible_enemies = []

    def __repr__(self):
        return "obstacle = " + str(self.obstacle)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_map(self):
        return self.new_map

    def get_new_loc(self):
        return self.new_loc

    def set_obstacle(self, boolean):
        assert isinstance(boolean, bool), "Tile.obstacle must be set to a boolean"
        self.obstacle = True

    def set_load_point(self, new_map, new_loc_x, new_loc_y):
        """
        :param new_map: string of filename
        :param new_loc: tuple (x, y) of tile coordinates
        """
        self.load_point = True
        self.new_map = new_map
        self.new_loc_x = new_loc_x
        self.new_loc_y = new_loc_y

    def set_combat_area(self, boolean):
        assert isinstance(boolean, bool), "Tile.combat_area must be set to a boolean"
        self.combat_area = True
