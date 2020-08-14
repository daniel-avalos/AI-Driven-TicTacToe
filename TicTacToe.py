# Tic Tac Toe
# The Table, The Players, and The Ref

# todo Recursive overhaul (still reliant on immediate win-check)
# todo touchups, see sub todo's
# todo General cleanup/polish


from random import choice
from time import sleep
from typing import *  # todo type hints


class TheTable:
    """The Table, central storage for all game elements and static
    functions for player/ref use
    Fully managed by The Referee"""
    # todo table will eventually have non-static functions. rewrite

    def __init__(self):

        self.the_board: Dict[int, str] = {}
        """Tic Tac Toe board, stored as 2D dict"""

        self.valid_moves: List[int] = []
        """All currently valid moves"""

        self.tokens_dict: Dict[int, str] = {
            0: 'X',
            1: 'O',
            # 2: 'T'
        }
        """Tokens dict used for tracking next player"""
        # Separate dict used fof tracking who's next, without having to search
        #  through the tuple each time

        self.tokens = tuple([x for x in self.tokens_dict.values()])
        self._build_table()
        # build board, create valid move set

    def _build_table(self):
        """Builds board to be played, creates valid"""
        for x in range(1, 10):
            self.the_board[x] = ' '
            self.valid_moves.append(x)

    def set_token(self, token: str, move: int) -> None:
        """Given a token and move int, place token onto board. Once placed,
        removes move from self.valid_moves. Raises Exception if invalid move
        or token passed

        Args:
            move: index of position to place token
            token: token to place
        """

        # Move and token validity check
        if move not in self.valid_moves:
            raise ValueError(f"{move} is not a valid move! Players need to "
                            f"validate!")
        if token not in self.tokens:
            raise ValueError(f"{token} is not a valid token! ...How did you "
                            f"do this")

        # Place token, remove from valid moves
        self.the_board[move] = token
        self.valid_moves.remove(move)

    def draw_board(self):
        """STdout current board status"""
        # todo if expanding players, expand board size. Cond based on token
        #  count?
        # todo better clarity on winning moves
        """
         X | O |-X-
        ---+---+---
         O |-X-| O 
        ---+---+---
        -X-| X | O 
        """

        b = self.the_board
        print(f' {b[7]} | {b[8]} | {b[9]} ')
        print(f'---+---+---')
        print(f' {b[4]} | {b[5]} | {b[6]} ')
        print(f'---+---+---')
        print(f' {b[1]} | {b[2]} | {b[3]} ')
        print()

    def is_won(self, board: dict = None) -> Tuple[bool, str]:
        """
        Win condition check. Defaults to checking live board, but can be
        passed a hypothetical board to check (Used by AIs when testing win
        conditionals or recurisve paths)

        Args:
            board: A board of tic tac toe to check. Defaults to current
                board, but can be passed a hypothetical board to check win
                conditions. Useful for AI running win conditional checks
        Returns: (game_won: bool, winner: str)
        """
        b = board
        if not b:
            b = self.the_board

        game_won = False
        winner = ''
        for t in self.tokens:
            game_won = (  # Boolean borrowed from nostarch.com/automatestuff
               (b[7] == t and b[8] == t and b[9] == t) or  # top
               (b[4] == t and b[5] == t and b[6] == t) or  # mid
               (b[1] == t and b[2] == t and b[3] == t) or  # low
               (b[7] == t and b[4] == t and b[1] == t) or  # left
               (b[8] == t and b[5] == t and b[2] == t) or  # cen
               (b[9] == t and b[6] == t and b[3] == t) or  # right
               (b[7] == t and b[5] == t and b[3] == t) or  # TL BR \
               (b[9] == t and b[5] == t and b[1] == t))    # TR BL /
            if game_won:
                winner = t
                return game_won, winner
        return game_won, winner


# -----------------------------------------------------------------------------


