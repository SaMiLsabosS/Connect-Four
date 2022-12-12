# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Sami Melhem
#               Aline Moller
#               Fatima Camci
#               Elsa Silva
# Section:      513
# Assignment:   Lab 12.14
# Date:         15th 11th 2022
#
# PROGRAM: CONNECT FOUR
import re, copy, turtle

play = lambda string: bool(re.search('[y|Y][e|E][s|S]|[y|Y]', string))
player_turn = lambda turn: 1 if (turn % 2 == 1) else 2
count_before_check = 0
start_checking = False


def print_board(board):
    print('------ CONNECT FOUR -------')
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(f'[{board[i][j]}]', end=' ')
        print('\n')
    print(' 1   2   3   4   5   6   7\n')


def check_colNum(board, colNum) -> list:
    for row in range(len(board) - 1, -1, -1):
        if board[row][colNum] == ' ':
            return [True, int(row)]
    return [False, -1]


def add_back_slash(temp, board) -> list:  # Add in more exceptions to create the diagonal faster
    while temp[0] != 0 and temp[1] != 0:
        temp = [temp[0] - 1, temp[1] - 1]
    back_slash = []
    while temp[0] != 6 and temp[1] != 7:
        back_slash.append(board[temp[0]][temp[1]])
        temp = [temp[0] + 1, temp[1] + 1]
    return back_slash


def add_front_slash(temp, board) -> list:  # Add in more exceptions to create the diagonal faster
    while temp[0] != 5 and temp[1] != 0:
        temp = [temp[0] + 1, temp[1] - 1]
    front_slash = []
    while temp[0] != -1 and temp[1] != 7:
        front_slash.append(board[temp[0]][temp[1]])
        temp = [temp[0] - 1, temp[1] + 1]
    return front_slash


def exceptions(board, point) -> list:
    exception = [False, []]
    temp = copy.deepcopy(point)
    back_slash = add_back_slash(temp, board)
    front_slash = add_front_slash(temp, board)
    # Checks for left exception
    if point in [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [2, 0], [3, 6], [4, 5], [4, 6], [5, 4], [5, 5], [5, 6]]:
        exception = [True, back_slash]
    # Checks for right exception
    elif point in [[0, 4], [0, 5], [0, 6], [1, 5], [1, 6], [2, 6], [3, 0], [4, 0], [4, 1], [5, 0], [5, 1], [5, 2]]:
        exception = [True, front_slash]
    # Not an exception
    else:
        exception[1] = [back_slash, front_slash]
    return exception  # [T or F, List of Diagonals]


def check_horizontal(row, chip) -> bool:
    for checkRow in range(len(row) - 3):
        if row[checkRow] == chip and row[checkRow] == row[checkRow + 1] == row[checkRow + 2] == row[checkRow + 3]:
            return True
    return False


def check_vertical(col, chip) -> bool:
    for checkCol in range(len(col) - 3):
        if col[checkCol] == chip and col[checkCol] == col[checkCol + 1] == col[checkCol + 2] == col[checkCol + 3]:
            return True
    return False


def check_diagonal(exception, chip) -> bool:
    if not exception[0]:
        slashes = [exception[1][0], exception[1][1]]  # back_slash, front_slash
        for slash in slashes:
            checkSlash = 0
            while checkSlash + 3 < len(slash):
                if slash[checkSlash] == chip and slash[checkSlash] == slash[checkSlash + 1] == slash[checkSlash + 2] == \
                        slash[checkSlash + 3]:
                    return True
                checkSlash += 1
    else:
        slash = exception[1]
        checkSlash = 0
        while checkSlash + 3 < len(slash):
            if slash[checkSlash] == chip and slash[checkSlash] == slash[checkSlash + 1] == slash[checkSlash + 2] == \
                    slash[checkSlash + 3]:
                return True
            checkSlash += 1
    return False


def check_four(board, colNum, rowNum, chip) -> bool:
    # check horizontal
    row = board[rowNum]
    if check_horizontal(row, chip):
        return True
    # check vertical
    col = [rows[colNum] for rows in board]
    if check_vertical(col, chip):
        return True
    # check diagonals [back_slash, front_slash]
    exception = exceptions(board, [rowNum, colNum])
    if check_diagonal(exception, chip):
        return True
    return False


def change_board(board, colNum, rowNum, chip) -> list:
    board[rowNum][colNum] = chip
    global start_checking
    if start_checking:
        return [board, check_four(board, colNum, rowNum, chip)]
    return [board, False]


def players_turn() -> int:
    while True:
        try:
            colNum = input('Which column do you want to place your chip? ')
            validNum = -1
            if bool(re.search('\d', colNum)) and 0 < int(colNum) < 8:
                validNum += int(colNum)
            elif colNum == 'end': # A quick way to stop the program
                exit()
            else:
                raise ValueError
            valid = check_colNum(board, validNum)
            if valid[0]:
                break
            else:
                print('Column is full')
        except ValueError:
            print('Incorrect Input! Try Again!')
    global count_before_check
    count_before_check += 1
    return [validNum, valid]


def play_game(board, players, current_player):
    while True:
        global count_before_check
        if count_before_check == 42:
            break
        print_board(board)
        player_num = player_turn(current_player)  # returns 1 or 2
        print(f"Player {player_num}'s Turn:\n")
        validList = players_turn()
        board_list = change_board(board, validList[0], validList[1][1], players[player_num - 1])
        current_player += 1
        board = board_list[0]
        if count_before_check > 6:  # 6 chips placed plus the next chip, and then starting to check for winning
            global start_checking
            start_checking = True
        if board_list[1]:
            break

def drawIllusion():
    colors = ['red', 'purple', 'blue', 'green', 'orange', 'yellow']
    pen = turtle.Pen()
    turtle.bgcolor('black')
    turtle.speed(1000)
    for x in range(318):
        pen.pencolor(colors[x % 6])
        pen.width(x // 100 + 1)
        pen.forward(x)
        pen.left(59)

if __name__ == '__main__':
    drawIllusion()
    import_file = open('input_instructions.txt')
    instructions = import_file.read()
    board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    players = ['R', 'Y']
    current_player = 1
    valid = []
    print(f'{instructions}\n')
    if play(input('Do you want to play Connect Four? ')):
        play_game(board, players, current_player)
        print_board(board)
        print(f'Player {player_turn(current_player + 1)} Wins!')
