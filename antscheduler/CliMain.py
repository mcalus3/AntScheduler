from Manager import Manager
import GVApi
import pycallgraph

config_file = "config.ini"


def main():
    graphviz = pycallgraph.output.GraphvizOutput()
    graphviz.output_file = 'basic.png'
    #with pycallgraph.PyCallGraph(output=graphviz):
    manager = Manager(config_file)
    if manager.config.render_images:
        GVApi.draw_graph(manager.nodes_list)
    manager.algorithm_run()


if __name__ == "__main__":
    main()
