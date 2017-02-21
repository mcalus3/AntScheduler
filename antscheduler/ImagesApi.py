import graphviz
import os
import logging

logger = logging.getLogger("AntScheduler.ImagesApi")
X11_colors = ["Blue", "BlueViolet", "Brown", "Chartreuse", "Coral", "CornflowerBlue", "Crimson", "DarkBlue", "DarkCyan",
              "DarkGoldenrod", "DarkGray", "DarkGreen", "DarkKhaki", "DarkMagenta", " DarkOliveGreen", "DarkOrange",
              "DarkOrchid", "DarkRed", "DarkSalmon", "DarkSeaGreen", "DarkSlateBlue", "DarkSlateGray", "DarkTurquoise",
              "DarkViolet", "DeepPink", "DeepSkyBlue", "DimGray", "DodgerBlue", "FireBrick", "ForestGreen", "Fuchsia"]
render_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


def draw_graph(nodes_list):
    """Draws the graph image using Graphviz library"""

    graph = graphviz.Digraph(name='ProcessGraph', format='png')
    graph.body.extend(['rankdir=LR'])
    graph.attr('node', style='bold')
    for node in nodes_list:
        graph.node(name=node.name, color=X11_colors[node.type])
        for successor in node.successor_list:
            graph.edge(node.name, successor.name, label=str(successor.time_value))

    try:
        graph.render(directory=render_dir)
    except RuntimeError:
        logger.warning("Can't render graphs. Check if Graphviz path is valid")

def schedule_image_create(_ant):
    """TODO: to be replaced by the scheduler class with matplotlib graph creation
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

    with open(os.path.join(render_dir, "output_schedule.txt"), "w") as text_file:
        text_file.write(schedule_str)
    """
    pass