import sys
sys.path.insert(0, 'C:\\repos\\AntScheduler\\antscheduler')

import pycallgraph
import antscheduler.__main__

graphviz = pycallgraph.output.GraphvizOutput()
graphviz.output_file = 'profiler.png'


with pycallgraph.PyCallGraph(output=graphviz):
    antscheduler.__main__.main()
