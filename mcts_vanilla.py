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


    # print("Node: " + str(node))
    # print("Child nodes: " + str(node.child_nodes))
    expand_leaf(node, state)

    result = MCTSNode(parent = node, parent_action = None, action_list = node.untried_actions)
    node.visits+=1
    # cn = node.child_nodes
    # while node.untried_actions == [] and node.child_nodes != []:
    #     if state.player_turn == identity:
    #         # Maximize bot's chances of winning
    #         result = max(node.child_nodes, key=lambda c:(cn[c].wins/cn[c].visits)+explore_faction
    #                                                     *sqrt(2*log(cn[c].parent.visits)/cn[c].visits))
    #     else:
    #         # Maximize bot's chance of losing if it's the other bot's turn
    #         result = max(node.child_nodes, key=lambda c:(1-(c.wins/c.visits)+explore_faction
    #                                                      *sqrt(2*log(cn[c].parent.visits)/cn[c].visits)))

    while node.untried_actions == [] and node.child_nodes != []:
        if state.player_turn == identity:
            result = max(node.child_nodes, key=lambda c:(c.wins/c.visits)+explore_faction
                         *sqrt(2*log(c.parent.visits)/c.visits))
        else:
            result = max(node.child_nodes, key=lambda c:(1-(c.wins/c.visits))+explore_faction
                         *sqrt(2*log(c.parent.visits)/c.visits))

    return result
    pass
    # Hint: return leaf_node


def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """

    # Make sure there are still actions to be taken
    if node.untried_actions != []:
        move = choice(node.untried_actions)
        state.apply_move(move)
        node.untried_actions.remove(move)
        new_node = MCTSNode(parent = node, parent_action = move, action_list = node.untried_actions)
        node.child_nodes.update({move: new_node})
        # print("New child_nodes: " + str(node.child_nodes))
        return new_node
    pass
    # Hint: return new_node


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    while state.legal_moves() != []:
        state.apply_move(choice(state.legal_moves))
    pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    if won:
        node.parent.wins+=1
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
        root_node.visits = 1
        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        # Selection
        v1 = traverse_nodes(node, sampled_game, identity_of_bot)
        # # Expansion
        delta = expand_leaf(node, sampled_game)
        # # Simulation
        # rollout(sampled_game)
        # # Backpropogation
        # backpropagate(v1, delta)

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return
