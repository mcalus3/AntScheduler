import logging
import Ant

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

    def graph_pheromone_clear(self):
        for node in self.nodes_list:
            node.pheromone_list = []

    def run(self):
        pass


class MaxMin(AntAlgorithm):
    """ Class containing Graph representing industrial process and method that runs Ant Colony Optimization on this
    graph"""

    def __init__(self, _config, _nodes_list):
        AntAlgorithm.__init__(self, _config, _nodes_list)

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

    def graph_pheromone_and_history_update(self):
        self.ant_population.sort(key=lambda x: x.result_value)
        self.result_history.append(self.ant_population[0])

        best_result = sorted(self.result_history, key=lambda x: x.result_value)[0]
        self.pheromone_trail_modify(best_result.visited_list, 1 + self.config.pheromone_potency, MULTIPLY)
        for i, ant in enumerate(self.ant_population):
            if i == self.config.max_min_ants_promoted:
                break
            value = (1 + self.config.pheromone_potency * (self.config.pheromone_distribution ** (i + 1)))
            self.pheromone_trail_modify(ant.visited_list, value, MULTIPLY)

    def run(self):

        for iteration in range(self.config.iterations):
            self.ant_population = [Ant.Ant(self.nodes_list[0]) for _ in range(int(self.config.ant_population))]

            for ant in self.ant_population:
                ant.result_generate()
                self.pheromone_trail_modify(ant.visited_list, self.config.evaporation_rate, MULTIPLY)
                self.pheromone_trail_modify(ant.visited_list, 1 - self.config.evaporation_rate, ADD)

            self.graph_pheromone_and_history_update()
            logger.info(
                "running iteration: {0}, best result_permutation is: {1}".format(iteration,
                                                                                 self.result_history[-1].result_value))


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
                    if _operation == MULTIPLY:
                        node[next_edge] *= _value
                    elif _operation == ADD:
                        node[next_edge] += _value

    def graph_pheromone_and_history_update(self):
        [ant.result.value_generate_as_makespan() for ant in self.ant_population]
        self.ant_population.sort(key=lambda x: x.result.value)
        self.result_history.append(self.ant_population[0])

        for current_ant in self.ant_population:
            modify_value = (self.ant_population[0].result.value / current_ant.result.value) ** 2
            modify_value *= self.config.pheromone_potency
            self.pheromone_trail_modify(current_ant.visited_list, modify_value, ADD)
        for node in self.nodes_list:
            for edge in node.pheromone_list:
                edge.multiply_pheromone(self.config.evaporation_rate)

    def run(self):

        for iteration in range(self.config.iterations):
            self.ant_population = [Ant(self.nodes_list[0]) for _ in range(int(self.config.ant_population))]

            for ant in self.ant_population:
                ant.result_generate()
                self.pheromone_trail_modify(ant.visited_list, self.config.evaporation_rate, MULTIPLY)
                self.pheromone_trail_modify(ant.visited_list, 1 - self.config.evaporation_rate, ADD)

            self.graph_pheromone_and_history_update()
            logger.info(
                "running iteration: {0}, best result_permutation is: {1}".format(iteration,
                                                                                 self.result_history[-1].result.value))
