import pygame, heapq, math, time
import node, board

blue = (0, 0, 255)

def dijkstra_solver(start_node, game_board):
    """Solve for the optimal path using dijkstra's algorithm"""
    # form priority queue
    # first digit = distance, second = order added, third = node
    # need order added to avoid nodes with same distance
    order_added = 0
    pq = [(0, order_added, start_node)]
    solution_found = False

    while len(pq) > 0 and not solution_found:
        current_distance, current_order, current_node = heapq.heappop(pq)

        # Nodes can get added to the priority queue multiple times. We only
        # process a vertex the first time we remove it from the priority queue.
        # todo: does this even make sense? they will always be the same
        if current_distance > current_node.distance:
            continue

        for i in [-1, 0, 1]:

            if solution_found: break

            for j in [-1, 0, 1]:

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

                (pq, order_added) = path_check(current_node, neighbor_node, pq, order_added)

                if game_board.check_solution_found(neighbor_node, neighbor_node_old_color):
                    solution_found = True
                    break

                neighbor_node.change_color_searched(neighbor_node_old_color)


def path_check(current_node, neighbor_node, pq, order_added):
    """Check if the new path to the node is shorter than any previous path"""

    new_distance = current_node.distance + neighbor_node.weight

    if new_distance < neighbor_node.distance:
        neighbor_node.set_distance(new_distance)
        neighbor_node.set_visited_from(current_node)

        order_added += 1
        heapq.heappush(pq, (neighbor_node.distance, order_added, neighbor_node))

    return(pq, order_added)