basic_puzzle = [[1,2,3],
                [4,5,0],
                [7,8,6]] # should be able to move 6 up 1 and get the answer

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

def main():
    valid_input = False # while loop continues to ask user until correct input
    while valid_input == False:   
        select_puzzle = input("This is Simon's CS 170 8-Puzzle, please select 1 for a basic puzzle or 2 to create your own\n")
        if select_puzzle == '1': # Hard Coded initial State
            print(basic_puzzle)
            valid_input = True
        elif select_puzzle == '2': # User-Written Initial State
            print(create_puzzle())
            valid_input = True
        else:
            print("Incorrect input, please select 1 or 2")


main()

