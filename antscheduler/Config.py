import configparser
from configparser import ConfigParser
import logging
import os

logger = logging.getLogger("AntScheduler.MaxMin")

class Config:
    """ Class containing all configuration infos as fields"""

    def __init__(self, _config_name):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', _config_name)
        algorithm_list = ["MaxMin", "AntSystem"]
        str_config_list = ["graph_file", "algorithm_type"]
        int_config_list = ["iterations", "ant_population", "max_min_ants_promoted"]
        float_config_list = ["evaporation_rate", "pheromone_potency", "pheromone_distribution", "init_pheromone_value"]
        parser = ConfigParser()
        parser.read(config_path)

        try:
            for str in str_config_list:
                setattr(self, str, parser.get("strings", str))

            for int in int_config_list:
                setattr(self, int, parser.getint("ints", int))

            for float in float_config_list:
                setattr(self, float, parser.getfloat("floats", float))
        except configparser.NoOptionError or configparser.NoSectionError:
            raise IOError(".ini config file corrupted!")
        if self.algorithm_type not in algorithm_list:
            raise IOError("wrong algorithm name!")
