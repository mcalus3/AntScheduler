from Manager import Manager
import GVApi

config_file = "config.ini"


def main():
    manager = Manager(config_file)
    if manager.config.render_images:
        GVApi.draw_graph(manager.nodes_list)
    manager.algorithm_run()


if __name__ == "__main__":
    main()
