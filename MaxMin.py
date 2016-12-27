import logging
from Ant import Ant
from AntAlgorithm import AntAlgorithm
from AntAlgorithm import MathOp

logger = logging.getLogger("AntScheduler.MaxMin")


class MaxMin(AntAlgorithm):
    """ Class containing Graph representing industrial process and method that runs Ant Colony Optimization on this
    graph"""

    def __init__(self, _config, _nodes_list):
        AntAlgorithm.__init__(self, _config, _nodes_list)

    @staticmethod
    def pheromone_trail_modify(_trail, _value, _operation):

        for i, node in enumerate(_trail):
            if i == len(_trail) - 1:
                break
            for edge in node.pheromone_list:
                if edge.successor == _trail[i + 1]:
                    if _operation == MathOp.MULTIPLY:
                        edge.multiply_pheromone(_value)
                    elif _operation == MathOp.ADD:
                        edge.add_pheromone(_value)

    def graph_pheromone_and_history_update(self):
        [ant.result.value_generate_as_makespan() for ant in self.ant_population]
        self.ant_population.sort(key=lambda x: x.result.value)
        self.result_history.append(self.ant_population[0])

        best_result = sorted(self.result_history, key=lambda x: x.result.value)[0]
        self.pheromone_trail_modify(best_result.visited_list, 1 + self.config.pheromone_potency, MathOp.MULTIPLY)
        for i, ant in enumerate(self.ant_population):
            if i == self.config.max_min_ants_promoted:
                break
            value = (1 + self.config.pheromone_potency * (self.config.pheromone_distribution ** (i + 1)))
            self.pheromone_trail_modify(ant.visited_list, value, MathOp.MULTIPLY)

    def run(self):

        for iteration in xrange(self.config.iterations):
            self.ant_population = [Ant(self.nodes_list[0]) for _ in range(int(self.config.ant_population))]

            for ant in self.ant_population:
                ant.result_generate()
                self.pheromone_trail_modify(ant.visited_list, self.config.evaporation_rate, MathOp.MULTIPLY)
                self.pheromone_trail_modify(ant.visited_list, 1 - self.config.evaporation_rate, MathOp.ADD)

            self.graph_pheromone_and_history_update()
            logger.info(
                "running iteration: {0}, best result is: {1}".format(iteration, self.result_history[-1].result.value))
