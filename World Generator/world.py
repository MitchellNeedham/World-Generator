import pygame
import pyperclip
import sys
import os
import math
from random import *


SHALLOW_WATER =  (23, 103, 232)
SHALLOW_MID_WATER = (21, 94, 212)
MID_WATER = (19, 85, 191)
MID_DEEP_WATER = (17, 77, 173)
DEEP_WATER = (16, 70, 158)

FOREST = (117, 237, 43)
WOODS = (93, 201, 26)
TEMPERATE_FOREST = (224, 230, 76)
PLAINS = (103, 245, 42)
GRASSLAND = (165, 214, 73)
HILLS = (62, 230, 98)
HIGH_FOREST_MOUNTAIN = (152, 250, 147)
LOW_FOREST_MOUNTAIN = (99, 186, 95)
BARREN_MOUNTAIN = (164, 207, 157)
BARREN_HILLS = (122, 173, 113)
RAINFOREST = (31, 207, 0)
MARSHLAND = (80, 156, 33)

JUNGLE = (125, 186, 19)
SWAMP = (85, 128, 10)
WET_BARREN_MOUNTAIN = (169, 179, 66)
DESERT = (235, 201, 68)
ARID_MOUNTAIN = (161, 134, 27)
DESERT_PLAINS = (214, 199, 60)
DESERT_HILLS = (209, 186, 56)

SNOW_HILLS = (222, 240, 216)
SNOW_PLAINS = (216, 230, 211)
TAIGA = (169, 186, 164)
ALPINE = (165, 204, 179)
LOW_SNOW_MOUNTAIN = (232, 235, 233)
SNOW_MOUNTAIN = (250, 250, 250)



TILE_HEIGHT = 200
TILE_WIDTH = 300

INIT_ZOOM = 3
MAX_ZOOM = 40
MIN_ZOOM = 0
ZOOM_INCREMENT = 1.1

START_POSITIONS = (200, 150)

tile_types = {
    'shallow water':            (SHALLOW_WATER,             -20,    0,   0, 100,   0, 100),
    'shallow mid water':        (SHALLOW_MID_WATER,         -40,  -20,   0, 100,   0, 100),
    'mid water':                (MID_WATER,                 -60,  -40,   0, 100,   0, 100),
    'mid deep water':           (MID_DEEP_WATER,            -80,  -60,   0, 100,   0, 100),
    'deep water':               (DEEP_WATER,                -100, -80,   0, 100,   0, 100),
						
    'forest':                   (FOREST,                    10, 100, 30, 80, 30, 70),
    'woods':                    (WOODS,                     10, 80, 30, 80, 30, 70),
    'temperate forest':         (TEMPERATE_FOREST,          20, 50, 30, 80, 30, 70),
    'plains':                   (PLAINS,                    0, 30, 30, 80, 30, 70),
    'grassland':                (GRASSLAND,                 0, 40, 30, 80, 30, 70),
    'hills':                    (HILLS,                     20, 50, 30, 80, 30, 70),
    'high forest mountain':     (HIGH_FOREST_MOUNTAIN,      80, 100, 30, 80, 30, 70),
    'low forest mountain':      (LOW_FOREST_MOUNTAIN,       60, 80, 30, 80, 30, 70),
    'barren mountain':          (BARREN_MOUNTAIN,           60, 100, 30, 80, 0, 30),
    'barren_hills':             (BARREN_HILLS,              0, 60, 30, 80, 0, 30),
    'rainforest':               (RAINFOREST,                30, 100, 30, 80, 70, 100),
    'marshland':                (MARSHLAND,                 0, 30, 30, 80, 70, 100),
						
    'jungle':                   (JUNGLE,                    30, 60, 80, 100, 50, 100),
    'swamp':                    (SWAMP,                     0, 40, 80, 100, 50, 100),
    'wet barren mountain':      (WET_BARREN_MOUNTAIN,       60, 100, 80, 100, 50, 100),
    'desert':                   (DESERT,                    0, 30, 80, 100, 0, 50),
    'arid mountain':            (ARID_MOUNTAIN,             60, 100, 80, 100, 0, 50),
    'desert plains':            (DESERT_PLAINS,             0, 50, 80, 100, 0, 50),
    'desert hills':             (DESERT_HILLS,              40, 60, 80, 100, 0, 50),
						
    'snow hills':               (SNOW_HILLS,                20, 50, 0, 30, 0, 100),
    'snow plains':              (SNOW_PLAINS,               0, 30, 0, 30, 0, 100),
    'taiga':                    (TAIGA,                     30, 60, 0, 30, 0, 100),
    'alpine':                   (ALPINE,                    40, 80, 0, 30, 0, 100),
    'low snow mountain':        (LOW_SNOW_MOUNTAIN,         60, 80, 0, 40, 0, 100),
    'snow mountain':            (SNOW_MOUNTAIN,             80, 100, 0, 50, 0, 100)}


