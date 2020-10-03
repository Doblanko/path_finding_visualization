import math
import pygame
white = (255, 255, 255)
black = (0, 0, 0)
brown = (139, 69, 19)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

class Node:
    def __init__(self, row, column, size):
        self.row = row
        self.column = column
        self.size = size
        self.set_color(white)
        self.is_start_node = False
        self.is_end_node = False
        self.set_distance(math.inf)
        self.visited = False
        self.set_visited_from(None)
        self.is_wall = False
        self.is_slow_path = False
        self.weight = 1

        # A* search parameters
        # f is the sum of distance (to the start node) and a heuristic of the distance to the finish (h)
        self.a_star_f = math.inf
        self.a_star_h = math.inf

    def set_start_node(self):
        self.is_start_node = True
        self.set_distance(0)
        self.set_color(green)
        self.set_a_star_h(0)
        self.set_a_star_f()

    def set_end_node(self):
        self.is_end_node = True
        self.set_color(red)

    def set_distance(self, distance):
        self.distance = distance

    def set_visited_from(self, visited_from):
        self.visited_from = visited_from

    def set_color(self, color):
        self.color = color

        # convert position in the grid to pixel position
        x_coord = self.column * self.size
        y_coord = self.row * self.size

        pygame.draw.rect(pygame.display.get_surface(), self.color, (x_coord + 1, y_coord + 1,
                                                                             self.size - 2, self.size - 2))

    def set_wall(self):
        self.reset_grid_type()
        self.is_wall = True
        self.set_color(black)

    def set_slow_path(self):
        self.reset_grid_type()
        self.is_slow_path = True
        self.set_color(brown)
        self.weight = 4

    def reset_grid_type(self):
        self.is_slow_path = False
        self.is_wall = False
        self.is_start_node = False
        self.is_end_node = False
        self.set_color(white)
        self.weight = 1

    def reset_solution(self):
        self.set_visited_from(None)
        self.set_distance(math.inf)
        if self.is_slow_path:
            self.set_color(brown)
        elif self.is_wall == False:
            self.set_color(white)

    def set_a_star_f(self):
        self.a_star_f = self.distance + self.a_star_h

    def set_a_star_h(self, h):
        self.a_star_h = h

    @classmethod
    def get_grid_location(cls, game_board, mouse_position):
        grid_location = []
        grid_location.append(math.trunc(mouse_position[1] / game_board.size))
        grid_location.append(math.trunc(mouse_position[0] / game_board.size))
        return grid_location