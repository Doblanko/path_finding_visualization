import pygame, threading
import board, node, dijkstra, a_star

if __name__ == '__main__':
    display_width = 700
    display_height = 500
    size = 20
    grey = (128, 128, 128)
    white = (255, 255, 255)
    start_location = [5, 5]
    end_location = [10, 10]
    solution_algorithm = 'dijkstra'

    pygame.init()
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Path Finding Visualization')
    gameDisplay.fill(grey)

    game_board = board.Board(display_height, display_width, start_location, end_location, size)

    clock = pygame.time.Clock()

    crashed = False

    dragging = False

    while not crashed:
        for event in pygame.event.get():

            # drag and drop function
            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_position = pygame.mouse.get_pos()

                # convert mouse position to a grid point
                grid_location = node.Node.get_grid_location(game_board, mouse_position)

                # grid node clicked
                node_clicked = game_board.board[grid_location[0]][grid_location[1]]

                if node_clicked.is_start_node or node_clicked.is_end_node:
                    dragging = True
                    node_hovered = node_clicked
                    node_clicked_color = node_clicked.color
                    node_hovered_color = node_clicked.color
                elif node_clicked.is_wall:
                    node_clicked.set_slow_path()
                elif node_clicked.is_slow_path:
                    node_clicked.reset_grid_type()
                else:
                    node_clicked.set_wall()

            # drag portion of drag and drop
            if event.type == pygame.MOUSEMOTION:
                # todo: don't let someone drag the start on the end or the end on the start
                # todo: reset distances once the start or end node is dragged
                if dragging == True:
                    # reset the previous node color when you leave it without dropping
                    node_hovered.set_color(node_hovered_color)

                    mouse_position = pygame.mouse.get_pos()

                    # convert mouse position to a grid point
                    grid_location = node.Node.get_grid_location(game_board, mouse_position)

                    # determine the node being hovered over
                    node_hovered = game_board.board[grid_location[0]][grid_location[1]]

                    # remember the old color of the hovered node to switch it back
                    node_hovered_color = node_hovered.color
                    node_hovered.set_color(node_clicked_color)

                    if node_hovered != node_clicked:
                        node_clicked.set_color(white)

            # drop portion of drag and drop
            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                if node_clicked.is_start_node:
                    node_clicked.reset_grid_type()
                    game_board.move_start_node(node_hovered.row, node_hovered.column)
                elif node_clicked.is_end_node:
                    node_clicked.reset_grid_type()
                    game_board.move_end_node(node_hovered.row, node_hovered.column)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    solution_algorithm = 'dijkstra'

                if event.key == pygame.K_a:
                    solution_algorithm = 'a_star'

                if event.key == pygame.K_SPACE:

                    if solution_algorithm == 'a_star':
                        # solve the grid on a separate thread to allow for live GUI updates
                        x = threading.Thread(target=a_star.a_star_solver, args=(game_board.board[
                            game_board.start_location[0]][game_board.start_location[1]], game_board.board[
                                                game_board.end_location[0]][game_board.end_location[1]], game_board))
                    elif solution_algorithm == 'dijkstra':
                        # default to dijkstra
                        # solve the grid on a separate thread to allow for live GUI updates
                        x = threading.Thread(target=dijkstra.dijkstra_solver, args=(game_board.board[
                            game_board.start_location[0]][game_board.start_location[1]], game_board))

                    x.start()
                if event.key == pygame.K_r:
                    game_board.reset_solution()


            if event.type == pygame.QUIT:
                crashed = True

        pygame.display.update()
        clock.tick(60)