AVG_ALT = 50
AVG_TEMP = 40
AVG_HUMIDITY = 40





class world(object):
    def __init__(self, screen, map_size, tile_shape):
        self.screen = screen
        self.map_size = map_size
        self.zoom_level = INIT_ZOOM

        self.tile_list = []

        self.generate_world()

        tile_height = TILE_HEIGHT
        tile_width = TILE_WIDTH
        tile_vert_spacing = 0

        if tile_shape == 1:
            tile_height = tile_width / (2 * math.sin(60 * math.pi / 180)) + tile_width / math.tan(60 * math.pi / 180)

        if tile_shape == 0:
            tile_vert_spacing = tile_height / 2
        elif tile_shape == 1:
            tile_vert_spacing = tile_width / (2 * math.sin(60 * math.pi / 180)) + tile_width / (2 * math.tan(60 * math.pi / 180))


               
        for i in range(map_size[0]):
            for j in range(map_size[1]):

                alt = self.attr_list[i][j][0]
                temp = self.attr_list[i][j][1]
                humidity = self.attr_list[i][j][2]

                key = self.get_tile_type(alt, temp, humidity)

                

                if j % 2 == 0:
                    self.tile_list.append(game_tile(self.screen, tile_width * i, tile_vert_spacing * j, tile_types[key][0], tile_width, tile_height, tile_shape, (i, j), key, self, alt, temp, humidity))
                else:
                    self.tile_list.append(game_tile(self.screen, tile_width * i + tile_width / 2, tile_vert_spacing * j, tile_types[key][0], tile_width, tile_height, tile_shape, (i, j), key, self, alt, temp, humidity))

    def get_tile_list(self):
        return self.tile_list

    def move_world(self, change):

        for tile in self.tile_list:
            tile.x += change[0]
            tile.y += change[1]

    def zoom_world(self, zoom):
        change_zoom = True

        if zoom == 1 and self.zoom_level < MAX_ZOOM:
            self.zoom_level += zoom
        elif zoom == -1 and self.zoom_level > MIN_ZOOM:
            self.zoom_level += zoom
        else:
            change_zoom = False

        if zoom == 1 and change_zoom:
            for tile in self.tile_list:
                tile.x /= ZOOM_INCREMENT
                tile.y /= ZOOM_INCREMENT
                tile.width /= ZOOM_INCREMENT
                tile.height /= ZOOM_INCREMENT

        if zoom == -1 and change_zoom:
            for tile in self.tile_list:
                tile.x *= ZOOM_INCREMENT
                tile.y *= ZOOM_INCREMENT
                tile.width *= ZOOM_INCREMENT
                tile.height *= ZOOM_INCREMENT

    def generate_world(self):
        self.attr_list = []
        coord_list = []
        start_coords = []
        land = True

        for _ in range(self.map_size[0]):
            self.attr_list.append([(None, None, None) for _ in range(self.map_size[1])])

        for i in range(START_POSITIONS[0]):
            if i > START_POSITIONS[1]:
                land = False


            start_coords.append((randint(0, self.map_size[0] - 1), randint(0, self.map_size[1] - 1)))


            self.attr_list[start_coords[i][0]][start_coords[i][1]] = \
                (self.get_alt(start_coords[i], True, land), self.get_temp(start_coords[i], True), self.get_humidity(start_coords[i], True))


       

        

        self.define_new_tile(self.get_nearby_coords(start_coords))



    def define_new_tile(self, coordinates):
        next_coord_list = []
        if coordinates == []:
            return 1




        for coord in coordinates:
            if coord[0] in range(0, self.map_size[0]) and coord[1] in range(0, self.map_size[1]):
                    print('')
            else:
                    continue
            
            self.attr_list[coord[0]][coord[1]] = (self.get_alt(coord, False, True), self.get_temp(coord, False), self.get_humidity(coord, False))

            next_coords = self.get_nearby_coords([coord])
            for next_coord in next_coords:
                if self.attr_list[next_coord[0]][next_coord[1]] == (None, None, None):
                    if next_coord not in next_coord_list:
                        next_coord_list.append(next_coord)

        self.define_new_tile(next_coord_list)

            

    def get_nearby_coords(self, coords):
        nearby_list = []

        repeating = 1

        if repeating == 0:
            for coord in coords:
            
                for new_coord in [(coord[0] + 1, coord[1]), (coord[0], coord[1] + 1), \
                    (coord[0], coord[1] - 1), (coord[0] - 1, coord[1])]:
                    new_coord = (new_coord[0] % (self.map_size[0]), new_coord[1] % (self.map_size[1]))
                    if new_coord not in nearby_list:
                        nearby_list.append(new_coord)

        elif repeating == 1:
            for coord in coords:
            
                for new_coord in [(coord[0] + 1, coord[1]), (coord[0], coord[1] + 1), \
                    (coord[0], coord[1] - 1), (coord[0] - 1, coord[1])]:
                    new_coord = (new_coord[0] % (self.map_size[0]), new_coord[1])
                    
                    if new_coord not in nearby_list and  0 <= new_coord[1] <= self.map_size[1] - 1:
                        nearby_list.append(new_coord)

            

        elif repeating == 2:
            for coord in coords:
            
                for new_coord in [(coord[0] + 1, coord[1]), (coord[0], coord[1] + 1), \
                    (coord[0], coord[1] - 1), (coord[0] - 1, coord[1])]:
                    if 0 <= new_coord[0] <= self.map_size[0] - 1 and 0 <= new_coord[1] <= self.map_size[1] - 1:
                        if new_coord not in nearby_list:
                            nearby_list.append(new_coord)

        return nearby_list

    def get_alt(self, coord, start, land):
        nearby_alts = []


        if start:
            if land:
                return randint(20, 60)
            else:
                return randint(-60, -20)

        

        for nearby in self.get_nearby_coords([coord]):
                
            if self.attr_list[nearby[0]][nearby[1]] != (None, None, None):

                nearby_alts.append(self.attr_list[nearby[0]][nearby[1]][0])

        new_alt = (sum(nearby_alts)) / (len(nearby_alts))

        if new_alt < -25:
            new_alt += randint(-20, 20)
        elif new_alt > 25:
            new_alt += randint(-20, 20)
        elif -25 < new_alt < 0:
            new_alt += randint(-15, 10)
        elif 0 < new_alt < 25:
            new_alt += randint(-7, 20)

        if new_alt > 100:
            new_alt = 100
        elif new_alt < -100:
            new_alt = -100


        return int(new_alt)

    def get_temp(self, coord, start):
        nearby_temps = []
        longitude = math.sqrt(math.pow(int(self.map_size[1]/2) - coord[1], 2))
        relative_pos_temp = (100 - longitude / int(self.map_size[1]/2) * 100)


        if start:
            return relative_pos_temp


        for nearby in self.get_nearby_coords([coord]):
            if self.attr_list[nearby[0]][nearby[1]] != (None, None, None):
                nearby_temps.append(self.attr_list[nearby[0]][nearby[1]][1])

        new_temp = ((sum(nearby_temps) / len(nearby_temps)  + relative_pos_temp * 1) / 2)

        new_temp += randint(-2, 2)

        #if new_temp > 80:
        #    new_temp += randint(-15, 10)
        #elif new_temp > 60:
        #    new_temp += randint(-15, 15)
        #elif new_temp <= 60:
        #    new_temp += randint(-15, 15)

        if new_temp > 100:
            new_temp = 100
        elif new_temp < 0:
            new_temp = 0


        return int(new_temp)


    def get_humidity(self, coord, start):
        nearby_humidity = []

        if start:
            return randint(0, 100)

        for nearby in self.get_nearby_coords([coord]):
            if self.attr_list[nearby[0]][nearby[1]] != (None, None, None):
                nearby_humidity.append(self.attr_list[nearby[0]][nearby[1]][2])
        
        new_humidity = (sum(nearby_humidity)) / (len(nearby_humidity))

        new_humidity += randint(-5, 5)

        if new_humidity > 100:
            new_humidity = 100
        elif new_humidity < 0:
            new_humidity = 0

        return new_humidity

    def get_tile_type(self, alt, temp, humidity):
        possible_types = []

        for item in tile_types.items():
            if item[1][1] <= alt <= item[1][2] and item[1][3] <= temp <= item[1][4] and item[1][5] <= humidity <= item[1][6]:
                possible_types.append(item[0])
        print(alt, temp, humidity, possible_types)


        return choice(possible_types)

    def is_over_tile(self, pos):
        vert_line = self.line_check(pos, 0)
        left_diag = self.line_check(pos, 1)
        right_diag = self.line_check(pos, 2)
        #print(vert_line, left_diag, right_diag)
        is_over_coord = (0, 0)
        pos_in_list = 0

        possible_columns = []
        possible_tiles_left = []
        possible_tiles_right = []

        diag_left_start_tile = (0, 0)
        diag_right_start_tile = (0, 0)

        diag_max_length = 0
        if self.map_size[0] > self.map_size[1]:
            diag_max_length = self.map_size[0]
        else:
            diag_max_length = self.map_size[1]


        if None in (vert_line, left_diag, right_diag) or -1 in (vert_line, left_diag, right_diag):
            return False

        

        if not vert_line % 2:
            if vert_line / 2 - 1 >= 0:
                possible_columns.append(int(vert_line / 2 - 1))
            if not vert_line - 0.5 == self.map_size[0]:
                possible_columns.append(int(vert_line / 2))
        else:
            possible_columns.append(int(vert_line / 2 - 0.5))


        if left_diag % 3 == 2:
            possible_tiles_left.append((0, math.floor(left_diag / 3) * 2 + 1))
        elif left_diag % 3 == 1:
            possible_tiles_left.append((-1, math.floor(left_diag / 3) * 2 + 1))
        elif left_diag % 3 == 0:
            possible_tiles_left.append((-2, math.floor(left_diag / 3) * 2 + 1))

        if right_diag % 3 == 2:
            possible_tiles_right.append((-1, self.map_size[1] - math.floor(right_diag / 3) * 2 - 3))
        elif right_diag % 3 == 1:
            possible_tiles_right.append((-2, self.map_size[1] - math.floor(right_diag / 3) * 2 - 3))
        elif right_diag % 3 == 0:
            possible_tiles_right.append((0, self.map_size[1] - math.floor(right_diag / 3) * 2 - 1))

        
        count_left = 0
        count_right = 0
        for i in range(1, diag_max_length):
            
            if not (i - 1) % 3:
                y_pos = i - count_left
                x_pos = i

                x_pos += possible_tiles_left[0][0]

                count_left += 1
                
                possible_tiles_left.append((x_pos, possible_tiles_left[0][1] - y_pos))
                possible_tiles_left.append((x_pos + 1, possible_tiles_left[0][1] - y_pos))
                possible_tiles_left.append((x_pos + 1, possible_tiles_left[0][1] - (y_pos + 1)))
                possible_tiles_left.append((x_pos + 2, possible_tiles_left[0][1] - (y_pos + 1)))



        for i in range(1, diag_max_length):
            if not (i - 1) % 3:
                y_pos = i - count_right
                x_pos = i

                x_pos += possible_tiles_right[0][0]

                count_right += 1
                
                
                possible_tiles_right.append((x_pos, possible_tiles_right[0][1] + y_pos))
                
                possible_tiles_right.append((x_pos + 1, possible_tiles_right[0][1] + y_pos))
                possible_tiles_right.append((x_pos + 1, possible_tiles_right[0][1] + (y_pos + 1)))
                
                possible_tiles_right.append((x_pos + 2, possible_tiles_right[0][1] + (y_pos + 1)))

        coordinates = sorted(list(set(possible_tiles_right) & set(possible_tiles_left)))

        if len(coordinates) == 0:
            return
        elif len(coordinates) == 1:
            is_over_coord = coordinates[0]


        elif vert_line % 2:
            if coordinates[0][1] % 2:
                is_over_coord = coordinates[1]
            else:
                is_over_coord = coordinates[0]
        else:
            if coordinates[0][1] % 2:
                is_over_coord = coordinates[0]
            else:
                is_over_coord = coordinates[1]

        #print(is_over_coord, coordinates)

        


        return is_over_coord[0] * self.map_size[1] + is_over_coord[1]

        
       
        

        

            










    def line_check(self, pos, line):
        start_tile = self.tile_list[0]
        bottom_left_tile = self.tile_list[self.map_size[1] - 1]
        side_length = start_tile.width / (2 * math.cos(30 * math.pi / 180))

        gradient = math.sin(30 * math.pi / 180) / math.cos(30 * math.pi / 180)


        if not start_tile.coords:
            return None

        line_count = 0
        
        tile_height = start_tile.coords[1][1] - start_tile.coords[0][1]
        tile_width = self.tile_list[0].width

        if self.map_size[0] > self.map_size[1]:
            line_count = int((self.map_size[0] * 2.5 + 1))
        else:
            line_count = int((self.map_size[1] * 2.5 + 1))

        if line == 0:
            line_val = start_tile.x
            for i in range((self.map_size[0] + 1) * 2):

                if pos[0] <= line_val + tile_width / 2 * i:
                    return i - 1
        if line == 1:

            for i in range(line_count):
                intercept = start_tile.coords[2][1] + side_length * i - start_tile.x * -gradient

                if pos[1] < -gradient * pos[0] + intercept:
                    return i - 1
        if line == 2:

            for i in range(-line_count, 0):

                intercept = start_tile.y + (start_tile.height - start_tile.side_point) * self.map_size[1] + side_length + side_length * i - bottom_left_tile.x * gradient

                
                if pos[1] < gradient * pos[0] + intercept:
                    if -i >= line_count:
                        return None
                    return -i - 1


    def hightlight(self, pos):
        if pos or pos == 0:
            if pos >= 0 or pos < self.map_size[0] * self.map_size[1]:
                tile = self.tile_list[pos]
                color = tile_types[tile.key][0]
                tile.color = (255 - int((255 - color[0]) / 1.5), 255 - int((255 - color[1]) / 1.5), 255 - int((255 - color[2]) / 1.5))
                return pos
        return None

    def unhightlight(self, pos):
        if pos or pos == 0:
            if pos >= 0 or pos < self.map_size[0] * self.map_size[1]:
                tile = self.tile_list[pos]
                color = tile_types[tile.key][0]
                tile.color = color
                


            










