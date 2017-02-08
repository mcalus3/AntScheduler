import configparser
from configparser import ConfigParser
import logging
import os

logger = logging.getLogger("AntScheduler.MaxMin")

class Config:
    """ Class containing all configuration infos as fields"""

    def __init__(self, _config_name):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', _config_name)
        parser = ConfigParser()
        parser.read(config_path)

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

            self.render_images = parser.getboolean("booleans", "render_images")
        except configparser.NoOptionError or configparser.NoSectionError:
            raise IOError(".ini config file corrupted!")
