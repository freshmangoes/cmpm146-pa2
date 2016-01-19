
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log


num_nodes = 1000
explore_faction = 2

def traverse_nodes(node, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """

    child_values = node.child_nodes.values()
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
    # Hint: return leaf_node

def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    new_node = node
    if node.untried_actions != []:
        
        move = choice(node.untried_actions)
        state.apply_move(move)
        new_node = MCTSNode(node, move, state.legal_moves)
        node.child_nodes[move] = new_node
        node.untried_actions.remove(move)
    

    return new_node

    # Hint: return new_node


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    while not state.is_terminal():
        state.apply_move(choice(state.legal_moves))


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    
    while node:
        node.wins += won
        node.visits += 1
        node = node.parent
    


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
        v1 =  traverse_nodes(node, sampled_game, identity_of_bot)
        delta = expand_leaf(v1, sampled_game)
        rollout(sampled_game)
        result = 0
        if identity_of_bot == sampled_game.winner:
            result = 1
        backpropagate(delta, result)
        #print(root_node.tree_to_string(3))
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    #print(root_node.tree_to_string(3))
    return max(root_node.child_nodes.values(), key = lambda c: c.visits).parent_action
