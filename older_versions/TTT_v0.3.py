# Tic Tac Toe
# The Arena, WiP
# Players return int 1-9

import random


class Human(object):
    """Human Prompt for Tic Tac Toe. Requires passed board and tokens
    Human has no access to board, same class can be reused by both players (Tokens handled by TheArena)

    draw_Board() displays passed board in readable format
    get_valids() creates a list of available moves (TheArena will handle invalid moves...consider phasing out)
    get_prompt() handles input"""
    def __init__(self, board, tokens, valids=None, move=None):
        self.board = board
        self.tokens = tokens
        self.valids = valids
        self.move = move

    def draw_board(self):
        b = self.board
        print(f' {b[7]} | {b[8]} | {b[9]} ')
        print(f'---+---+---')
        print(f' {b[4]} | {b[5]} | {b[6]} ')
        print(f'---+---+---')
        print(f' {b[1]} | {b[2]} | {b[3]} ')

    def get_valids(self):
        self.valids = []
        for key, val in self.board.items():
            if val == ' ':
                self.valids.append(key)

    def get_prompt(self):
        token = self.tokens[0]
        prompt = None
        print(f"{token}, select your move")
        while prompt not in '1 2 3 4 5 6 7 8 9'.split() or int(prompt) not in self.valids:
            prompt = input("> ")
        self.move = int(prompt)

    def main(self):
        self.draw_board()
        self.get_valids()
        self.get_prompt()
        return self.move
# -------------------------------------------------------------------------------------------------------


class AIRando(object):
    def __init__(self, board, tokens, valids=None, final_move=None):
        self.board = board
        self.tokens = tokens
        self.valids = valids
        self.final_move = final_move

    def gen_valids(self):
        pass
        self.valids = []
        for key, val in self.board.items():
            if val == ' ':
                self.valids.append(key)

    def rando_cal(self):
        pass
        self.final_move = random.choice(self.valids)

    def main(self):
        pass
        self.gen_valids()
        self.rando_cal()
        return self.final_move
# -------------------------------------------------------------------------------------------------------


class AILev1(object):
    def __init__(self, board, tokens, work=None, valids=None, foes=None, owns=None, final_move=None):
        self.board = board
        self.tokens = tokens
        self.work = work
        self.valids = valids
        self.foes = foes
        self.owns = owns
        self.final_move = final_move

    def clone(self):    # Creates clone of board for self.work. AI mutates board in certain checks
        self.work = self.board.copy()

    def gen_valids(self):
        self.valids = []
        for key, val in self.board.items():
            if val == ' ':
                self.valids.append(key)
            # elif val == self.tokens[1]:
            #     self.foes.append(key)
            # else:
            #     self.owns.append(key)

    # def copy_board(self):
    #     self.work = self.board.copy()

    def will_win(self, board, key):  # Boolean sourced nostarch.com/automatestuff
        b = board
        t = self.tokens[key]
        return ((b[7] == t and b[8] == t and b[9] == t) or  # top
                (b[4] == t and b[5] == t and b[6] == t) or  # mid
                (b[1] == t and b[2] == t and b[3] == t) or  # low
                (b[7] == t and b[4] == t and b[1] == t) or  # left
                (b[8] == t and b[5] == t and b[2] == t) or  # cen
                (b[9] == t and b[6] == t and b[3] == t) or  # right
                (b[7] == t and b[5] == t and b[3] == t) or  # TL BR \
                (b[9] == t and b[5] == t and b[1] == t))    # TR BL /

    def opposite_corner(self, check):
        corners = [1, 3, 7, 9]
        inv = corners.index(check)
        return self.board[corners[::-1][inv]] # ***

    def single_move(self):
        # Win/Block     # Token 0 (Player) win check, token 1 (Opponent) win check
        for x in range(2):
            self.work = self.board.copy()
            for move in self.valids:
                self.work[move] = self.tokens[x]
                if self.will_win(self.work, x):
                    return move
                    # self.final_move = move
                self.work = self.board.copy()
        #for move in valids:
            #self.clone()


        # for token in self.tokens:
        #     for move in self.valids:
        #         self.work[move] = token
        #         if self.won(token):
        #             self.final_move = move
        #         self.board.copy()

            # for moves in [self.foes, self.owns]:
                # for move in moves:
                #     for move in self.valids:
                #         self.work = self.board.copy()
                #         self.work[move] = player
                #         if self.won(player):
                #             self.final_move = move

    def corner_contingency(self):
            # Block opposing corners, claim opposite corner
        for token in self.tokens[::-1]:
            for move in self.valids:
                if move in [1, 3, 7, 9]:
                    if self.opposite_corner(move) == token:
                        return move

        # for moves in [self.foes, self.owns]:
            # for move in moves:
                # if move in [1, 3, 7, 9]:
                    # opposing = self.opposite_corner(move)
                    # if opposing == ' ':
                        # self.final_move = move

    def rng_corner(self):
        # Random corner
        valid_corners = []
        for move in self.valids:
            if move in [1, 3, 7, 9]:
                valid_corners.append(move)
        return random.choice(valid_corners)

    def finals(self):
        # Center
        if 5 in self.valids:
            return 5
        # Final Edges
        else:
            return random.choice(self.valids)

    def runnings(self):
        self.final_move = self.single_move()
        if self.final_move is None:
            self.final_move = self.corner_contingency()
        if self.final_move is None:
            self.final_move = self.rng_corner()
        if self.final_move is None:
            self.final_move = self.finals()

    def main(self):
        self.gen_valids()
        self.runnings()
        # print(self.board)
        # self.single_move()
        return self.final_move
