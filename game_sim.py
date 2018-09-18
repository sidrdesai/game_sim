"""Template for simulating games.

"""

import random as rand
import sys

DEFAULT_PROMPT = '> '


class Game:
    """
    Base class for games.

    Games should extend this class and and implement their own rules to advance
    the state. Classes have a set number of and advance when the current player
    returns an action.
    """
    def __init__(self, state=None, options=None):
        """Initializes the game.

        This method should not be overriden. The setup of the game state should
        be specified in reset_game, which this function calls.

        Args:
            state (dict): beginning game state if trying to start from a saved
                state
            options (dict): options to be set for the game (these may be
                overwritten if state is set
        """
        self.game_over = False
        if options:
            self.update_options(options)
        if state:
            self._load_state(state)
        else:
            self.reset_game()

    def update_options(self, options):
        """Updates the options for the game state.

        All the game options will be set as _opt_ followed by the name of the
        option. These options will be used when the game is reset. This method
        should be overridden to check that options are set to acceptable values
        for the game start.

        Args:
            options (dict): options to be set for the game
        """
        for name in options:
            setattr(self, "_opt_"+name, options[name])

    def reset_game(self):
        """Resets the game.

        This is the initialization method for the game. The constructor should
        not be overridden, rather this method should be written specific for
        the game. This is called after the options are set, so it should
        respect the options when setting up the game. It is also important to
        set self.game_over to be False in this method.
        """
        self.players = [Player()]
        self._scores = [0]
        self._current_player_id = 0
        self.game_over = False

    def step(self):
        """Advances the game 1 turn.

        This is should be written to be as atomic as possible. It should
        roughly equate to one "turn" in the game. The outer loop should run
        this function as long as game_over is False. The current player is
        asked to provide an action, and the current_player_id is changed if
        appropriate.
        """
        if self.game_over:
            return
        possible_actions = ActionList(["0", "1"])
        act = self.players[self._current_player_id].get_action(
            possible_actions)
        if act == "1":
            self.game_over = True

    def get_full_state(self):
        """This is used to get the full state of the game in text form.

        Players should access the game through the get_player_state method so
        some of the state information could be hidden. For games where this is
        not necessary, it may not be defined where it will throw an error if
        called.
        """
        raise NotImplementedError("Text representation of full state not\
            implemented for this game.")

    def get_player_state(self, player_id):
        """This returns a text representation of the state visible to a player.

        This is different from the full state becuase information might be
        hidden from some players in certain games.

        Args:
            player_id (int): The identiier for the player

        Returns:
            dict: state visible to player; by default, just the score
        """
        return {'score': self._scores[player_id]}

    def get_player_reward(self, player_id):
        """Returns a numerical value for the player's score.

        This is meant to be used for learning polcies for games. This is the
        current score or in other words, the cumulative rewards earned by the
        player.

        Args:
            player_id (int): The identifier for the player

        Returns:
            float: player score
        """
        return self._scores[player_id]

    def _load_state(self, state):
        """Loads state from a dictionary representation for state.

        Args:
            state (dict): previously saved state for game
        """
        for var in state:
            setattr(self, var, state[var])

    # TODO: add save and load from file functions


class ActionList:
    """Representation of the list of possible actions.

    This is the base class for a list of possible actions. By default, each
    action is represented by a string. This can also serve as a template for
    action lists that require a more complex representation.
    """
    def __init__(self, actions):
        """Initializes action list.

        By default this takes in and stores a list of strings.
        Args:
            actions (list): list of possible actions
        """
        self._actions = actions

    def __str__(self):
        """Shows possible actions in a human-readable way.

        This is used so a CLI player would know what commands are allowed. Not
        every game will have this, since the state might make it obvious. Thus,
        the default is the empty string.

        Returns:
            string: possible actions
        """
        return ""

    def get_random_action(self):
        """Returns a random action from a uniform distribution.

        The default player plays randomly. This function should sample from a
        uniform distribution ver the possible actions, but the behavior would
        be specific to each game.

        Returns:
            string: chosen action
        """
        return rand.choice(self._actions)

    def isValid(self, input_str):
        """Returns whether the user input is a valid action.

        Return:
            boolean: True if action is valid
        """
        return input_str in self._actions


class Player:
    """A human or AI agent that makes decisions in the game.

    The base player class just returns a random action. This class can be
    extended to be an interface for a human or it can follow some policy. This
    abstraction allows the game rules to ignore the nature of the player.
    """
    def __init__(self):
        pass

    def get_action(self, possible):
        """Returns an action from the player.

        By default, the player plays randomly.

        Args:
            possible (ActionList): a representation of the possible actions
        Returns:
            string: random action
        """
        return possible.get_random_action()


class CLI_Player(Player):
    """Command line interface player

    This is the class that interfaces with a human. To the game, it is the same
    no matter what kind of player is playing the game. This class prints to the
    terminal and gets user input as well as checking for valid inputs.
    """
    def __init__(self, ostream=sys.stdout):
        self.out = ostream.write
        self.input = sys.stdin  # TODO: enable reading from filestream

    def get_action(self, possible):
        """Returns an action inputted by a human.

        Interfaces with a human through the terminal, providing error checking.
        This terminates when the user inputs a valid action.

        Args:
            possible (ActionList): a representation of the possible actions

        Returns:
            string: chosen action
        """
        self.out(possible)
        self.out("Select an action: ")
        inp = input()
        while not possible.isValid(inp):
            self.out("Not a valid action!")
            self.out(possible)
            self.out("Select an action: ")
            inp = input()
        return inp
