# Tic Tac Toe
# The Table, The Players, and The Ref
# To do, recursive player

from random import choice


class TheTable:     # Stores game elements, static methods. Read by Players, managed by TheRef
    board = {}           # Ref clears and sets
    valid_moves = []     # Ref adds 1-9 at beginning, removes moves as made
    tokens = ['X', 'O']  # Ref manages and flips. Players access to identify self and opponent (0, 1 respectively)

    @staticmethod
    def draw_board():
        b = TheTable.board
        print(f' {b[7]} | {b[8]} | {b[9]} ')
        print(f'---+---+---')
        print(f' {b[4]} | {b[5]} | {b[6]} ')
        print(f'---+---+---')
        print(f' {b[1]} | {b[2]} | {b[3]} ')

    @staticmethod
    def is_won(board, check):    # user indicates token to check for, board to use (real board, or AI's working board)
        b = board
        x = check
        return (  # Boolean source: nostarch.com/automatestuff
               (b[7] == x and b[8] == x and b[9] == x) or  # top
               (b[4] == x and b[5] == x and b[6] == x) or  # mid
               (b[1] == x and b[2] == x and b[3] == x) or  # low
               (b[7] == x and b[4] == x and b[1] == x) or  # left
               (b[8] == x and b[5] == x and b[2] == x) or  # cen
               (b[9] == x and b[6] == x and b[3] == x) or  # right
               (b[7] == x and b[5] == x and b[3] == x) or  # TL BR \
               (b[9] == x and b[5] == x and b[1] == x))    # TR BL /
# -------------------------------------------------------------------------------------------------------


class Player:
    """Player Class type. Defines final_move object for each player to modify, return to TheRef
    TheRef calls each player's main() to return their move"""

    def __init__(self, final_move=None):
        self.final_move = final_move

    def main(self):
        # self.move_generation()
        # return self.final_move
        print("Called Player is not implemented. Exiting...")
        exit(1)
# -------------------------------------------------------------------------------------------------------


class Human(Player):
    """Human Prompt for Tic Tac Toe.
    Draws board, quick input validation"""

    def get_prompt(self, prompt=None):
        TheTable.draw_board()
        print(f"{TheTable.tokens[0]}, select your move")
        while prompt not in '1 2 3 4 5 6 7 8 9'.split() or int(prompt) not in TheTable.valid_moves:
            prompt = input("> ")
        self.final_move = int(prompt)

    def main(self):
        self.get_prompt()
        return self.final_move


class AiRando(Player):
    """Rando Calrissian plays random moves till his final days"""

    def rando_cal(self):
        print("Rando Sees: ", TheTable.valid_moves)
        self.final_move = choice(TheTable.valid_moves)

    def main(self):
        self.rando_cal()
        return self.final_move


class AiLevi(Player):
    """Opens random, recognizes winning moves
    Since win check block loops through both players, levi() returns to break for loop"""

    def levi(self):
        # Play winning moves, or block opponent ones
        print("Levi sees: ", TheTable.valid_moves)
        for ident in TheTable.tokens:
            for move in TheTable.valid_moves:
                work = TheTable.board.copy()
                work[move] = ident
                if TheTable.is_won(work, ident):
                    return move
        # Otherwise, play random
        print("Random:")
        return choice(TheTable.valid_moves)

    def main(self):
        self.final_move = self.levi()
        return self.final_move


class AiRalph(Player):
    pass


class TheRef(object):
    """The Referee. Tracks game state, rules, and player calls.

    the_setup() set TheTable (Board, valid moves, assigns players to tokens, selects play order)
    spectating() triggers spectator mode if no human players are in play
    play_game() handles player calls, writes moves, alternates between players
    game_over() allows game to run until victory or full board
    play_again() displays results, offers to repeat game
    """

    def __init__(self, get_from=None, next_move=None, results=None, repeating=True):
        self.get_from = get_from        # {'X': {player_function}, 'O': {player_function}}
        self.next_move = next_move      # next move queued for the board
        self.results = results          # Final outcome. String.
        self.repeating = repeating      # Repeats game, set by play_again()

    def the_setup(self):
        # Set the table
        TheTable.board = {}
        TheTable.valid_moves = []
        for y in range(1, 10):
            TheTable.board[y] = ' '
            TheTable.valid_moves.append(y)
        # Assign player calls
        self.get_from = {'X': ' ', 'O': ' '}  # Uses TheTable.tokens[] to call keys
        assignments = [Human, AiRando, AiLevi, AiRalph]
        for char in self.get_from.keys():
            prompt = ''
            print(f"Will '{char}' be (0) human, (1) Rando?, (2) Levi, or (3) Recursive Ralph?")
            while prompt not in '0 1 2 3'.split():
                prompt = input("> ")
            self.get_from[char] = assignments[int(prompt)]()
        # Random starting players
        if choice([0, 1]) == 0:
            TheTable.tokens = TheTable.tokens[::-1]

    def spectating(self):
        if 'Human' not in str(self.get_from):
            print('Spectating...')
            TheTable.draw_board()
            input()

    def play_game(self, ):
        self.spectating()                                   # Spectator mode, triggered by AI only players
        next_player = TheTable.tokens[0]                    # Next player, indicated by first token
        self.next_move = self.get_from[next_player].main()  # Next player selects their move with main()
        TheTable.board[self.next_move] = next_player        # Writes player's token to spot on board
        TheTable.valid_moves.remove(self.next_move)         # Clears move from valid moves
        TheTable.tokens = TheTable.tokens[::-1]             # Flips Tokens

    def game_over(self):
        def game_tied():
            full = ' ' not in list(TheTable.board.values())
            if full:
                self.results = "Game Tied"
            return full
        def game_won():  # Once move is made and tokens flipped, check if previous player's move won game
            won = TheTable.is_won(TheTable.board, TheTable.tokens[1])
            if won:
                self.results = f"{TheTable.tokens[1]} wins"
            return won
        return game_won() or game_tied()

    def play_again(self, prompt=''):
        TheTable.draw_board()
        print(self.results)
        while prompt not in '0 1'.split():
            prompt = input("\n(0) Quit \n(1) Play again \n> ")
        self.repeating = prompt is '1'

    def main(self):
        while self.repeating:
            self.the_setup()
            while not self.game_over():
                self.play_game()
            self.play_again()


if __name__ == '__main__':
    ref = TheRef()
    ref.main()
