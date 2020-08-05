# Tic Tac Toe
# The Table, The Players, and The Ref

# todo Recursive overhaul (still reliant on immediate win-check)
# todo touchups, see sub todo's
# todo General cleanup/polish


from random import choice
from time import sleep
from typing import * # todo type hints


class _TheTable:
    """The Table, central storage for all game elements and static
    functions for player/ref use
    Fully managed by The Referee"""
    # todo table will eventually have non-static functions. rewrite

    tokens: Tuple[str, str] = ('X', 'O')
    # Ref references tokens before initializing table

    def __init__(self):

        self.valid_moves: List[int] = []
        """All currently valid moves"""

        self.the_board: Dict[int, str] = {}
        for x in range(1, 10):
            self.the_board[x] = ' '
            self.valid_moves.append(x)

        self.next_token: str = self.tokens[0]
        # todo at current, next player is tokens[0], with list flipped after each turn.
        # todo create stand alone ***Done

    def set_table(self):
        raise Exception("Table should be set via init, not cust func")
        # todo test, prepare to work with global table obj ***Moved to init


    def place_token(self):
        # todo
        """No validity check, places token on and flips var next_token"""

    def is_move_valid(self, move):
        return move in self.valid_moves

    def draw_board(self):
        b = self.the_board
        print(f' {b[7]} | {b[8]} | {b[9]} ')
        print(f'---+---+---')
        print(f' {b[4]} | {b[5]} | {b[6]} ')
        print(f'---+---+---')
        print(f' {b[1]} | {b[2]} | {b[3]} ')

    @staticmethod
    def is_won(board: dict, check: str):
        """
        Static method used to check if a given board wins
        Because this points to no board default, can be used by playing
        board or by an AI's working board

        Args:
            board: a given board of tic tac toe
            check:

        Returns:

        """
        b = board
        c = check
        return (  # Boolean borrowed from nostarch.com/automatestuff
               (b[7] == c and b[8] == c and b[9] == c) or  # top
               (b[4] == c and b[5] == c and b[6] == c) or  # mid
               (b[1] == c and b[2] == c and b[3] == c) or  # low
               (b[7] == c and b[4] == c and b[1] == c) or  # left
               (b[8] == c and b[5] == c and b[2] == c) or  # cen
               (b[9] == c and b[6] == c and b[3] == c) or  # right
               (b[7] == c and b[5] == c and b[3] == c) or  # TL BR \
               (b[9] == c and b[5] == c and b[1] == c))    # TR BL /


# -----------------------------------------------------------------------------


class Character:
    """TheRef calls appropriate player's main() to return final_move
    Each player determines move in unique methods"""
    # todo standardize determine_move function

    _char_type = 'NON-IMPLEMENTED'
    table: _TheTable
    name: str
    token: str
    call_string: str

    def get_move_to_make(self) -> int:
        raise Exception("Called Player is not implemented")


# -----------------------------------------------------------------------------


class Human(Character):
    """Human Prompt for Tic-Tac-Toe.
    Draws board, quick input validation"""

    _char_type = 'Human'

    def __init__(self, table: _TheTable, token: str):
        self.table = table
        self.token = token
        self.name = self.get_name()
        self.call_string = f"{self.token} {self.name}, select your move"

    # todo get player character name, prompt
    def get_name(self) -> str:
        return input(f"what is your name, player {self.token}? > ")

    def get_move_to_make(self):
        self.table.draw_board()  # todo player should not draw board
        print(self.call_string)

        player_choice: int = 0
        while not self.table.is_move_valid(player_choice):
            player_choice = int(input("> "))

        return player_choice


class AiRando(Character):
    """Rando plays random moves till his final days"""

    _char_type = 'AiRando'

    def __init__(self, table: _TheTable, token: str):
        self.table = table
        self.token = token
        self.call_string = f"{self._char_type} {self.token} is choosing..."

    def get_move_to_make(self):
        sleep(1)  # simulates the effect of 'choosing'
        return choice(self.table.valid_moves)


