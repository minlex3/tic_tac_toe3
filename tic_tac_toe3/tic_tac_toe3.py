import random
import sys

kwords = ["user", "easy", "medium", "hard"]
USER_TURN = False
AI_TURN = True

class TicTac:
    board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    exit = False

    def show(self, text=None):
        if text != None:
            print(text)
        print("---------")
        print("|"," ".join(self.board[2]), "|")
        print("|"," ".join(self.board[1]), "|")
        print("|"," ".join(self.board[0]), "|")
        print("---------")

    def input_param(self):
        text = input("Input command: ").split()
        if text[0] == "exit":
            self.exit = True
            self.player_1 = 0
            self.player_2 = 0
        elif (text[0] == "start") and (len(text) == 3) and (text[1] in kwords) and (text[2] in kwords):
            self.player_1 = text[1]
            self.player_2 = text[2]
            self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
            self.show()
        else:
            print("Bad parameters!")
            self.input_param()

    def user(self, char):
        point = input("Enter the coordinates: ").split()
        if all([x.isdigit() for x in point]):
            if all([0 < int(x) < 4 for x in point]):
                if self.board[int(point[1]) - 1][int(point[0]) - 1] == " ":
                    self.move((int(point[1]) - 1), (int(point[0]) - 1), char)
                    self.show()
                    #self.check()
                else:
                    print("This cell is occupied! Choose another one!")
                    self.user(char)
            else:
                print("Coordinates should be from 1 to 3!")
                self.user(char)
        else:
            print("You should enter numbers!")
            self.user(char)

    def easy(self, char, text=None):
        x = random.randrange(3)
        y = random.randrange(3)
        if self.board[x][y] == " ":
            self.move(x, y, char)
            if text == None:
                self.show('Making move level "easy"')
            else:
                self.show(text)
        else:
            self.easy(char, text)

    def medium(self, char):
        pair = self.check_pairs(char)
        if pair == 0:
            alt_char = 'O' if char == 'X' else 'X'
            pair = self.check_pairs(alt_char)
            if pair == 0:
                self.easy(char, 'Making move level "medium"')
                return
        pair = pair.split()
        self.move(int(pair[1]), int(pair[0]), char)
        self.show('Making move level "medium"')

    def check_pairs(self, char):
        for j in range(3):
            letter_count = space_count = 0
            for i in range(3):
                if self.board[i][j] == char:
                    letter_count += 1
                elif self.board[i][j] == " ":
                    space_count += 1
                    space = str(j) + " " + str(i)
            if letter_count == 2 and space_count == 1:
                return space
        for i in range(3):
            letter_count = space_count = 0
            for j in range(3):
                if self.board[i][j] == char:
                    letter_count += 1
                elif self.board[i][j] == " ":
                    space_count += 1
                    space = str(j) + " " + str(i)
            if letter_count == 2 and space_count == 1:
                return space
        letter_count = space_count = 0
        for i in range(3):
            if self.board[i][i] == char:
                letter_count += 1
            elif self.board[i][i] == " ":
                space_count += 1
                space = str(i) + " " + str(i)
        if letter_count == 2 and space_count == 1:
            return space

        if self.board[0][2] == self.board[1][1] == char and self.board[2][0] == " ":
            return '0 2'
        if self.board[0][2] == self.board[2][0] == char and self.board[1][1] == " ":
            return '1 1'
        if self.board[2][0] == self.board[1][1] == char and self.board[0][2] == " ":
            return '2 0'
        return 0

    def hard(self, char):
        move = None
        char_user = 'O' if char == 'X' else 'X'
        self.best_score = -sys.maxsize
        self.board_copy = [self.board[y].copy() for y in range(3)]
        for y in range(3):
            for x in range(3):
                if self.board_copy[y][x] == " ":
                    self.board_copy[y][x] = char
                    self.score = self.minimax(0, USER_TURN, char, char_user)
                    self.board_copy[y][x] = " "
                    if self.score > self.best_score:
                        self.best_score = self.score
                        move = (y, x)
        self.move(move[0], move[1], char)
        self.show('Making move level "hard"')

    def minimax(self, depth, is_ai_turn, char, char_user):
        if self.check(char, self.board_copy):
            return 1
        elif self.check(char_user, self.board_copy):
            return -1
        elif all([member != " " for group in self.board_copy for member in group]):
            return 0

        if is_ai_turn:
            best_score = -sys.maxsize
            for y in range(3):
                for x in range(3):
                    if self.board_copy[y][x] == ' ':
                        self.board_copy[y][x] = char
                        score = self.minimax(depth + 1, USER_TURN, char, char_user)
                        self.board_copy[y][x] = ' '
                        if score > best_score:
                            best_score = score
        else:
            best_score = sys.maxsize
            for y in range(3):
                for x in range(3):
                    if self.board_copy[y][x] == ' ':
                        self.board_copy[y][x] = char_user
                        score = self.minimax(depth + 1, AI_TURN, char, char_user)
                        self.board_copy[y][x] = ' '
                        if score < best_score:
                            best_score = score
        return best_score

    def move(self, x, y, char):
        self.board[int(x)][int(y)] = char

    def check(self, char, field=None):
        if field == None:
            field = self.board
        if field[1][1] == char:
            if (    field[0][0] == field[2][2] == char or 
                    field[0][2] == field[2][0] == char or 
                    field[0][1] == field[2][1] == char or 
                    field[1][0] == field[1][2] == char):
                return True
        if field[2][0] == char:
            if (    field[2][1] == field[2][2] == char or 
                    field[0][0] == field[1][0] == char):
                return True
        if field[0][2] == char:
            if (    field[0][0] == field[0][1] == char or 
                    field[1][2] == field[2][2] == char):
                return True
    
    def check_full(self):
        if self.check('X'):
            print('X wins\n')
            return True
        elif self.check('O'):
            print('O wins\n')
            return True
        elif all([member != " " for group in self.board for member in group]):
            print('Draw\n')
            return True
        else:
            return False

def game_main():
    while True:
        game.input_param()
        if game.exit == True:
            return
        while True:
            if game.player_1 == 'user':
                game.user('X')
            if game.player_1 == 'easy':
                game.easy('X')
            if game.player_1 == 'medium':
                game.medium('X')
            if game.player_1 == 'hard':
                game.hard('X')
            if game.check_full():
                break
            if game.player_2 == 'user':
                game.user('O')
            if game.player_2 == 'easy':
                game.easy('O')
            if game.player_2 == 'medium':
                game.medium('O')
            if game.player_2 == 'hard':
                game.hard('O')
            if game.check_full():
                break

game = TicTac()
game_main()