class game_tile(object):
    def __init__(self, screen, x, y, color, width, height, shape, pos, key, world, alt, temp, humidity):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.shape = shape
        self.pos = pos
        self.key = key
        self.world = world
        self.alt = alt
        self.temp = temp
        self.humidity = humidity

        self.coords = []

        self.side_point = 0

        #self.color = (int(255 * self.temp / 100), int(255 * self.temp / 100), int(255 * self.temp / 100))

        




    def display(self):
        if self.shape == 0:
            coord_left = (self.x, self.y + self.height / 2)
            coord_right = (self.x + self.width, self.y + self.height / 2)
            coord_top = (self.x + self.width / 2, self.y)
            coord_bottom = (self.x + self.width / 2, self. y + self.height)

            self.coords = [coord_top, coord_bottom, coord_left, coord_right]

            if self.onScreen:
                pygame.gfxdraw.filled_polygon(self.screen, (coord_left, coord_top, coord_right, coord_bottom), self.color)

        if self.shape == 1:
            
            self.side_point = self.width / (2 * math.tan(60 * math.pi / 180))

            coord_top = (self.x + self.width / 2, self.y)
            coord_bottom = (self.x + self.width / 2, self. y + self.height)
            coord_top_left = (self.x, self.y + self.side_point)
            coord_bottom_left = (self.x, self.y + self.height - self.side_point)
            coord_top_right = (self.x + self.width, self.y + self.side_point)
            coord_bottom_right = (self.x + self.width, self.y + self.height - self.side_point)

            self.coords = [coord_top, coord_bottom, coord_top_left, coord_bottom_left, coord_top_right, coord_bottom_right]

            if self.onScreen():
                pygame.gfxdraw.filled_polygon(self.screen, ( coord_top_left, coord_top, coord_top_right, coord_bottom_right, coord_bottom, coord_bottom_left), self.color)
                

        


    def onScreen(self):
        if self.x < self.screen.get_width() and self.x + self.width > 0:
            if self.y < self.screen.get_height() and self.y + self.height > 0:
                return True
        return False




