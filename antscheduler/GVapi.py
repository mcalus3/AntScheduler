__author__ = 'mcalus'

import graphviz

X11_colors = ["Blue", "BlueViolet", "Brown", "Chartreuse", "Coral", "CornflowerBlue", "Crimson", "DarkBlue", "DarkCyan",
              "DarkGoldenrod", "DarkGray", "DarkGreen", "DarkKhaki", "DarkMagenta", " DarkOliveGreen", "DarkOrange",
              "DarkOrchid", "DarkRed", "DarkSalmon", "DarkSeaGreen", "DarkSlateBlue", "DarkSlateGray", "DarkTurquoise",
              "DarkViolet", "DeepPink", "DeepSkyBlue", "DimGray", "DodgerBlue", "FireBrick", "ForestGreen", "Fuchsia"]


def draw_graph(nodes_list):
    graph = graphviz.Digraph('ProcessGraph', filename='process.gv')
    graph.body.extend(['rankdir=LR'])
    graph.attr('node', style='bold')
    for node in nodes_list:
        graph.node(name=node.name, color=X11_colors[node.type])
        for successor in node.successor_list:
            graph.edge(node.name, successor.name, label=str(successor.time_value))

    graph.view()
