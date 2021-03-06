import logging
from Ant import Ant

logger = logging.getLogger("AntScheduler.MaxMin")
MULTIPLY = 0
ADD = 1


class AntAlgorithm:
    """ Class containing Graph representing industrial process and method that runs Ant Colony Optimization on this
    graph"""

    def __init__(self, _config, _nodes_list):
        self.config = _config
        self.nodes_list = _nodes_list
        self.ant_population = []
        self.result_history = []

    def run(self):
        pass

    def pheromone_init(self):
        for node in self.nodes_list:
            nested_predecessors = [node] + node.nested_predecessors()
            for successor in self.nodes_list:
                if successor not in nested_predecessors:
                    node.pheromone_dict[successor] = self.config.init_pheromone_value

    @staticmethod
    def pheromone_trail_modify(_trail, _value, _operation):
        iterator = iter(_trail)
        node = next(iterator)  # throws StopIteration if empty.
        for next_node in iterator:
            if _operation == MULTIPLY:
                node.pheromone_dict[next_node] *= _value
            elif _operation == ADD:
                node.pheromone_dict[next_node] += _value
            node = next_node


class MaxMin(AntAlgorithm):
    """ Class containing Graph representing industrial process and method that runs Ant Colony Optimization on this
    graph"""

    def __init__(self, _config, _nodes_list):
        AntAlgorithm.__init__(self, _config, _nodes_list)
        self.history_best = Ant(self.nodes_list[0])
        # TODO how to make arbitrary big max value?
        self.history_best.result_value = 100000

    def run(self):
        self.pheromone_init()
        for iteration in range(self.config.iterations):
            self.ant_population = [Ant(self.nodes_list[0]) for _ in range(self.config.ant_population)]
            for ant in self.ant_population:
                ant.result_generate()
                self.evaporate_pheromone_trail(ant)

            self.graph_update()
            logger.info(
                "running iteration: {0}, best result_permutation is: {1}".format(iteration,
                                                                                 self.result_history[-1].result_value))

    def graph_update(self):
        """In each iteration graph pheromone is being updated according to the best ants results"""
        self.ant_population.sort(key=lambda x: x.result_value)
        self.result_history.append(self.ant_population[0])
        self.history_best = min(self.history_best, self.ant_population[0], key=lambda x: x.result_value)
        self.prepare_and_modify_best_trails()

    def prepare_and_modify_best_trails(self):
        """Modify trail - once for history best result and once for couple of local best results"""
        self.pheromone_trail_modify(self.history_best.visited_list, 1 + self.config.pheromone_potency, MULTIPLY)
        for i in range(self.config.max_min_ants_promoted):
            value = (1 + self.config.pheromone_potency * (self.config.pheromone_distribution ** (i + 1)))
            self.pheromone_trail_modify(self.ant_population[i].visited_list, value, MULTIPLY)

    def evaporate_pheromone_trail(self, ant):
        """evaporate the pheromone, minimal value is 1"""
        self.pheromone_trail_modify(ant.visited_list, self.config.evaporation_rate, MULTIPLY)
        self.pheromone_trail_modify(ant.visited_list, 1 - self.config.evaporation_rate, ADD)


class AntSystem(AntAlgorithm):
    """ Class containing Graph representing industrial process and method that runs Ant Colony Optimization on this
    graph"""

    def __init__(self, _config, _nodes_list):
        AntAlgorithm.__init__(self, _config, _nodes_list)

    def graph_update(self):
        self.ant_population.sort(key=lambda x: x.result_value)
        self.result_history.append(self.ant_population[0])

        # Modify trail - once for history best result and once for couple of local best results
        for ant in self.ant_population:
            value = (1 / ant.result_value * ant_population[0].result_value * self.config.pheromone_potency)
            self.pheromone_trail_modify(self.ant.visited_list, value, ADD)

    def run(self):
        self.graph_pheromone_clear()
        for iteration in range(self.config.iterations):
            self.ant_population = [Ant(self.nodes_list[0]) for _ in range(self.config.ant_population)]
            for ant in self.ant_population:
                ant.result_generate()

            self.graph_update()
            logger.info(
                "running iteration: {0}, best result_permutation is: {1}".format(iteration,
                                                                                 self.result_history[-1].result_value))