# -------------------------------------------------------------------------------------------------------


class TheArena(object):
    """The Arena. Stores game state, rules, and player calls separate from players

    the_setup() Sets Arena's board and player types. Randomizes first player
    the_cook() clones board, uses the_call to get player move
    the_call() Recursive move validation from queued player (Human has verification already. Remove?)
    the_check() checks for terminal states, queues next player's turn
    """
    def __init__(self,
                 board=None, valids=None, clone=None, players=None,
                 move=None, tokens=None, results=None, again=True):
        self.board = board          # {1 thru 9: (' ' or 'X' or 'O')}
        self.valids = valids        # list of board keys where val=' '
        self.clone = clone          # cloned board to send (Note: secure or redundant?)
        self.players = players      # {'X': {player_function}, 'O': {player_function}}
        self.move = move            # next queued move to write to board
        self.tokens = tokens        # [0]=next player. the_setup randomizes, the_check flips
        self.tokens = ['X', 'O']
        self.results = results
        self.again = again

    def human(self):  # Sends move request to human
        go = Human(self.clone, self.tokens)
        self.move = go.main()
        # self.move = int(input("rough prompt> "))
        # go_catch = go.main()
        # pass
        # cloned = self.clone
        # print(f'{cloned} will send to queued human')

    def ai_levi(self):  # Sends move request to ai
        go = AILev1(self.clone, self.tokens)
        self.move = go.main()
        # pass
        # cloned = self.clone
        # print(f'{cloned} will send to queued AI')

    def ai_rando(self):
        go = AIRando(self.clone, self.tokens)
        self.move = go.main()

    def the_setup(self):

        self.board = {}
        for x in range(1, 10):
            self.board[x] = ' '

        self.valids = []
        for key, val in self.board.items():
            if val == ' ':
                self.valids.append(key)

        self.players = {'X': ' ', 'O': ' '}  # Preserves token to player call
        assignments = [self.human, self.ai_levi, self.ai_rando]
        for i in self.players.keys():
            work = i
            print(f"Will '{work}' be (0) human, (1) Levi, or (2) Rando?")
            prompt = ''
            while prompt not in '0 1 2'.split():
                prompt = input("> ")
            self.players[work] = assignments[int(prompt)]

        if random.choice([0, 1]) == 0:
            self.tokens = self.tokens[::-1]

    def draw_board(self):
        b = self.board
        print(f' {b[7]} | {b[8]} | {b[9]} ')
        print(f'---+---+---')
        print(f' {b[4]} | {b[5]} | {b[6]} ')
        print(f'---+---+---')
        print(f' {b[1]} | {b[2]} | {b[3]} ')

    def spectating(self):
        return 'player_human' not in self.players.values()  # Will trigger spectate if no humans. Allows AI levels
        # return self.players['X'] == self.player_ai and self.players['O'] == self.player_ai

    def the_call(self):  # Copy, send to next_player
        # self.clone = self.board.copy()
        # self.move = self.players[self.tokens[0]]()
        # check = self.players[self.tokens[0]]()
        # self.players[self.tokens[0]]()
        # print(self.players[self.tokens[0]], "'s move:", self.move, "check: ", check)
        # if self.move not in self.valids:
        #    self.the_call()
        # self.clone = self.board.copy()
        # queued = self.tokens[0]
        # call = self.players[queued]
        # self.move = call(self.clone)
        pass

    def the_cook(self):     # Move validation, writes to board (token = tokens[0])
                            # Clones self.board, to prevent shared memory location
                            # Calls function stored in players (Writes move to self.move)
                            #  Writes self.move to board
        # print(self.board)
        self.clone = self.board.copy()
        self.players[self.tokens[0]]()
        self.board[self.move] = self.tokens[0]
        self.tokens = self.tokens[::-1]
        if self.spectating():
            print('spectating')
            self.draw_board()
            input()

        # self.clone = self.board.copy()
        # queued = self.tokens[0]
        # call = self.players[queued]
        # elf.move = call(self.clone)
        # if self.move not in self.valids:
        # the_copy(self.clone, call]

    def the_results(self):
        self.draw_board()
        print(self.results)

    def is_full(self):
        full = ' ' not in list(self.board.values())
        if full:
            self.results = "Game Tied"
            return True
        else:
            return False

    def is_won(self):   # Boolean sourced nostarch.com/automatestuff
        b = self.board
        x = self.tokens[1]  # catch has already flipped tokens at this point
        won = ((b[7] == x and b[8] == x and b[9] == x) or  # top
               (b[4] == x and b[5] == x and b[6] == x) or  # mid
               (b[1] == x and b[2] == x and b[3] == x) or  # low
               (b[7] == x and b[4] == x and b[1] == x) or  # left
               (b[8] == x and b[5] == x and b[2] == x) or  # cen
               (b[9] == x and b[6] == x and b[3] == x) or  # right
               (b[7] == x and b[5] == x and b[3] == x) or  # TL BR \
               (b[9] == x and b[5] == x and b[1] == x))    # TR BL /
        if won:
            self.results = f"{x} wins"
            return True
        else:
            return False

    def game_over(self):
        return self.is_won() or self.is_full()

    def play_again(self):
        prompt = ''
        while prompt not in ['0', '1']:
            prompt = input("\n(0) Quit \n(1) Play again \n> ")
            if prompt == '0':
                self.again = False

    def main(self):
        while self.again:
            self.the_setup()
            while not self.game_over():
                self.the_cook()
            self.the_results()
            self.play_again()


play = TheArena()
if __name__ == '__main__':
    play.main()