class Character:
    """TheRef calls appropriate player's main() to return final_move
    Each player determines move in unique methods"""
    # todo standardize determine_move function

    # todo do these need to be preinit?

    char_type: str = 'NON-IMPLEMENTED'
    """Type of character (human, AIRando, etc). Used to reference 
    character type before init"""

    def __init__(self, table: TheTable, token: str):
        """"""
        self.table = table
        """Pointer to active table"""
        self.token = token
        """Token character represents"""
        self.call_string: str = f"{self.char_type} {self.token} is thinking..."
        """String to display once called on by Ref"""

    def prompt_next_move(self) -> int:
        """Function to prompt character for next move

        Returns:
            int of move character wishes to make
        """
        print(self.call_string)
        return self._move_determination()

    def _move_determination(self) -> int:
        """Character specific move calculation"""
        raise Exception("Called Player is not implemented")


class Human(Character):
    """Human Prompt for Tic-Tac-Toe.
    Draws board, quick input validation"""
    char_type = 'Human'

    def __init__(self, table: TheTable, token: str):
        super().__init__(table, token)
        self.player_name = self._prompt_name()
        self.call_string = f"{self.token} {self.player_name}, select your move"

    # todo get player character name, prompt
    def _prompt_name(self) -> str:
        return input(f"what is your name, player {self.token}? > ")

    def _move_determination(self) -> int:
        player_choice: int = 0
        while player_choice not in self.table.valid_moves:
            try:
                player_choice = int(input("> "))
            except ValueError:
                player_choice = 0

        return player_choice


class AiRando(Character):
    """Rando plays random moves till his final days"""

    char_type = 'AiRando'

    def __init__(self, table: TheTable, token: str):
        super().__init__(table, token)
        self.table = table
        self.token = token
        self.call_string = f"{self.char_type} {self.token} is choosing..."

    def _move_determination(self) -> int:
        sleep(1)  # simulates the effect of 'choosing'
        return choice(self.table.valid_moves)


class AiLevi(Character):
    """Opens random, but can recognize winning moves. will play to either
    win the game or block opponent from winning"""

    char_type = 'AiLevi'

    def __init__(self, table: TheTable, token: str):
        # todo does Levi need init arg final move?
        super().__init__(table, token)
        self.final_move = 0

    def _win_check(self) -> int:
        """
        Checks each valid move for a win move, selects fist 'winning' move
        found (Either for victory or opponent block)
        Returns:
            Move as int
        """
        # Play winning moves, or block opponent ones
        for token in self.table.tokens:
            for move in self.table.valid_moves:
                work = self.table.the_board.copy()
                work[move] = token
                won, winner = self.table.is_won(board=work)
                if won:
                    # whatever the move was won the game. Play to win, or block
                    return move
        # Otherwise, play random
        return choice(self.table.valid_moves)

    def _move_determination(self) -> int:
        sleep(2)
        self.final_move = self._win_check()
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

    char_type = 'AiRalph'

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

    def prompt_next_move(self):
        self.ralph()
        return self.final_move


