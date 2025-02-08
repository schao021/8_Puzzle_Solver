import heapq # this is for priority queue

dimension = 3 # We can just change this to adjust from 3x3 to like a 4x4

depth_0_puzzle = [[1,2,3],
                  [4,5,6],
                  [7,8,8]] # should be able to move 6 up 1 and get the answer

depth_2_puzzle = [[1,2,3],
                 [4,5,6],
                 [0,7,8]]

depth_4_puzzle = [[1,2,3],
                  [5,0,6],
                  [4,7,8]]

depth_8_puzzle = [[1,3,6],
                  [5,0,2],
                  [4,7,8]]

depth_12_puzzle = [[1,3,6],
                   [5,0,7],
                   [4,8,2]]

depth_16_puzzle = [[1,6,7],
                   [5,0,3],
                   [4,8,2]]

depth_20_puzzle = [[7,1,2],
                   [4,8,5],
                   [6,3,0]]

depth_24_puzzle = [[0,7,2],
                   [4,6,1],
                   [3,5,8]]

test_puzzle2 = [[7,2,4],
                [5,0,6],
                [8,3,1]]

example_puzzle_1 = [[4,1,2],
                    [5,3,0],
                    [7,8,6]]

example_puzzle_2 = [[1,5,2],
                    [4,8,7],
                    [6,3,0]]

example_test = [[0,7,2],
                [4,6,1],
                [3,5,8]]

eight_puzzle_goal_state = [[1,2,3], # Final Goal State
                           [4,5,6],
                           [7,8,0]]

class Node:
    def __init__(self, state, parent=None, cost=0):
        self.state = state # current list
        self.parent = parent # can be used for backtracking if i need
        self.cost = cost  # cost to reach node g(n)

    def __lt__(self, other):
        return self.cost < other.cost # Use this for comparison of node to which node will be popped

    def __str__(self):
        return f"State: {self.state}, Cost: {self.cost}"

def make_node(state, parent=None, cost=0):
    return Node(state, parent, cost)

def expand_node(node, possible_moves): # expand base on the direction, possible moves is list and state is the current, so we will make children, # change to node to access cost
    children = []
    state = node.state
    # find the blank space first
    row,col = find_blank(state)
    for move in possible_moves:  # iterate through and find all possible moves in list like [up, down, left, right]
        new_state = [row[:] for row in state]
        if move == "up" and row > 0: # all the mvoes i just swap the two
            new_state[row][col], new_state[row - 1][col] = new_state[row - 1][col], new_state[row][col]
        elif move == "down" and row < dimension - 1:
            new_state[row][col], new_state[row + 1][col] = new_state[row + 1][col], new_state[row][col]
        elif move == "left" and col > 0:
            new_state[row][col], new_state[row][col - 1] = new_state[row][col - 1], new_state[row][col]
        elif move == "right" and col < dimension - 1:
            new_state[row][col], new_state[row][col + 1] = new_state[row][col + 1], new_state[row][col]
        child_node = make_node(new_state, node, node.cost + 1) # Make a node so i can access the cost later and add 1 per iteration
        print(child_node)
        children.append(child_node) # append the children after swapping the two
    return children # return the list so we have all the children

# Use this to find the blank space for every iteration
def find_blank(state):
    for row in range(dimension):
        for col in range(dimension):
            if state[row][col] == 0:
                return row,col
    print("Error, no blank space found")
    return -1, -1

# Use the find blank to find the position where I can move left, right down up
def find_directions(row,col):
    possible_moves = []
    if row < dimension - 1:
        possible_moves.append("down")
    if row > 0:
        possible_moves.append("up")
    if col < dimension - 1:
        possible_moves.append("right")
    if col > 0:
        possible_moves.append("left")
    return possible_moves # list out all the possible moves so i can expand the nodes later

def find_location(goal_char, state):
    for row in range(dimension):
        for col in range(dimension):
            if state[row][col] == goal_char: # Compare base on row and col whether it match goal
                return row,col
    print("Error, char not found")
    return -1, -1

def create_puzzle(): # Used to make custom puzzle
    custom_puzzle = []
    # User will enter each number in 123 format
    row_1_puzzle = [int(x) for x in list(input("Please enter 3 numbers for the first row (e.g. 123)\n"))]
    row_2_puzzle = [int(x) for x in list(input("Please enter 3 numbers for the second row (e.g. 123)\n"))]
    row_3_puzzle = [int(x) for x in list(input("Please enter 3 numbers for the third row (e.g. 123)\n"))]
    custom_puzzle.append(row_1_puzzle)
    custom_puzzle.append(row_2_puzzle)
    custom_puzzle.append(row_3_puzzle)
    return custom_puzzle

def print_solution_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    print("\nSolution Path:")
    for state in path:
        for row in state:
            print(row)
        print("---")

