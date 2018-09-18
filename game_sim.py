"""Template for simulating games.

"""

import random as rand
import sys

DEFAULT_PROMPT = '> '


class Game:
    """
    Base class for games.

    Games should extend this class and and implement their own rules
    to advance the state. Classes have a set number of and advance when
    the current player returns an action.
    """
    def __init__(self, state=None, options=None):
        """Initializes the game.

        This method should not be overriden. The setup of the game
        state should be specified in reset_game, which this function
        calls.
        """
        if options:
            for opt in options:
                self._update_options(opt)
        if state:
            self.reset_game(state)
        self.game_over = False

    def _update_options(self, option):
        """Updates the options for the game state.

        This general form allows for an arbitrary number of inputs for
        the game, but they should be named entries in the form of 2-ples
        where the first entry is a string determining the option, and
        the second is value for that option.
        """
        setattr(self, option[0], option[1])

    def reset_game(self):
        """Resets the game.

        This is the initialization method for the game. The constructor
        should not be overridden, rather this method should be written
        specific for the game. This is called after the options are set,
        so it should respect the options when setting up the game. It is
        also important to set self.game_over to be False in this method.
        """
        self.players = [Player()]
        self._scores = [0]
        self._current_player_id = 0
        self.game_over = False

    def step(self):
        """Advances the game 1 turn.

        This is should be written to be as atomic as possible.
        """
        if self.game_over:
            return
        possible_actions = ActionList(["0", "1"])
        act = self.players[self._current_player_id].get_action(
            possible_actions)
        if act == "1":
            self.game_over = True

    def get_full_state(self):
        raise NotImplementedError("Text representation of full state \
            not implemented for this game.")

    def get_player_state(self, player_id):
        return self._scores[player_id]

    def get_player_reward(self, player_id):
        return self._scores[player_id]

    #TODO: add save and load functions


class ActionList:
    """Representation of the list of possible actions.

    This is the base class for a list of possible actions. By
    default, each action is represented by a string. This can also
    serve as a template for action lists that require a more complex
    representation.
    """
    def __init__(self, actions):
        self._actions = actions

    def __str__(self):
        return str(self._actions)

    def get_random_action(self):
        return rand.choice(self._actions)

    def isValid(self, input_str):
        return input_str in self._actions


class Player:
    def __init__(self):
        pass

    def get_action(self, possible):
        return possible.get_random_action()


class CLI_Player(Player):
    def __init__(self, ostream=sys.stdout, istream=sys.stdin):
        self.out = ostream.write
        self.input = sys.stdin  #TODO: enable reading from filestream

    def get_action(self, possible):
        self.out(possible)
        self.out("Select an action: ")
        inp = input()
        while not possible.isValid(inp):
            self.out("Not a valid action!")
            self.out(possible)
            self.out("Select an action: ")
            inp = input()
        return inp
