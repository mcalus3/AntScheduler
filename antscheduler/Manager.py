"""
Application created for academic purposes. Application utilises different Ant Algorithms to resolve
Job-shop scheduling problem and generate a schedule for process given by the nodes list specified in input.

Copyright (C) 2016 Marek Calus. All Rights Reserved.

"""

import os
import csv
import sys
import logging
import UiForm
import ImagesApi
from Config import Config
from GraphNode import GraphNode
from AntAlgorithm import MaxMin
from AntAlgorithm import AntSystem
from PyQt5 import QtWidgets


logger = logging.getLogger("AntScheduler")


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
    """stores algorithm configuration data, does graph creation from data file and runs the algorithm"""

    global logger
    initialize_logger()

    def __init__(self, _config_file):
        self.config = Config(_config_file)
        graph = self.graph_create(self.config.graph_file)
        self.nodes_list = graph

    def graph_create(self, _graph_file):
        graph_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), _graph_file)
        nodes_list = []
        with open(graph_path, "r") as file_csv:
            csv_reader = csv.reader(file_csv)

            # read the static info about each node
            for row in csv_reader:
                if len(row) < 3:
                    logger.warning("Incorrect input, blank line in input file")
                    continue
                nodes_list.append(GraphNode(row[0], int(row[1]), int(row[2])))
            file_csv.seek(0)

            # read the dynamic info about each node (successors lists)
            for i, row in enumerate(csv_reader):
                if len(row) <= 3:
                    continue
                pre_list = row[3].split()
                predecessors = [node for node in nodes_list if node.name in pre_list]
                for predecessor in predecessors:
                    nodes_list[i].add_predecessor(predecessor)
                    predecessor.add_successor(nodes_list[i])

            # initialise pheromone edges
            for predecessor in nodes_list:
                nested_predecessors = [predecessor] + predecessor.return_nested_predecessors()
                for successor in nodes_list:
                    if successor not in nested_predecessors:
                        predecessor.pheromone_dict[successor] = self.config.init_pheromone_value

        return nodes_list

    def algorithm_run(self):

        if self.config.algorithm_type == "max_min":
            algorithm = MaxMin(self.config, self.nodes_list)
        elif self.config.algorithm_type == "ant_system":
            algorithm = AntSystem(self.config, self.nodes_list)
        else:
            return
        algorithm.run()

        logger.info("result_permutation history:")
        logger.info([ant.result_value for ant in algorithm.result_history])
        best_result = sorted(algorithm.result_history, key=lambda x: x.result_value)[0]
        logger.info("best path: {0}".format(best_result.result_value))
        logger.info(" -> ".join([operation.name for operation in best_result.visited_list]))
        schedule_image_create(best_result)


class UIManager(QtWidgets.QMainWindow, UiForm.Ui_MainWindow):
    """Handles the UI form input and output"""

    def __init__(self, manager, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.RunButton.clicked.connect(self.algorithm_run)
        self.manager = manager
    def closeEvent(self, event):

        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               "Are you sure to quit?", QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def algorithm_run(self):
        if self.manager.config.render_images:
            ImagesApi.draw_graph(self.manager.nodes_list)

        self.manager.algorithm_run()


class CLIManager:
    """Handles the CLI input and output"""

    def __init__(self):
        pass


def schedule_image_create(_ant):
    """TODO: to be replaced by the scheduler class with matplotlib graph creation"""
    _operations_list = _ant.visited_list
    _result = _ant.result_value
    schedule_str = ""
    machines = 0
    # Getting the machines number
    for op in _operations_list:
        if op.type > machines:
            machines = op.type

    for machine in range(1, machines + 1):
        schedule_str += "Machine " + str(machine)
        machine_operations = [operation for operation in _operations_list if operation.type == machine]
        t = 0
        # printing the schedule for current machine
        while machine_operations:
            if machine_operations[0].start_time == t:
                schedule_str += machine_operations[0].name[0] * machine_operations[0].time_value
                t += machine_operations[0].time_value
                machine_operations.pop(0)
            else:
                schedule_str += " "
                t += 1
        schedule_str += "\n"
    # printing the time axis
    schedule_str += "         "
    for n in range(int(_result / 10 + 1)):
        schedule_str += str(n) + "0        "
    schedule_str += str(_result)

    with open(os.path.join(render_path, "output_schedule.txt"), "w") as text_file:
        text_file.write(schedule_str)