def generic_search(puzzle, goal_state, hueristic):
    initial_node = make_node(puzzle, None, 0) # root node where the puzzle begin
    priority_queue = []
    if hueristic == 1: # Uniform
        heapq.heappush(priority_queue, (initial_node.cost, initial_node))
    elif hueristic == 2: # A* with Displaced Tiles
        heapq.heappush(priority_queue, ((initial_node.cost + misplaced_tiles(initial_node.state, goal_state)), initial_node))
    elif hueristic == 3: # A* with Manhatten 
        heapq.heappush(priority_queue, ((initial_node.cost + manhatten(initial_node.state, goal_state)), initial_node))
    else:
        return "Failure, incorrect heuristic option. Must be 1, 2 or 3"
    visited = set() # I use this to store the visted so that I dont have repeat
    nodes_expanded = 0
    max_queue_size = 0 # Both for report
    while priority_queue:
        max_queue_size = max(max_queue_size, len(priority_queue))  # Track the max queue size
        prio_value, cur_node = heapq.heappop(priority_queue) # Pop the node with lowest cost
        nodes_expanded += 1 # After we pop it, that means we expanded
        if cur_node.state == goal_state: # See if the current node we popped is true
            print("\nSolution Found")
            print(f"Solution Depth: {cur_node.cost}")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Max Queue Size: {max_queue_size}")
            print_solution_path(cur_node)
            return cur_node # return if the node is true
        
        visited.add(tuple(map(tuple, cur_node.state))) # Add the current node into visted
        # else we expand all the children nodes and push it back into the queue
        row, col = find_blank(cur_node.state)
        possible_moves = find_directions(row, col)
        children = expand_node(cur_node, possible_moves)
        for child in children:
            child_state_tuple = tuple(map(tuple, child.state))
            if child_state_tuple not in visited:  # If we didn't visit it yet, push into heapq and so we don't run into it again
                if hueristic == 1:
                    heapq.heappush(priority_queue, (child.cost, child))
                elif hueristic == 2:
                    heapq.heappush(priority_queue, (child.cost + misplaced_tiles(child.state, goal_state), child))
                elif hueristic == 3:
                    heapq.heappush(priority_queue, ((child.cost + manhatten(child.state, goal_state)), child))
                # visited.add(child_state_tuple)
    return "Failure, No Solution Found"

def misplaced_tiles(initial_state, goal_state):
    count = 0
    for row in range(dimension):
        for col in range(dimension): # Loop through and check if initial and goal state are the same, if different add 1
            initial_tile = initial_state[row][col]
            goal_tile = goal_state[row][col]
            if initial_tile != goal_tile:
                count += 1
    if count > 1: # This is to account for blank space, because we don't count it as a tile
        count -= 1
    return count

def manhatten(initial_state, goal_state):
    cost = 0 # Hold total cost
    for row in range(dimension):
        for col in range(dimension):
            current_tile = initial_state[row][col]
            if current_tile != 0: # If it isn't a blank space, because blank space doesn't move
                goal_row, goal_col = find_location(current_tile, goal_state)
                row_dif = abs(row - goal_row)
                col_dif = abs(col - goal_col)
                cost += row_dif + col_dif # Find the row and column difference and add it up
    print(cost)
    return cost

def main():
    valid_input = False # while loop continues to ask user until correct input
    while valid_input == False:   
        select_puzzle = input("This is Simon's CS 170 8-Puzzle, please select 1 for a basic puzzle or 2 to create your own\n")
        if select_puzzle == '1': # Hard Coded initial State
            # print(basic_puzzle)
            valid_input = True
            initial_node = make_node(example_test)
            # initial_node = make_node(example_puzzle_1)
            print(f"Initial State is: {initial_node.state}")
            print(f"Goal State is: {eight_puzzle_goal_state}")
            # print(f"Misplaced Tiles: {misplaced_tiles(initial_node.state, eight_puzzle_goal_state)}")
            # print(f"Manhatten Total: {manhatten(initial_node.state, eight_puzzle_goal_state)}")
            # row,col = find_blank(initial_node.state)
            # pos_moves = find_directions(row,col)
            # print(pos_moves)
            # children = expand_node(initial_node,pos_moves)
            # for child in children:
            #     print(child)
            final_node = generic_search(initial_node.state, eight_puzzle_goal_state, 3)
            print(final_node)
            # print(f"This is the initial node {initial_node}")
            # print(f"This is the final node {final_node}")
        elif select_puzzle == '2': # User-Written Initial State
            custom_puzzle = create_puzzle()
            valid_input = True
            initial_node = make_node(custom_puzzle)
            # generic_search(initial_node)
        else:
            print("Incorrect input, please select 1 or 2")


main()

