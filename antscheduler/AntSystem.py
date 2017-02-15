import logging
from Ant import Ant
from AntAlgorithm import AntAlgorithm
from AntAlgorithm import MathOp

logger = logging.getLogger("AntScheduler.AntSystem")


class AntSystem(AntAlgorithm):
    """ Class containing Graph representing industrial process and method that runs Ant Colony Optimization on this
    graph"""

    def __init__(self, _config, _nodes_list):
        AntAlgorithm.__init__(self, _config, _nodes_list)

    @staticmethod
    def pheromone_trail_modify(_trail, _value, _operation):

        for i, node in _trail:
            if i == len(_trail) - 1:
                break
            for edge in node.pheromone_dict:
                next_edge = next(_trail)
                if edge == next_edge:
                    if _operation == MathOp.MULTIPLY:
                        node[next_edge] *= _value
                    elif _operation == MathOp.ADD:
                        node[next_edge] += _value

    def graph_pheromone_and_history_update(self):
        [ant.result.value_generate_as_makespan() for ant in self.ant_population]
        self.ant_population.sort(key=lambda x: x.result.value)
        self.result_history.append(self.ant_population[0])

        for current_ant in self.ant_population:
            modify_value = (self.ant_population[0].result.value / current_ant.result.value) ** 2
            modify_value *= self.config.pheromone_potency
            self.pheromone_trail_modify(current_ant.visited_list, modify_value, MathOp.ADD)
        for node in self.nodes_list:
            for edge in node.pheromone_list:
                edge.multiply_pheromone(self.config.evaporation_rate)

    def run(self):

        for iteration in range(self.config.iterations):
            self.ant_population = [Ant(self.nodes_list[0]) for _ in range(int(self.config.ant_population))]

            for ant in self.ant_population:
                ant.result_generate()
                self.pheromone_trail_modify(ant.visited_list, self.config.evaporation_rate, MathOp.MULTIPLY)
                self.pheromone_trail_modify(ant.visited_list, 1 - self.config.evaporation_rate, MathOp.ADD)

            self.graph_pheromone_and_history_update()
            logger.info(
                "running iteration: {0}, best result_permutation is: {1}".format(iteration, self.result_history[-1].result.value))
