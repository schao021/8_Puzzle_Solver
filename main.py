import heapq # this is for priority queue

dimension = 3 # We can just change this to adjust from 3x3 to like a 4x4

class Node:
    def __init__(self, state, parent=None, cost=0):
        self.state = state # current list
        self.parent = parent # can be used for backtracking if i need
        self.cost = cost  # cost to reach node g(n)

    def __lt__(self, other):
        return self.cost < other.cost # Use this for comparison of node to determine the cost of nodes

    def __str__(self):
        return f"State: {self.state}, Cost: {self.cost}"

def make_node(state, parent=None, cost=0):
    return Node(state, parent, cost)

# Use this to find the blank space for every iteration
def find_blank(state):
    for row in range(dimension):
        for col in range(dimension):
            if state[row][col] == 0:
                return row,col
    print("Error, no blank space found")
    return -1

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
        child_node = make_node(new_state, state, node.cost + 1) # Make a node so i can access the cost later and add 1 per iteration
        children.append(child_node) # append the children after swapping the two
    return children # return the list so we have all the children

basic_puzzle = [[1,2,3],
                [4,5,0],
                [7,8,6]] # should be able to move 6 up 1 and get the answer

example_puzzle_1 = [[4,1,2],
                    [5,3,0],
                    [7,8,6]]

eight_puzzle_goal_state = [[1,2,3],
                           [4,5,6],
                           [7,8,0]]


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

# Uniform is A* with h(n) = 0, so f(n) = g(n) cumulative cost and expand the cheapest node
# The two A* ones we use h(n) according to specific, so that means everything else I think should be the same
# In A*, h(n) is number of misplaced tiles, g(b) is depth of node f(n) = g(n) + h(n), so we want to find the lowest depth

# function general-search(problem, QUEUEING-FUNCTION)
# nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
# loop do 
# if EMPTY(nodes) then return "failure"
#     node = REMOVE-FRONT(nodes)
# if problem.GOAL-TEST(node.STATE) succeeds then return node
#     nodes = QUEUEING- FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
# end

# Priority Queue I think?
# 1. We make initial node and put it into queue
# 2. Loop, remove the front node from queue and expand it
#  2a. If empty: no solution is found and return failure
#  2b. if goal is found, goal state is found, return node with goal state,
#  2c. Else, expand the current node and add its children to queue
# 3. Have a goal_test to check whether or not current node = goal state
# 4. expand the children of the current node base on the actions(Left, right, up, down)
# 5. Quering function to insert expanded node back into queue.

# Uniform Cost Search
def uniform_cost(puzzle,hueristic): # puzzle is the given problem?
    initial_node = make_node(puzzle, None, 0) # root node where the puzzle begin
    priority_queue = []
    heapq.heappush(priority_queue, (initial_node.cost, initial_node))
    visited = set() # I use this to store the visted so that I dont have repeat
    while priority_queue:
        prio_value, cur_node = heapq.heappop(priority_queue) # Pop the node with lowest cost
        if cur_node.state == eight_puzzle_goal_state: # See if the current node we popped is true
            return cur_node # return if the node is true
        
        visited.add(tuple(map(tuple, cur_node.state))) # Add the current node into visted
        # else we expand all the children nodes and push it back into the queue
        row, col = find_blank(cur_node.state)
        possible_moves = find_directions(row, col)
        children = expand_node(cur_node, possible_moves)
        for child in children:
            child_state_tuple = tuple(map(tuple, child.state)) # 
            if child_state_tuple not in visited:
                heapq.heappush(priority_queue, (child.cost, child))  # If we didn't visit it yet, push into heapq and so we don't run into it again
                visited.add(child_state_tuple)
    return "Failure, No Solution Found"

def misplaced_tiles(initial_state, goal_state):
    count = 0
    for i in range(dimension):
        for j in range(dimension):
            initial_tile = initial_state[i][j]
            goal_tile = goal_state[i][j]
            if initial_tile != goal_tile:
                count += 1
    return count

def main():
    valid_input = False # while loop continues to ask user until correct input
    while valid_input == False:   
        select_puzzle = input("This is Simon's CS 170 8-Puzzle, please select 1 for a basic puzzle or 2 to create your own\n")
        if select_puzzle == '1': # Hard Coded initial State
            # print(basic_puzzle)
            valid_input = True
            initial_node = make_node(basic_puzzle)
            # initial_node = make_node(example_puzzle_1)
            print(f"Initial State is: {initial_node.state}")
            print(f"Goal State is: {eight_puzzle_goal_state}")
            print(f"Misplaced Tiles: {misplaced_tiles(initial_node.state, eight_puzzle_goal_state)}")
            # row,col = find_blank(initial_node.state)
            # pos_moves = find_directions(row,col)
            # print(pos_moves)
            # children = expand_node(initial_node,pos_moves)
            # for child in children:
            #     print(child)
            # final_node = uniform_cost(initial_node.state,0)
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

