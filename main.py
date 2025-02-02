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

def main():
    valid_input = False # while loop continues to ask user until correct input
    while valid_input == False:   
        select_puzzle = input("This is Simon's CS 170 8-Puzzle, please select 1 for a basic puzzle or 2 to create your own\n")
        if select_puzzle == '1':
            print(basic_puzzle)
            valid_input = True
        elif select_puzzle == '2':
            print(create_puzzle())
            valid_input = True
        else:
            print("Incorrect input, please select 1 or 2")


main()

