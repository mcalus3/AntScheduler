class PheromoneEdge:
    """ Class representing pheromone edges"""

    def __init__(self, _successor, _value=1):
        self.value = _value
        self.successor = _successor

    def add_pheromone(self, _value):
        self.value += _value

    def multiply_pheromone(self, _value):
        self.value *= _value
