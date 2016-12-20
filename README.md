# AntScheduler
Application uses different Ant Algorithms to resolve Job-shop scheduling problem and generate a schedule for process given by the nodes list specified in input.
First version of application was created for academic purposes on Gdansk University of Technology, it had to generate a schedule of work for industrial process given by the user, modelled as a directed, acyclic graph with colors on the nodes and weighted edges.
Input is an operation list given in the .csv file (containing for operation: operation name, machine type, time length and predecessors list)
Output is a schedule of a best result found by the algorithm and history of results during search iterations.
Application visualises graph using GraphViz software.
