# Tic Tac Toe
# The Table, The Players, and The Ref

# todo Recursive overhaul (still reliant on immediate win-check)
# todo touchups, see sub todo's
# todo General cleanup/polish


from random import choice
from time import sleep
from typing import * # todo type hints


class TheTable:          
    """The Table, central storage for all game elements and static
    functions for player/ref use
    Fully managed by The Referee"""
    # todo table will eventually have non-static functions. rewrite

    the_board = {}
    valid_moves = []
    tokens = ['X', 'O']
    next_token = None
    # todo at current, next player is tokens[0], with list flipped after each turn.
    # todo create stand alone

    def set_table(self):
        """Prepare table for new game, clearing out old entries and preparing new board"""
        # todo test, prepare to work with global table obj
        self.the_board = {}
        self.valid_moves = []
        tokens = ['X', 'O']
        for y in range(1, 10):
            TheTable.the_board[y] = ' '
            TheTable.valid_moves.append(y)

    def place_token(self):
        # todo
        """No validity check, places token on and flips var next_token"""

    @staticmethod
    def draw_board():
        b = TheTable.the_board
        print(f' {b[7]} | {b[8]} | {b[9]} ')
        print(f'---+---+---')
        print(f' {b[4]} | {b[5]} | {b[6]} ')
        print(f'---+---+---')
        print(f' {b[1]} | {b[2]} | {b[3]} ')

    @staticmethod
    def is_won(board, check):    # real or AI's work board, token to check for
        b = board
        x = check
        return (  # Boolean borrowed from nostarch.com/automatestuff
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
    """TheRef calls appropriate player's main() to return final_move
    Each player determines move in unique methods"""

    def __init__(self, ):
        self.final_move = None
        self.name = None

    def calculate(self):
        """Player specific function, where player subclass decides next move"""
        print("Called Player is not implemented. Exiting...")
        exit(1)

    def main(self):
        self.calculate()

# -------------------------------------------------------------------------------------------------------


class Human(Player):
    """Human Prompt for Tic-Tac-Toe.
    Draws board, quick input validation"""

    def __init__(self, ):
        super().__init__()

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
    """Rando plays random moves till his final days"""

    def __init__(self, final_move=None):
        self.final_move = final_move

    def calculate(self):
        self.final_move = choice(TheTable.valid_moves)

    def main(self):
        self.calculate()
        return self.final_move


class AiLevi(Player):
    """Opens random, recognizes winning moves
    Levi checks for immediate winning moves, otherwise plays random
    """
    
    def __init__(self, final_move=None):
        self.final_move = final_move

    def win_check(self):
        # Play winning moves, or block opponent ones
        for token in TheTable.tokens:
            for move in TheTable.valid_moves:
                work = TheTable.the_board.copy()
                work[move] = token
                if TheTable.is_won(work, token):
                    return move
        # Otherwise, play random
        return choice(TheTable.valid_moves)

    def levi(self):
        self.final_move = self.levi()
        
    def main(self):
        self.levi()
        return self.final_move


class AiRalph(Player):
    """Recursive Ralph
    Uses immediate check, then uses recursive analysis to find preferable positions

    prepare() copies info from The Table to reduce cross class pulls, preps score dict
    Win_check() identifies next move victories or defeats
    recur() uses recursion to score every condition 6 moves ahead in the game
    score_check() finds the highest or lowest score (+/-) and plays it.
        Random tie breaker if scores identical (i.e. symmetrical corners)
    ralph() uses win_check to identify immediacy, otherwise uses recur
    """

    def __init__(self, scores=None, players=None, clone_board=None, final_move=None):
        self.scores = scores
        self.players = players
        self.clone_board = clone_board
        self.final_move = final_move

    def prepare(self):
        self.scores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        # self.scores = {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0), 5: (0, 0),
        # 6: (0, 0), 7: (0, 0), 8: (0, 0), 9: (0, 0)}
        self.players = TheTable.tokens.copy()
        self.clone_board = TheTable.the_board.copy()

    def win_check(self):
        for token in self.players:
            for move in TheTable.valid_moves:
                work = self.clone_board.copy()
                work[move] = token
                if TheTable.is_won(work, token):
                    return move

    def recur(self, board, tokens, depth, last):
        work = board.copy()
        if depth > 6:
            return False    # cuts quarter million games down to 75k, reducing move 9 counts
        elif TheTable.is_won(work, self.players[0]):
            self.scores[last] += 10 - depth
        elif TheTable.is_won(work, self.players[1]):
            self.scores[last] -= 10 - depth
        else:
            for key, var in work.items():
                if var == ' ':
                    work[key] = tokens[0]
                    self.recur(work, tokens[::-1], depth + 1, key)
                    work[key] = ' '
                    
    def score_check(self):
        out = []
        scored = list((v, k) for k, v in self.scores.items())
        target = max(-min(scored)[0], max(scored)[0])
        if target != 0:
            for v, k in scored:
                if abs(v) == target:
                    out.append(k)
            return choice(out)
        else:
            return choice(TheTable.valid_moves)

    def ralph(self):
        self.prepare()
        self.final_move = self.win_check()
        if not self.final_move:
            self.recur(TheTable.the_board, self.players, 1, 0)
            self.final_move = self.score_check()

    def main(self):
        self.ralph()
        return self.final_move


class TheRef(object):
    """The Referee, game master and rule keeper
    the_setup   set TheTable (Board, valid moves, players calls, play order)
    spectating  opt spectator mode triggered by no_human
    play_game   calls players, writes moves, alternates turns players
    game_over   checks for term states (wins, ties)
    play_again  displays results, offers to repeat game
    """
    # todo the ref contains board logic and operations. Move to board, allow ref to create global class and

    def __init__(self):
        self.get_from = None
        """" 'X': {player_object}, 'O': {player_object} """
        self.next_move = None
        """" player sourced move, queued for board write """
        self.results = None
        """ Game over string """
        self.repeating = True
        """ Repeats game, set by play_again() """
        self.no_human = False
        """ Flag set if no human player detected"""

    def the_setup(self):
        # todo move to Table
        # Set the table
        TheTable.the_board = {}
        TheTable.valid_moves = []
        for y in range(1, 10):
            TheTable.the_board[y] = ' '
            TheTable.valid_moves.append(y)

        # todo this might be ok. Ref should keep player calls. Move to own func
        # Assign player calls
        self.get_from = {'X': ' ', 'O': ' '}
        assignments = (Human, AiRando, AiLevi, AiRalph)
        for char in self.get_from.keys():
            prompt = ''
            print(f"Will '{char}' be (0) human, (1) Rando, (2) Levi, or (3) Ralph?")
            while prompt not in '0 1 2 3'.split():
                prompt = input("> ")
            self.get_from[char] = assignments[int(prompt)]()

        # todo check spectate flag, rename no_human -> spectating
        # To spectate
        self.no_human = 'Human' not in str(self.get_from)
        # Random starting players
        if choice([0, 1]) == 0:
            TheTable.tokens = TheTable.tokens[::-1]

    def spectate(self, last_player):
        # todo consider specate line move to a part of "who's turn next"
        print(last_player, 'played', self.next_move)
        TheTable.draw_board()
        # sleep(1)
        input()
        '''if 'Human' not in str(self.get_from):
            print(last_player, 'played', self.next_move)
            TheTable.draw_board()
            input()'''

    def play_game(self):
        """ 1) IDs next player via first sorted token
            2) Calls that player's main(), they hand move to ref
            3) Ref writes move to board
            4) Clears the move from valid list
            5) Opt spectator mode
            6) Flips tokens (remember, first token is always next player)"""
        # todo these need to be separate functions!
        next_player = TheTable.tokens[0]
        self.next_move = self.get_from[next_player].main()
        TheTable.the_board[self.next_move] = next_player
        TheTable.valid_moves.remove(self.next_move)
        if self.no_human:
            self.spectate(next_player)
        TheTable.tokens = TheTable.tokens[::-1]

    def game_over(self):
        # todo consider properties in TheTable
        #  todo (table knows if game is over, or won, but ref acts on it)
        def game_won():  # Tokens already flipped. checks if prev player won
            won = TheTable.is_won(TheTable.the_board, TheTable.tokens[1])
            if won:
                self.results = f"{TheTable.tokens[1]} wins"
            return won
        def game_tied():
            full = ' ' not in list(TheTable.the_board.values())
            if full:
                self.results = "Game Tied"
            return full
        return game_won() or game_tied()

    def play_again(self, prompt=''):
        TheTable.draw_board()
        print(self.results)
        while prompt not in '0 1'.split():
            prompt = input("\n(0) Quit \n(1) Play again \n> ")
        self.repeating = prompt == '1'

    def main(self):
        # todo good running loop. Consider moving play game features
        #  to separate functions, and calling in main loop
        while self.repeating:
            self.the_setup()
            while not self.game_over():
                self.play_game()
            self.play_again()


if __name__ == '__main__':
    ref = TheRef()
    ref.main()