class TheCharacters:

    def __init__(self, table_playing: TheTable):
        # tokens: Tuple[str, str] = ('X', 'O')

        # todo was created for ref to gather players, unneeded?
        """Publicly accessible tokens tuple. Can be read before init"""
        # tokens needs to be accessable before init

        self.table_playing = table_playing
        """Pointer to table in play. AI needs to 'see' table for their own 
        calculations """

        self.characters: Dict[int, Type[Character]] = {
            0: Human,
            1: AiRando,
            2: AiLevi,
            3: AiRalph,
        }
        """dict of available players, to assign into call_player values"""

        # todo random choice to determine who goes first?
        # self._token_index_next: int = choice(self.characters.keys())
        self._token_next_index: int = 0
        """Tracks which player is up next"""

        self._token_deck_index: int = self._get_token_deck_index()
        """Tracks player is on deck after next player"""
        # todo at current, next player is tokens[0], with list flipped after
        #  each turn.
        # todo create stand alone ***Done

        self.call_char: Dict[str, Character] = self._get_new_characters()
        """Dictionary containing player objects assigned to tokens. 
        Use table.next_token to call"""

    @property
    def token_next(self) -> str:
        """Token of next player to make move"""
        return self.table_playing.tokens_dict[self._token_next_index]

    @property
    def _token_deck(self) -> str:
        """Token of who plays AFTER next player. Used to track player
        queue, especially in <2 player games"""
        return self.table_playing.tokens_dict[self._token_deck_index]

    def _set_tokens_next_deck(self):
        """After player has made their move, cycle next players"""
        token_deck_index_new = self._get_token_deck_index()
        self._token_next_index = self._token_deck_index
        self._token_deck_index = token_deck_index_new

    # todo explore next()
    def _get_token_deck_index(self) -> int:
        """Attempts to self._token_next_index + 1. If OOB, 0"""
        try:
            attempt_deck_index = self._token_deck_index + 1
            if self.table_playing.tokens_dict[attempt_deck_index]:
                return attempt_deck_index
        except KeyError:
            return 0
        except AttributeError:
            # New Game, deck is 1
            return 1

    def _get_new_characters(self):
        """Runs on Init, prompts human user to assign character to Tokens
        X/O"""
        characters_dict = {}

        print(self._get_characters_string())
        for token in self.table_playing.tokens:
            # User specifices character type assigned to token
            user_prompt = ''
            characters_available = [f'{k}' for k in self.characters.keys()]
            while user_prompt not in characters_available:
                user_prompt = input(f"'{token}' > ").strip()

            # init character type, assigning pointer to table and it's token
            characters_dict[token] = \
                self.characters[int(user_prompt)](self.table_playing, token)

        return characters_dict

    def _get_characters_string(self) -> str:
        """"Builds string used to display playable characters"""
        characters_string = ''
        for key in self.characters.keys():
            characters_string += f'{key}: {self.characters[key].char_type}'
            if key != len(self.characters) - 1:
                characters_string += ', '

        return characters_string

    def get_next_move(self) -> int:
        """Gets move from next queued player, moves through queue"""
        # todo migrate get_move(?) from Ref
        next_move = self.call_char[self.token_next].prompt_next_move()
        self._set_tokens_next_deck()
        return next_move


# -----------------------------------------------------------------------------

class GameOver(Exception):
    pass


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
        self.table_playing = TheTable()
        self.characters_playing = TheCharacters(self.table_playing)

        self.next_move = None
        """player sourced move, queued for board write"""

        self.results = None
        """ Game over string """

        self.repeating = True
        """ Repeats game, set by play_again() """

    # -------------------------------------------------------------------------
    # Play functions
    # -------------------------------------------------------------------------

    @property
    def get_next_player(self):
        """Get next player to make a move. Referenced from TheCharacters"""
        return self.characters_playing.token_next

    @property
    def get_next_player_move(self):
        """Get's next player's move"""
        return self.characters_playing.get_next_move()

    def set_move(self):
        """Give move and token to table, to place on board"""
        self.table_playing.set_token(self.get_next_player,
                                     self.get_next_player_move)

    def draw_board(self):
        self.table_playing.draw_board()

    def play_round(self):
        # OBjs already built. Play game
        self.draw_board()
        if self.game_over:
            raise GameOver
        self.set_move()

    @property
    def game_won(self) -> Tuple[bool, str]:
        """Pointer to self.table_playing.is_won()

        Returns:
            Boolean and Token of game winner
        """
        return self.table_playing.is_won()

    @property
    def game_tied(self) -> bool:
        """Checks for any valid moves left. If none, board is filled. """
        return len(self.table_playing.valid_moves) == 0

    @property
    def game_over(self) -> bool:
        won, winner = self.game_won
        tied = self.game_tied

        if won:
            self.results = f"\n***{winner} wins***\n"
        elif tied:
            self.results = "\n---Game Tied---\n"

        return won or tied

    def main(self):
        # todo good running loop. Consider moving play game features
        #  to separate functions, and calling in main loop

        while True:
            try:
                self.play_round()
            except GameOver:
                print(self.results)
                return


def play_again() -> bool:
    """"""
    prompt = ''
    print('(0) Quit')
    print('(1) Play again')
    while prompt not in ('0', '1'):
        prompt = input('> ')
    return prompt == '1'


if __name__ == '__main__':
    # Todo new ref each run
    repeating = True
    while repeating:
        ref = TheRef()
        ref.main()
        repeating = play_again()
