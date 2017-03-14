class Node:
    """ Class representing nodes on process graph. It represents operation in industrial process"""

    def __init__(self, _name, _type, _time_value):
        self.name = _name
        self.type = _type
        self.time_value = _time_value
        self.successor_list = []
        self.predecessor_list = []
        self.pheromone_dict = {}
        self.start_time = None

    def pheromones_get(self, _nodes):
        return {node: self.pheromone_dict[node] for node in _nodes if node in self.pheromone_dict}

    def nested_predecessors(self):
        nested_list = self.predecessor_list[:]
        if not nested_list:
            return []
        for node in nested_list:
            nested_list.extend(node.nested_predecessors())
        return nested_list


def graph_create(graph_text):

    graph_text = graph_text_format(graph_text)
    nodes_list = []

    # read the static info about each node
    for row in graph_text:
        nodes_list.append(Node(row[0], int(row[1]), int(row[2])))

    # read the dynamic info about each node (successors lists)
    for i, row in enumerate(graph_text):
        try:
            pre_list = row[3].split()
            for predecessor in [node for node in nodes_list if node.name in pre_list]:
                nodes_list[i].predecessor_list.append(predecessor)
                predecessor.successor_list.append(nodes_list[i])
        except IndexError:
            continue  # node has no successors

    start_nodes = [node for node in nodes_list if node.predecessor_list == []]
    if len(start_nodes) > 1:
        new_start_node = Node("automatic_start", 0, 0)
        new_start_node.successor_list = start_nodes
        nodes_list.insert(0, new_start_node)
        for node in start_nodes:
            node.predecessor_list.append(new_start_node)

    return nodes_list


def graph_text_format(graph_text):

    graph_text = graph_text.splitlines()
    for row in graph_text:
        if not row:
            graph_text.remove(row)

    graph_text = [row.split(",") for row in graph_text]
    for row in graph_text:
        if len(row) < 3:
            graph_text.remove(row)
            continue
        try:
            int(row[1])
            int(row[2])
        except ValueError:
            graph_text.remove(row)

    return graph_text
