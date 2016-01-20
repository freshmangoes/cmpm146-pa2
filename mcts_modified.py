
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.


def traverse_nodes(node, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """

    child_values = node.child_nodes.values()
    # Checking to make sure there are no untried actions
    # and there are still child nodes left
    while node.untried_actions == [] and len(child_values) != 0:
        if state.player_turn == identity:
            # Maximize bot's chances of winning
            node = max(child_values, key=lambda c:(c.wins/c.visits)
                                    + explore_faction*sqrt(2*log(c.parent.visits)/c.visits))
        else:
            # Maximize bot's chance of losing
            node = max(child_values, key=lambda c:(1-(c.wins/c.visits)
                                    + explore_faction*sqrt(2*log(c.parent.visits)/c.visits)))
        state.apply_move(node.parent_action)
        child_values = node.child_nodes.values()
    return node

    pass
    # Hint: return leaf_node


def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    new_node = node
    # Checking to make sure there are still untried actions
    if node.untried_actions:
        # Randomly choose untried action
        move = choice(node.untried_actions)
        # Apply the move to the game state
        state.apply_move(move)
        # Make a new node with the move and the game state
        new_node = MCTSNode(node, move, state.legal_moves)
        # Append the new node to the tree
        node.child_nodes[move] = new_node
        # Remove the action from the list of untried actions
        node.untried_actions.remove(move)
    return new_node
    pass
    # Hint: return new_node


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    # Checking to make sure there are still moves left
    while not state.is_terminal():
        # Choose a random move
        state.apply_move(choice(state.legal_moves))
    pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """

    while node:
        # Increment the number of wins if the bot won
        node.wins += won
        # Increment the number of visits
        node.visits += 1
        # Trace back on the tree
        node = node.parent
    pass


def think(state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = state.player_turn
    root_node = MCTSNode(parent=None, parent_action=None, action_list=state.legal_moves)

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state.copy()
        # Start at root
        node = root_node
        # Do MCTS - This is all you!
        # Select
        v1 =  traverse_nodes(node, sampled_game, identity_of_bot)
        # Expand
        delta = expand_leaf(v1, sampled_game)
        # Rollout
        rollout(sampled_game)
        # Iterator for backpropogate and win
        result = 0
        if identity_of_bot == sampled_game.winner:
            result = 1
        backpropagate(delta, result)

        # Debug statement to print entire tree
        #print(root_node.tree_to_string(3))

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate
    return max(root_node.child_nodes.values(), key = lambda c: c.visits).parent_action
