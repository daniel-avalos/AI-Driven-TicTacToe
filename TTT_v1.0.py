# Tic Tac Toe
# The Table, The Players, and The Ref

# To Do:
# # Gigantic technical report
# # Recursive overhaul (still reliant on immediate win-check)
# # General cleanup/polish


from random import choice


class TheTable:          # Stores game, static methods. Read by Players, run by TheRef
    the_board = {}       # Dict of num-pad keys to placed tokens
    valid_moves = []     # list of free spaces, ref managed
    tokens = ['X', 'O']  # first token is next player (ref randomizes and flips)

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

    def main(self):
        print("Called Player is not implemented. Exiting...")
        exit(1)
# -------------------------------------------------------------------------------------------------------


class Human(Player):
    """Human Prompt for Tic Tac Toe.
    Draws board, quick input validation"""

    def __init__(self, final_move=None):
        self.final_move = final_move

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

    def main(self):
        return choice(TheTable.valid_moves)


class AiLevi(Player):
    """Opens random, recognizes winning moves
    levi() checks for immediate winning moves, otherwise plays random
    """

    @staticmethod
    def levi():
        # Play winning moves, or block opponent ones
        for token in TheTable.tokens:
            for move in TheTable.valid_moves:
                work = TheTable.the_board.copy()
                work[move] = token
                if TheTable.is_won(work, token):
                    return move
        # Otherwise, play random
        return choice(TheTable.valid_moves)

    def main(self):
        return self.levi()


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
    """The Referee. Tracks game state, rules, and player calls.

    the_setup() set TheTable (Board, valid moves, assigns players calls, sets play order)
    spectating() triggers spectator mode if no human players are in play
    play_game() handles player calls, writes moves, alternates between players
    game_over() allows game to run until victory or full board
    play_again() displays results, offers to repeat game
    """

    def __init__(self, get_from=None, next_move=None, results=None, repeating=True,
                 no_human=False):
        self.get_from = get_from        # {'X': {player_function}, 'O': {player_function}}
        self.next_move = next_move      # player sourced move, queued for board write
        self.results = results          # Game over string
        self.repeating = repeating      # Repeats game, set by play_again()
        self.no_human = no_human

    def the_setup(self):
        # Set the table
        TheTable.the_board = {}
        TheTable.valid_moves = []
        for y in range(1, 10):
            TheTable.the_board[y] = ' '
            TheTable.valid_moves.append(y)
        # Assign player calls
        self.get_from = {'X': ' ', 'O': ' '}
        assignments = (Human, AiRando, AiLevi, AiRalph)
        for char in self.get_from.keys():
            prompt = ''
            print(f"Will '{char}' be (0) human, (1) Rando, (2) Levi, or (3) Ralph?")
            while prompt not in '0 1 2 3'.split():
                prompt = input("> ")
            self.get_from[char] = assignments[int(prompt)]()
        # To spectate
        self.no_human = 'Human' not in str(self.get_from)
        # Random starting players
        if choice([0, 1]) == 0:
            TheTable.tokens = TheTable.tokens[::-1]

    def spectate(self, last_player):
        if 'Human' not in str(self.get_from):
            print(last_player, 'played', self.next_move)
            TheTable.draw_board()
            input()

    def play_game(self):
        """ 1) IDs next player via first sorted token
            2) Calls that player's main(), they hand move to ref
            3) Ref writes move to board
            4) Clears the move from valid list
            5) Opt spectator mode
            6) Flips tokens (remember, first token is always next player)"""
        next_player = TheTable.tokens[0]
        self.next_move = self.get_from[next_player].main()
        TheTable.the_board[self.next_move] = next_player
        TheTable.valid_moves.remove(self.next_move)
        if self.no_human:
            self.spectate(next_player)
        TheTable.tokens = TheTable.tokens[::-1]

    def game_over(self):
        def game_tied():
            full = ' ' not in list(TheTable.the_board.values())
            if full:
                self.results = "Game Tied"
            return full
        def game_won():  # Tokens already flipped. checks if prev player won game
            won = TheTable.is_won(TheTable.the_board, TheTable.tokens[1])
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
