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
import AntAlgorithm
from Config import Config
from GraphNode import GraphNode
from PyQt5 import QtWidgets


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
    """stores algorithm configuration data, does graph creation from data file and runs the algorithm"""

    global logger
    initialize_logger()

    def __init__(self):
        self.config = Config(config_file)
        graph = self.graph_create(self.config.graph_file)
        self.nodes_list = graph
        # TODO: Temoprary
        ImagesApi.draw_graph(self.nodes_list)

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
                    nodes_list[i].predecessor_list.append(predecessor)
                    predecessor.successor_list.append(nodes_list[i])

            # initialise pheromone edges
            for predecessor in nodes_list:
                nested_predecessors = [predecessor] + predecessor.nested_predecessors()
                for successor in nodes_list:
                    if successor not in nested_predecessors:
                        predecessor.pheromone_dict[successor] = self.config.init_pheromone_value

        return nodes_list

    def algorithm_run(self):
        # run function specified in self.config.algorithm_type with arguments self.config and self.nodes_list
        algorithm = getattr(AntAlgorithm, self.config.algorithm_type)(self.config, self.nodes_list)
        algorithm.run()

        logger.info("result_permutation history:")
        logger.info([ant.result_value for ant in algorithm.result_history])
        best_result = algorithm.history_best
        logger.info("best path: {0}".format(best_result.result_value))
        logger.info(" -> ".join([operation.name for operation in best_result.visited_list]))
        ImagesApi.schedule_image_create(best_result)

    def nodes_list_load(self):
        """Loads new nodes list and draws it"""
        pass


class UIManager(QtWidgets.QMainWindow, Manager, UiForm.Ui_MainWindow):
    """Handles the UI form input and output"""
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.RunButton.clicked.connect(self.algorithm_run)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               "Are you sure you want to quit?", QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class CLIManager(Manager):
    """Handles the CLI input and output"""
    def __init__(self):
        super().__init__()

