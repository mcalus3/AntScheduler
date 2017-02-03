class Result:
    """class represents permutation of nodes that creates result and the value of it"""

    def __init__(self, _nodes_list):
        self.operation_list = [Operation(node) for node in _nodes_list]
        self.value = None

    @staticmethod
    def operation_check_availability(waiting_list, running_list):
        for req in waiting_list[0].predecessor_list:
            if req.name in [op.name for op in running_list + waiting_list]:
                return False
        return True

    def value_generate_as_makespan(self):

        waiting_list = self.operation_list[:]
        running_list = []
        t = -1
        while True:
            # each loop is next time moment
            t += 1
            if waiting_list:
                while waiting_list[0].type not in [operation.type for operation in running_list]:
                    # try to run first operation in queue - if it is possible run it and check next
                    if self.operation_check_availability(waiting_list, running_list):
                        self.operation_list[-len(waiting_list)].start_time = t
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
            if not waiting_list and not running_list:
                # terminate the simulation
                makespan = t
                self.value = makespan
                return makespan


class Operation:
    """class represents operation on schedule"""

    def __init__(self, _node):
        self.name = _node.name
        self.type = _node.type
        self.time_left = _node.time_value
        self.time = _node.time_value
        self.start_time = 0
        self.predecessor_list = [Operation(node) for node in _node.predecessor_list]
