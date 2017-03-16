import pycallgraph
import antscheduler.__main__

graphviz = pycallgraph.output.GraphvizOutput()
graphviz.output_file = 'profiler.png'


with pycallgraph.PyCallGraph(output=graphviz):
    antscheduler.__main__.main()
