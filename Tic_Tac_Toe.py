#printing the board
from IPython.display import clear_output

def display_board(board):
    clear_output()
    print(board[0:3])
    print(board[3:6])
    print(board[6:9])


#default board
test_board = ['1','2','3','4','5','6','7','8','9']
display_board(test_board)

# Players choices on mark
def player_input():
    input_choice = ""
    while input_choice != "X" or input_choice != "O":
        input_choice = input("Please input your choice ('X' or 'O')")    
        if input_choice == "X" or input_choice == "O":
            return input_choice
        else:
            print("your choice is invalid")


#Combine all function into it (the board, marker, and position) and assign the choice of Marker to the board
def place_marker(board, marker, position):
    board[position-1] = marker
    display_board(board)


#winning check function
def win_check(board, mark):
    winners = [
        [1, 2, 3], [1, 5, 9], [3, 5, 7],  # Diagonals
        [1, 4, 7], [2, 5, 8], [3, 6, 9],  # Columns
        [4, 5, 6], [7, 8, 9]              # Rows
    ]
    bool_list_check = [] 
    for winner in winners:
        check = True  # Assume the current combination is a win
        for pos in winner:
            if board[pos-1] != mark:  # If any position doesn't match the mark
                check = False  # It's not a win
                break  # No need to check further
        bool_list_check.append(check)  # Append the result for this combination
    if any(bool_list_check) == True:
        return True
    if any(bool_list_check) == False:
        pass

#random pick on X/O for the start first
import random

def choose_first():
    random_choice = random.choice(["X","O"])
    print(random_choice)


#check if space available
def space_check(board, position):
    return board[position] not in ["X", "O"]


#check if the board is full
def full_board_check(board):
    occupied_num = 0
    for num in board:
        if num in ["X","O"]:
            occupied_num += 1
        else:
            pass
    if occupied_num == 9:
        return True
    else:
        return False


#return input if the position is available
def player_choice(board):
    input_choice = ""
    while True:
        try:
            input_choice = int(input("Please input your choice (1-9): "))    
            if input_choice in range(1,10): 
                if board[input_choice-1] not in ["X", "O"]:
                    return input_choice 
                else:
                    print("This position is already taken. Please choose another.")
            else:
                print("Your choice is invalid. Please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

#check if continuous
def replay():
    play = ""
    while play != "Y" and play != "N":
        play = input("Do you want to play again? Y or N")
        if play == "Y":
            return True
        if play == "N":  
            return False

#Start game greetings
def start_game():
    play = ""
    while play != "Y" and play != "N":
        play = input("Do you want to start the game? Y or N")
        if play == "Y":
            return True
        if play == "N":  
            return False

#putting them all together:
print('Welcome to Tic Tac Toe!')
if start_game() == True:
    continuous = True
    #while True:
    while continuous == True:
        
        # Set the game up here
        print("Here is the empty game board")
        game_board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        display_board(game_board)
        
        #user pick side
        player1 = player_input()
        if player1 == "X":
            player2 = "O"
        else:
            player2 = "X"
        #while game_on:
        game_on = True
        while game_on == True:

            #Player 1 Turn
            print("Now, it is Player 1's turn to move") 
            place_marker(game_board, player1, player_choice(game_board))
            if win_check(game_board, player1) == True:
                print("Player 1 Wins! Congratulations!")
                break
            if full_board_check(game_board) == True: 
                print("Full Board, Game over")
                break
                
            # Player2's turn.
            print("Now, it is Player 2's turn to move")
            place_marker(game_board, player2, player_choice(game_board))
            if win_check(game_board, player2) == True:
                print("Player 2 Wins! Congratulations!")
                break
            if full_board_check(game_board) == True: 
                print("Full Board, Game over")
                break

    #if not replay():
        if not replay():
            continuous = False
            print("Thank you for playing")

