from Edge import *
from State import *
import copy
import random
import math
''' Test code Not right anymore
root = State([Edge(None), Edge(None)])
root.edge_pointers[0].next_state = State([])
root.edge_pointers[1].next_state = State([Edge(State([])), Edge(State([]))])
root.edge_pointers[0].set_parameters(2, 2, 2)
root.edge_pointers[1].set_parameters(5, 5, 5)
root.edge_pointers[1].next_state.edge_pointers[0].set_parameters(6, 6, 6)
root.edge_pointers[1].next_state.edge_pointers[1].set_parameters(3, 3, 3)
'''

def main():
    root = State(None)
    root.board.reset()
    for i in range (1000000):
        leaf_node = select(root)
        expand(leaf_node)
    for edge in root.edge_pointers:
        print(edge.visit_count, edge.q_value)

def select(master_root):
    '''
    From the root of the tree, traverse using the greedy method to get to a leaf state
    Parameter: master_root : the root of the tree

    Return: a String representing a path to the leaf state (can be changed to get a reference to the state)
    '''
    state = master_root
    parent_visit_count = 1
    while(state is not None and len(state.edge_pointers) != 0):
        max_index = 0
        max_U = 0
        for index, edge in enumerate(state.edge_pointers):
            #U = edge.q_value/edge.visit_count + math.sqrt(math.log(parent_visit_count)/edge.visit_count)
            U = edge.q_value/edge.visit_count + math.sqrt(math.log(parent_visit_count)/edge.visit_count)
            if(U > max_U):
                max_U = U
                max_index = index
        parent_visit_count = state.edge_pointers[max_index].visit_count
        state = state.edge_pointers[max_index].next_state
    return state

def expand(node):
    '''
    From a leaf node, expand to all possible other nodes from the action set A.
    Parameter: node: a pointer to the leaf node

    Return:
    '''
    for move in sorted(node.board.legal_moves()):
        node.edge_pointers.append(Edge(State(None), node))
        node.edge_pointers[-1].next_state.parent_edge = node.edge_pointers[-1]
        node.edge_pointers[-1].next_state.board = copy.deepcopy(node.board)
        node.edge_pointers[-1].next_state.board.step(move)
        Q = simulate(node.edge_pointers[-1].next_state) # whether O has won or lost
        back_up(node.edge_pointers[-1], Q)

def simulate(node):
    '''
    Simulate using rollout policy to get to a game result

    Return: the Weight as final result
    '''
    board_copy = copy.deepcopy(node.board)
    while (not board_copy.done):
        board_copy.step(random.choice(board_copy.legal_moves()))
    q = 0
    if str(board_copy.winner) == 'Winner.O':
        q = 1
    elif str(board_copy.winner) == 'Winner.X':
        q = -1
    else:
        q = 0
    return q

def back_up(edge, Q):
    while(edge is not None):
        edge.visit_count += 1
        edge.q_value += Q
        edge = edge.parent_state.parent_edge



if __name__ == "__main__":
    main()