import pycallgraph
import antscheduler.__main__ as __main__

graphviz = pycallgraph.output.GraphvizOutput()
graphviz.output_file = 'basic.png'

with pycallgraph.PyCallGraph(output=graphviz):
    __main__.main()
