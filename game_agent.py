"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import numpy
import math
# import logging


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # two factors: 1. the steps gap between two players and 2. the
    # distance for the center
    legal_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    if not legal_moves:
        return float("inf") if game.is_winner(player) else float("-inf")
    else :
        return len(opp_moves) * -1.0 / len(legal_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # Combine the evaluation of move steps and distance to the center
    legal_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    if not legal_moves:
        return float("inf") if game.is_winner(player) else float("-inf")
    else :
        w, h = game.width / 2., game.height / 2.
        y, x = game.get_player_location(player)
        return len(legal_moves) - len(opp_moves) + math.sqrt((h - y)**2 + (w - x)**2)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # use division the get the gap between the two players
    legal_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    if not legal_moves:
        return float("inf") if game.is_winner(player) else float("-inf")
    else :
        w, h = game.width / 2., game.height / 2.
        y, x = game.get_player_location(player)
        return len(legal_moves) - len(opp_moves) + float((h - y)**2 + (w - x)**2)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            print('time out!')  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        # Parameters: game g, current depth quota d and minimax index minmax
        # return min/max value of current state
        def get_value(g, d, minmax):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            # Determine whether the search reaches the depth limit or the terminal state
            local_moves = g.get_legal_moves()
            if not local_moves or d <= 0 :
                return self.score(g, self)

            # reduce the depth quota
            # if d == 2 :
            #     print('depth now: ', d, 'moves: ', len(local_moves))

            # Find the max/min value based on the minmax parameter or raise an error for invalid parameter
            if minmax == 'min':
                return min([get_value(g.forecast_move(move), d - 1, 'max') for move in local_moves])
            elif minmax == 'max':
                return max([get_value(g.forecast_move(move), d - 1, 'min') for move in local_moves])
            else:
                raise ValueError('invalid min/max parameter value')


        # return the best move
        legal_moves = game.get_legal_moves()

        # logger = logging.getLogger('minimaxPlayer')
        # logger.warning('depth: %s', depth.search_depth)
        # print('total depth: ', depth, 'Total moves : ', len(legal_moves))

        if not legal_moves:
            return (-1, -1)
        else:
            idx = numpy.argmax([get_value(game.forecast_move(move), depth - 1, 'min') for move in legal_moves])
            return legal_moves[idx]


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            d = 1
            while True:
                best_move = self.alphabeta(game, d)
                d = d + 1
        except SearchTimeout:
            return best_move  # return the last move if timeout

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        # raise NotImplementedError
        # Parameters: g from game, a for alpha, b for beta, d for depth and minmax for min/max index
        def ab_value(g, a, b, d, minmax):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            # Check whether the game state is terminal, i.e. no legal_moves
            local_moves = g.get_legal_moves()
            if not local_moves or d <= 0:
                return self.score(g, self)

            # Return the alpha/beta value based on the alpha/beta index minmax
            if minmax == 'min':
                v = float('inf')
                for move in local_moves:
                    v = min(v, ab_value(g.forecast_move(move), a, b, d - 1, 'max'))
                    if v <= a :
                        return v
                    b = min(v,b)
                return v
            elif minmax == 'max':
                v = float('-inf')
                for move in local_moves:
                    v = max(v, ab_value(g.forecast_move(move), a, b, d - 1, 'min'))
                    if v >= b :
                        return v
                    a = max(v,a)
                return v
            else:
                raise ValueError('Invalid alpha/beta index parameter value')

        # return the best move
        legal_moves = game.get_legal_moves()
        next_move = (-1, -1)
        if not legal_moves:
            return next_move
        else:
            # Prune from sub-tree
            max_v = float('-inf')
            for move in legal_moves:
                v = ab_value(game.forecast_move(move), alpha, beta, depth - 1, 'min')
                if max_v < v :
                    next_move = move
                    max_v = v
                if v >= beta :
                    return next_move
                alpha = max(max_v,alpha)
            return next_move
