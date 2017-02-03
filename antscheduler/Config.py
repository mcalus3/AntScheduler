import configparser
from configparser import ConfigParser
import logging

logger = logging.getLogger("AntScheduler.MaxMin")


class Config:
    """ Class containing all configuration infos as fields"""

    def __init__(self, _config_path):
        parser = ConfigParser()
        parser.read(_config_path)

        try:
            self.graph_file = parser.get("strings", "graph_file")
            self.algorithm_type = parser.get("strings", "algorithm_type")

            self.iterations = parser.getint("ints", "iterations")
            self.ant_population = parser.getint("ints", "ant_population")
            self.max_min_ants_promoted = parser.getint("ints", "max_min_ants_promoted")

            self.evaporation_rate = parser.getfloat("floats", "evaporation_rate")
            self.pheromone_potency = parser.getfloat("floats", "pheromone_potency")
            self.pheromone_distribution = parser.getfloat("floats", "pheromone_distribution")
            self.init_pheromone_value = parser.getfloat("floats", "init_pheromone_value")
        except configparser.NoOptionError or configparser.NoSectionError:
            raise IOError(".ini config file corrupted!")
