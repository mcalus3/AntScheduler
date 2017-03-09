import random
import logging

logger = logging.getLogger("AntScheduler.Ant")


class Ant:
    """Class representing one cycle of iteration and the result_permutation of this cycle"""

    def __init__(self, _start_node):
        self.visited_list = [_start_node]
        self.visibility_list = []
        self.result_value = None
        self.visibility_list_update()

    def result_generate(self):
        while self.visibility_list:
            next_node = self.next_node_calculate()
            self.ant_move(next_node)
        self.result_value = result_value_calculate_as_makespan(self.visited_list)

    def next_node_calculate(self):
        pheromones_dict = self.visited_list[-1].pheromones_get(self.visibility_list)
        next_node = weighted_choice_sub(pheromones_dict)
        return next_node

    def ant_move(self, _next_node):
        self.visited_list.append(_next_node)
        self.visibility_list.remove(_next_node)
        self.visibility_list_update()

    def visibility_list_update(self):
        """to add a successor to visibility list you have to check if all it's predecessors are already visited"""
        for successor in self.visited_list[-1].successor_list:
            if set(successor.predecessor_list).issubset(self.visited_list):
                self.visibility_list.append(successor)


def weighted_choice_sub(_dict):
    """Optimized weighted choice function. For further optimization, iterate through sorted list (descending)"""
    rnd = random.random() * sum(_dict.values())
    for i, w in enumerate(_dict):
        rnd -= _dict[w]
        if rnd < 0:
            return w


def result_value_calculate_as_makespan(_operations):
    """Function that makes the schedule given the processes order. Returns the makespan. Roughly optimized"""

    for i, operation in enumerate(_operations):
        # TODO: bad-looking list split (get the i-th and previous ones)
        machine_unload_time = get_machine_unload_time(_operations[:i+1])
        if operation.predecessor_list:
            predecessor_end_times = [predecessor.start_time + predecessor.time_value for predecessor in
                                     operation.predecessor_list]
        else:
            predecessor_end_times = [0]
        operation.start_time = max([machine_unload_time] + predecessor_end_times)
    return _operations[-1].start_time + _operations[-1].time_value


def get_machine_unload_time(_operations):
    """Function used only by the result_value_calculate_as_makespan"""
    for operation in reversed(_operations[:-1]):
        if operation.type == _operations[-1].type:
            return operation.start_time + operation.time_value
    return 0
