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

    def visibility_list_update(self):
        """to add a successor to visibility list you have to check if all it's predecessors are already visited"""
        for successor in self.visited_list[-1].successor_list:
            if set(successor.predecessor_list).issubset(self.visited_list):
                self.visibility_list.append(successor)

    def ant_move(self, _next_node):
        self.visited_list.append(_next_node)
        self.visibility_list.remove(_next_node)
        self.visibility_list_update()

    def next_node_calculate(self):
        pheromones_dict = self.visited_list[-1].get_pheromones(self.visibility_list)
        next_node = weighted_choice_sub(pheromones_dict)
        return next_node

    def result_generate(self):
        while self.visibility_list:
            next_node = self.next_node_calculate()
            self.ant_move(next_node)
        self.result_value = result_value_calculate_as_makespan(self.visited_list)


def weighted_choice_sub(_dict):
    rnd = random.random() * sum(_dict.values())
    for i, w in enumerate(_dict):
        rnd -= _dict[w]
        if rnd < 0:
            return w

def result_value_calculate_as_makespan(_result_permutation):
    waiting_list = _result_permutation[:]
    running_list = []
    for node in waiting_list:
        node.time_left = node.time_value
    t = -1
    while True:
        # each loop is next time moment
        t += 1
        if waiting_list:
            while waiting_list[0].type not in [operation.type for operation in running_list]:
                # try to run first operation in queue - if it is possible run it and check next
                if operation_check_availability(waiting_list, running_list):
                    #TODO: Add missing data structures
                    running_list.append(waiting_list.pop(0))
                    if not waiting_list:
                        break
                else:
                    # if not, wait for next moment in time
                    break
        # delete completed operations from running list and decrease time left
        running_list = [operation for operation in running_list if operation.time_left > 1]
        for operation in running_list:
            operation.time_left -= 1
        if not (waiting_list or running_list):
            # terminate the simulation
            return t


def operation_check_availability(waiting_list, running_list):
    for req in waiting_list[0].predecessor_list:
        if req.name in [op.name for op in running_list + waiting_list]:
            return False
    return True
