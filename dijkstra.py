import pygame, heapq, math, time
import node

grey = (211, 211, 211)
blue = (0, 0, 255)
grey_brown = (168, 147, 125)

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
        if current_distance > current_node.distance:
            continue

        for i in [-1, 0, 1]:
            # stop if solution found
            if solution_found == True:
                break

            # don't go out of range
            if not -1 < (current_node.row + i) < game_board.rows:
                continue

            for j in [-1, 0, 1]:
                # stop if solution found
                if solution_found == True:
                    break

                # skip diagonals
                if abs(i) + abs(j) != 1:
                    continue
                # don't go out of range
                if not -1 < (current_node.column + j) < game_board.columns:
                    continue

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

                new_distance = current_node.distance + neighbor_node.weight

                # Only consider this new path if it's better than any path we've
                # already found.
                if new_distance < neighbor_node.distance:
                    neighbor_node.set_distance(new_distance)
                    neighbor_node.set_visited_from(current_node)

                    order_added += 1
                    heapq.heappush(pq, (neighbor_node.distance, order_added, neighbor_node))

                    # check if you found the solution
                    if neighbor_node.is_end_node:
                        neighbor_node.set_color(neighbor_node_old_color)
                        game_board.draw_solution()

                        # break out of the loops
                        solution_found = True
                        break


                # change the node to the searched color
                if neighbor_node.is_start_node == False:
                    if neighbor_node.is_slow_path:
                        neighbor_node.set_color(grey_brown)
                    else:
                        neighbor_node.set_color(grey)
                else:
                    neighbor_node.set_color(neighbor_node_old_color)