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
from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg

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
        self.nodes_list = None

    def graph_create(self):
        graph_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.config.graph_file)

        if self.__class__ == UIManager:
            csv_reader = self.OperationList.toPlainText()
            csv_reader = csv_reader.splitlines()
            csv_reader = [row.split(",") for row in csv_reader]

        else:
            with open(graph_path, "r") as file_csv:
                csv_reader = file_csv.read()
                csv_reader = [row.split(",") for row in csv_reader]

        nodes_list = []
        for row in csv_reader:
            # check if the data aren't missing
            if len(row) < 3:
                logger.warning("Incorrect input, blank line in input file")
                continue
            # read the static info about each node
            nodes_list.append(GraphNode(row[0], int(row[1]), int(row[2])))

            # read the dynamic info about each node (successors lists)
        for i, row in enumerate(csv_reader):
            try:
                pre_list = row[3].split()
                for predecessor in [node for node in nodes_list if node.name in pre_list]:
                    nodes_list[i].predecessor_list.append(predecessor)
                    predecessor.successor_list.append(nodes_list[i])
            except IndexError:
                continue  # node has no successors

            # initialise pheromone edges
            for node in nodes_list:
                nested_predecessors = [node] + node.nested_predecessors()
                for successor in nodes_list:
                    if successor not in nested_predecessors:
                        node.pheromone_dict[successor] = self.config.init_pheromone_value
        # draw a graph image
        ImagesApi.draw_graph(nodes_list)
        if self.__class__ == UIManager:
            svg_item = QtSvg.QGraphicsSvgItem("..\\data\\ProcessGraph.gv.svg")
            scene = QtWidgets.QGraphicsScene()
            scene.addItem(svg_item)
            self.processView.setScene(scene)

        self.nodes_list = nodes_list

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


class UIManager(QtWidgets.QMainWindow, Manager, UiForm.Ui_MainWindow):
    """Handles the UI form input and output"""

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.StartButton.clicked.connect(self.algorithm_run)
        self.CreateButton.clicked.connect(self.graph_create)
        with open("..\\data\\ExampleInput.csv") as input:
            self.OperationList.setPlainText(input.read())
        self.graph_create()
        #self.algorithmComboBox.setCurrentIndex()
        configs = [(self.iterationsLineEdit, "iterations"),
                   (self.antPopulationLineEdit, "ant_population"),
                   (self.evaporationRateLineEdit, "evaporation_rate"),
                   (self.pheromonePotencyLineEdit, "pheromone_potency"),
                   (self.initPheromoneLineEdit, "init_pheromone_value"),
                   (self.antsPromotedLineEdit, "max_min_ants_promoted"),
                   (self.pheromoneDistributionLineEdit, "pheromone_distribution")]

        #self.iterationsLineEdit.textChanged.connect(self.iterations_slot)
        for pair in configs:
            pair[0].setText(str(getattr(self.config, pair[1])))
            pair[0].textChanged.connect(generate_setter(pair, self.config))

    def iterations_slot(self):
        self.config.iterations = int(str(self.iterationsLineEdit.text()))

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               "Are you sure you want to quit?", QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def generate_setter(pair, config_obj):
    def func():
        try:
            setattr(config_obj, pair[1], int(str(pair[0].text())))
        except ValueError:
            setattr(config_obj, pair[1], float(str(pair[0].text())))
    return func

class CLIManager(Manager):
    """Handles the CLI input and output"""

    def __init__(self):
        super().__init__()
