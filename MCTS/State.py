from Env import *
'''
TODO: Figure out how to change the parameters from constructor.
'''

class State:
   def __init__(self, parent_edge):
      '''
      Parameter: 
      edges : a list of edges that this state will point to
      '''
      self.v = 0 # Change
      self.board = Env()
      self.edge_pointers = []
      self.parent_edge = parent_edge
      
   def set_parameters(self, v, board):
      '''
      Manually set parameters for the Edge
      This is used for debugging
      '''
      self.v = v
      self.board = board