class AiLevi(Character):
    """Opens random, recognizes winning moves
    Levi checks for immediate winning moves, otherwise plays random
    """

    _char_type = 'AiLevi'

    def __init__(self, table: _TheTable, token: str, final_move=None):
        # todo does Levi need init arg final move?
        self.final_move = final_move


    def win_check(self):
        # Play winning moves, or block opponent ones
        for token in self.table.tokens:
            for move in self.table.valid_moves:
                work = self.table.the_board.copy()
                work[move] = token
                if self.table.is_won(work, token):
                    return move
        # Otherwise, play random
        return choice(self.table.valid_moves)

    def levi(self):
        self.final_move = self.levi()
        
    def get_move_to_make(self):
        self.levi()
        return self.final_move


class AiRalph(Character):
    # todo consider broken until rewrite
    """Recursive Ralph
    Uses immediate check, then uses recursive analysis to find preferable positions

    prepare() copies info from The Table to reduce cross class pulls, preps score dict
    Win_check() identifies next move victories or defeats
    recur() uses recursion to score every condition 6 moves ahead in the game
    score_check() finds the highest or lowest score (+/-) and plays it.
        Random tie breaker if scores identical (i.e. symmetrical corners)
    ralph() uses win_check to identify immediacy, otherwise uses recur
    """

    _char_type = 'AiRalph'

    def __init__(self, scores=None, players=None, clone_board=None,
                 final_move=None):
        super().__init__()
        self.scores = scores
        self.players = players
        self.clone_board = clone_board
        self.final_move = final_move


    def prepare(self):
        self.scores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        # self.scores = {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0), 5: (0, 0),
        # 6: (0, 0), 7: (0, 0), 8: (0, 0), 9: (0, 0)}
        self.players = self.table.tokens.copy()
        self.clone_board = self.table.the_board.copy()

    def win_check(self):
        for token in self.players:
            for move in self.table.valid_moves:
                work = self.clone_board.copy()
                work[move] = token
                if self.table.is_won(work, token):
                    return move

    def recur(self, board, tokens, depth, last):
        work = board.copy()
        if depth > 6:
            return False    # cuts quarter million games down to 75k, reducing move 9 counts
        elif self.table.is_won(work, self.players[0]):
            self.scores[last] += 10 - depth
        elif self.table.is_won(work, self.players[1]):
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
            return choice(self.table.valid_moves)

    def ralph(self):
        self.prepare()
        self.final_move = self.win_check()
        if not self.final_move:
            self.recur(self.table.the_board, self.players, 1, 0)
            self.final_move = self.score_check()

    def get_move_to_make(self):
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
    # todo this is not proper doc!

    # todo the ref contains board logic and operations.
    #  Move to board, allow ref to create global class

    def __init__(self):
        # Todo expand on use here
        self.table_playing: _TheTable = _TheTable()

        self.call_char: Dict[str, Character] = {}
        """Dictionary containing player objects assigned to tokens. 
        Use table.next_token to call"""
        self.call_char = self.get_new_call_char()
        # 'X': {player_object}, 'O': {player_object}

        self.next_move = None
        """player sourced move, queued for board write"""
        self.results = None
        """ Game over string """
        self.repeating = True
        """ Repeats game, set by play_again() """
        # todo rewrite to display board each time regardless of human mode
        # Draw board each time.
        self.no_human = False
        """ Flag set if no human player detected"""

        self.characters: dict = {
            0: Human,
            1: AiRando,
            2: AiLevi,
            3: AiRalph,
        }
        """dict of available players, to assign into call_player values"""

        self.characters_string: str = self.get_characters_string()
        """String used to display all available characters"""
        self.characters_select: List[str] \
            = [f'{k}' for k in self.characters.keys()]
        """List of keys from avail characters. User selects char to assign"""


    # -------------------------------------------------------------------------
    # Init/Reset functions
    # -------------------------------------------------------------------------

    def get_new_call_char(self) -> Dict[str, Character]:
        """Assign parent Character obj to token calls. Used to init/clear
        call_player"""
        # (Reference actual tokens. THis could allow 3 players?
        characters_dict = {}
        for token in _TheTable.tokens:
            characters_dict[token] = Character

        return characters_dict

    def get_characters_string(self) -> str:
        """"Builds string used to display playable characters"""
        characters_string = ''
        for key in self.characters.keys():
            characters_string += f'{key}: {self.characters[key]._char_type}'
            if key != len(self.characters) - 1:
                characters_string += ', '

        return characters_string

    # -------------------------------------------------------------------------
    # Play functions
    # -------------------------------------------------------------------------

    def setup_board(self):
        # todo move to Table *** DOne

        # todo this might be ok. Ref should keep player calls. Move to own func
        # clear old assigned players
        self.call_char = self.get_new_call_char()

        print(self.characters_string)
        for token in self.call_char.keys():
            # assign actual character to each token call in call_char
            # print(f"'{char}': (0) human, (1) Rando, (2) Levi, or (3) Ralph?")

            prompt = ''
            while prompt.strip() not in self.characters_select:
                prompt = input(f"'{token}' > ")
            self.call_char[token] = \
                self.characters[int(prompt)](self.table_playing, token)

        # todo first rebuild will be human only. Refactor how ref draws board
        # todo check spectate flag, rename no_human -> spectating
        # To spectate
        self.no_human = 'Human' not in str(self.call_char)
        # Random starting players
        # x goes first
        # if choice([0, 1]) == 0:
        #     TheTable.tokens = TheTable.tokens[::-1]

    def play_game(self):
        """ 1) IDs next player via first sorted token
            2) Calls that player's main(), they hand move to ref
            3) Ref writes move to board
            4) Clears the move from valid list
            5) Opt spectator mode
            6) Flips tokens (remember, first token is always next player)"""
        # todo these need to be separate functions!
        # next_player = self.table_playing.tokens[0]
        next_player = self.table_playing.next_token  # unneeded var?
        self.next_move = self.call_char[next_player].get_move_to_make()
        self.table_playing.the_board[self.next_move] = next_player
        self.table_playing.valid_moves.remove(self.next_move)
        if self.no_human:
            self.spectate(next_player)
        self.table_playing.tokens = self.table_playing.tokens[::-1]

    def get_next_move(self) -> int:
        """Call next player for their move"""
        if __name__ == '__main__':
            return self.call_char[self.table_playing.next_token]

    def spectate(self, last_player):
        # todo consider refactoring spectate into ref drawing board after
        #  every move
        print(last_player, 'played', self.next_move)
        self.table_playing.draw_board()
        # sleep(1)
        input()
        '''if 'Human' not in str(self.get_from):
            print(last_player, 'played', self.next_move)
            TheTable.draw_board()
            input()'''

    def game_over(self):
        # todo consider properties in TheTable
        #  todo (table knows if game is over, or won, but ref acts on it)
        def game_won():  # Tokens already flipped. checks if prev player won
            won = self.table_playing.is_won(self.table_playing.the_board, self.table_playing.tokens[1])
            if won:
                self.results = f"{self.table_playing.tokens[1]} wins"
            return won
        def game_tied():
            full = ' ' not in list(self.table_playing.the_board.values())
            if full:
                self.results = "Game Tied"
            return full
        return game_won() or game_tied()

    def play_again(self, prompt=''):
        self.table_playing.draw_board()
        print(self.results)
        while prompt not in '0 1'.split():
            prompt = input("\n(0) Quit \n(1) Play again \n> ")
        self.repeating = prompt == '1'

    def main(self):
        # todo good running loop. Consider moving play game features
        #  to separate functions, and calling in main loop
        while self.repeating:
            self.setup_board()
            while not self.game_over():
                self.play_game()
            self.play_again()


if __name__ == '__main__':
    ref = TheRef()
    ref.main()
