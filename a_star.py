import pygame, heapq, math, time
import node, board

grey = (211, 211, 211)
blue = (0, 0, 255)
grey_brown = (168, 147, 125)

def a_star_solver(start_node, end_node, game_board):
    """Solve for the optimal path using A* algorithm"""
    # form priority queue
    # first digit = distance, second = order added, third = node
    # need order added to avoid nodes with same distance
    order_added = 0
    pq = [(0, order_added, start_node)]
    solution_found = False

    while len(pq) > 0 and not solution_found:
        current_a_star_f, current_order, current_node = heapq.heappop(pq)

        # Nodes can get added to the priority queue multiple times. We only
        # process a vertex the first time we remove it from the priority queue.
        #if current_a_star_f > current_node.a_star_f:
            #continue

        for i in [-1, 0, 1]:
            # stop if solution found
            if solution_found: break

            # don't go out of range
            if not -1 < (current_node.row + i) < game_board.rows: continue

            for j in [-1, 0, 1]:
                # stop if solution found
                if solution_found: break

                if game_board.grid_check(i, j, current_node): continue

                # define the node being looked at as neighbor node for simplicity
                neighbor_node = game_board.board[current_node.row + i][current_node.column + j]

                # remember the old color and change it to searching color
                neighbor_node_old_color = neighbor_node.color
                neighbor_node.set_color(blue)

                # slow down animation
                time.sleep(0.005)

                # skip walls
                if neighbor_node.is_wall:
                    neighbor_node.set_color(neighbor_node_old_color)
                    continue

                (pq, order_added) = path_check(current_node, neighbor_node, end_node, pq, order_added)

                if game_board.check_solution_found(neighbor_node, neighbor_node_old_color):
                    solution_found = True
                    break

                # change the node to the searched color
                neighbor_node.change_color_searched(neighbor_node_old_color)

def path_check(current_node, neighbor_node, end_node, pq, order_added):
    """Check if the new path to the node is shorter than any previous path"""

    new_distance = current_node.distance + neighbor_node.weight
    new_a_star_h = abs(neighbor_node.row - end_node.row) + abs(neighbor_node.column - end_node.column)
    new_a_star_f = new_distance + new_a_star_h

    if new_a_star_f < neighbor_node.a_star_f:
        neighbor_node.set_distance(new_distance)
        neighbor_node.set_a_star_h(new_a_star_h)
        neighbor_node.set_a_star_f()
        neighbor_node.set_visited_from(current_node)

        order_added += 1
        heapq.heappush(pq, (neighbor_node.a_star_f, order_added, neighbor_node))

    return(pq, order_added)