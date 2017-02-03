"""
Application created for academic purposes. Application utilises different Ant Algorithms to resolve
Job-shop scheduling problem and generate a schedule for process given by the nodes list specified in input.

Copyright (C) 2016 Marek Calus. All Rights Reserved.

"""

import os
import subprocess
import csv
import sys
import logging
import GVApi
from Config import Config as ConfigClass
from GraphNode import GraphNode
from MaxMin import MaxMin
from PheromoneEdge import PheromoneEdge
from AntSystem import AntSystem


logger = logging.getLogger("AntScheduler")
config_file = "config.ini"


def initialize_logger():

    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    console_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))

    logger.addHandler(console_handler)

    logger.debug("Logger initialized")
    return logger


class Manager:
    """handles input, output, configuration and graph creation, runs the algorithm and plots the schedule"""

    global logger
    initialize_logger()

    def __init__(self, _config_file):
        self.config = ConfigClass(_config_file)
        graph = self.graph_create(self.config.graph_file)
        self.nodes_list = graph

    @staticmethod
    def schedule_image_create(_result):
        """TODO: to be replaced by the scheduler class with matplotlib graph creation"""
        schedule_str = ""
        machines = 0
        # Getting the machines number
        for op in _result.operation_list:
            if op.type > machines:
                machines = op.type

        for machine in range(1, machines + 1):
            schedule_str += "Machine " + str(machine)
            machine_operations = [operation for operation in _result.operation_list if operation.type == machine]
            t = 0
            # printing the schedule for current machine
            while machine_operations:
                if machine_operations[0].start_time == t:
                    schedule_str += machine_operations[0].name[0] * machine_operations[0].time
                    t += machine_operations[0].time
                    machine_operations.pop(0)
                else:
                    schedule_str += " "
                    t += 1
            schedule_str += "\n"
        # printing the time axis
        schedule_str += "         "
        for n in range(int(_result.value / 10 + 1)):
            schedule_str += str(n) + "0        "
        schedule_str += str(_result.value)

        with open("output_schedule.txt", "w") as text_file:
            text_file.write(schedule_str)

    def graph_create(self, _graph_file):
        nodes_list = []
        with open(_graph_file, "r") as file_csv:
            csv_reader = csv.reader(file_csv)

            for row in csv_reader:
                if len(row) < 3:
                    logger.warning("Incorrect input, blank line in input file")
                    continue
                nodes_list.append(GraphNode(row[0], int(row[1]), int(row[2])))
            file_csv.seek(0)

            for i, row in enumerate(csv_reader):
                if len(row) <= 3:
                    continue
                pre_list = row[3].split()
                predecessors = [node for node in nodes_list if node.name in pre_list]

                for predecessor in predecessors:
                    nodes_list[i].add_predecessor(predecessor)
                    predecessor.add_successor(nodes_list[i])

                    # pheromone edges are initialised
            for predecessor in nodes_list:
                nested_predecessors = [predecessor] + predecessor.return_nested_predecessors()
                for successor in nodes_list:
                    if successor not in nested_predecessors:
                        predecessor.add_pheromone(PheromoneEdge(successor, self.config.init_pheromone_value))

        return nodes_list

    def algorithm_run(self):
        """TODO: replace with classes inheriting after algorithm class and overriding functions"""

        if self.config.algorithm_type == "max_min":
            algorithm = MaxMin(self.config, self.nodes_list)
        elif self.config.algorithm_type == "ant_system":
            algorithm = AntSystem(self.config, self.nodes_list)
        else:

            return

        algorithm.run()

        logger.info("result history:")
        logger.info([ant.result.value for ant in algorithm.result_history])
        best_result = sorted(algorithm.result_history, key=lambda x: x.result.value)[0]
        logger.info("best path: {0}".format(best_result.result.value))
        logger.info(" -> ".join([operation.name for operation in best_result.visited_list]))
        self.schedule_image_create(best_result.result)


def main():
    manager = Manager(config_file)
    GVApi.draw_graph(manager.nodes_list)
    manager.algorithm_run()


if __name__ == "__main__":
    main()
