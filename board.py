import pygame, time
import node

grey = (128, 128, 128)
yellow = (255, 255, 0)
brown_yellow = (204, 153, 102)

class Board():

    def __init__(self, display_height, display_width, start_location, end_location, size):
        # calculate the number of rows and columns based on the display size and grid size
        self.rows = int(display_height / size)
        self.columns = int(display_width / size)
        self.start_location = start_location
        self.end_location = end_location
        self.size = size
        self.board = []
        self.initializeBoard()

    def initializeBoard(self):
        # loop through
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                selected_node = node.Node(i, j, self.size)
                row.append(selected_node)

                # convert position in grid to pixel position
                x_coord = j * self.size
                y_coord = i * self.size

                # draw a rectangle with a border
                pygame.draw.rect(pygame.display.get_surface(), grey, (x_coord, y_coord, self.size, self.size))
                pygame.draw.rect(pygame.display.get_surface(), selected_node.color, (x_coord + 1, y_coord + 1,
                                                                                     self.size - 2, self.size - 2))

            self.board.append(row)
        # set the start node
        start_node = self.board[self.start_location[0]][self.start_location[1]]
        start_node.set_start_node()

        # set the end node
        end_node = self.board[self.end_location[0]][self.end_location[1]]
        end_node.set_end_node()

    def move_start_node(self, row, column):

        # reset the old start node
        self.board[self.start_location[0]][self.start_location[1]].reset_grid_type

        #set the new start node and record the location
        self.start_location = [row, column]
        self.board[self.start_location[0]][self.start_location[1]].set_start_node()

    def move_end_node(self, row, column):

        # reset the old end node
        self.board[self.end_location[0]][self.end_location[1]].reset_grid_type

        #set the new start node and record the location
        self.end_location = [row, column]
        self.board[self.end_location[0]][self.end_location[1]].set_end_node()

    def draw_solution(self):

        end_node = self.board[self.end_location[0]][self.end_location[1]]
        current_node = end_node.visited_from

        #record the path taken
        path = [current_node]

        while current_node.is_start_node == False:
            current_node = current_node.visited_from
            path.append(current_node)

        # remove last value because it is the start node
        path.pop()

        # draw the path from start to finish
        for node in reversed(path):
            if node.is_slow_path:
                node.set_color(brown_yellow)
            else:
                node.set_color(yellow)

            time.sleep(0.05)

    def reset_solution(self, clear_all):
        """Resets the solution part of the board so you can re-solve or clears entire board"""
        for i in range(self.rows):
            for j in range(self.columns):
                self.board[i][j].reset_solution(clear_all)
        # reset properties of start and end node by re-initializing them as start and end nodes
        self.board[self.start_location[0]][self.start_location[1]].set_start_node()
        self.board[self.end_location[0]][self.end_location[1]].set_end_node()


    def grid_check(self, i, j, current_node):
        """Check if gridpoint is a valid next location (in bounds and not diagonal)"""
        # don't go out of i range
        if not -1 < (current_node.row + i) < self.rows: return True

        # skip diagonals
        if abs(i) + abs(j) != 1: return True

        # don't go out of j range
        if not -1 < (current_node.column + j) < self.columns: return True

        return False

    def check_solution_found(self, neighbor_node, neighbor_node_old_color):
        """Check if the solution is found."""
        if neighbor_node.is_end_node:
            neighbor_node.set_color(neighbor_node_old_color)
            self.draw_solution()
            return True

        return False