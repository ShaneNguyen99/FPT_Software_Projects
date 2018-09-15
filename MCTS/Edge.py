'''
TODO: Figure out how to change the parameters from constructor.
'''

class Edge:
   def __init__(self, state, parent_state):
      '''
      Parameter: 
      state : the state that this edge will point to
      '''
      self.p_prob = 0 # to-Change
      self.visit_count = 0 # to-Change
      self.q_value = 0 # to-Change
      self.next_state = state
      self.parent_state = parent_state
      
   def set_parameters(self, p_prob, visit_count, q_value):
      '''
      Manually set parameters for the Edge
      This is used for debugging
      '''
      self.p_prob = p_prob
      self.visit_count = visit_count
      self.q_value = q_value