import xml.etree.ElementTree as ElemTree


class Config:
    """ Class containing all configuration infos as fields"""

    def __init__(self, _config_path):
        try:
            tree = ElemTree.parse(_config_path)
        except IOError:
            return
        root = tree.getroot()

        self.graph_file = root.find("graph_file").attrib.get("value")
        self.algorithm_type = root.find("algorithm_type").attrib.get("value")
        self.iterations = int(root.find("iterations").attrib.get("value"))
        self.ant_population = int(root.find("ant_population").attrib.get("value"))
        self.max_min_ants_promoted = int(root.find("max_min_ants_promoted").attrib.get("value"))
        self.evaporation_rate = float(root.find("evaporation_rate").attrib.get("value"))
        self.pheromone_potency = float(root.find("pheromone_potency").attrib.get("value"))
        self.pheromone_distribution = float(root.find("pheromone_distribution").attrib.get("value"))
        self.init_pheromone_value = float(root.find("init_pheromone_value").attrib.get("value"))
