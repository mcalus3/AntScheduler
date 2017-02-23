![AntScheduler Logo](https://github.com/mcalus3/AntScheduler/blob/master/graphics/AntScheduler_logo.png)

Ant-powered scheduling app by mcalus3.

**AntScheduler** was created for academic purposes, my first goal was to implement a simple, but potentially usable industrial application that can help with industrial process scheduling. The basic task of **AntScheduler** is to solve the combinatorial problem of scheduling n operations on m machines in an optimum manner. That's where comes Ant Colony Optimization algorithm firstly proposed by M. Dorigo in 1992 (and one of the best till now!). The application is under developement.

## Installation and dependencies

Python 3.0 or higher is required.
Packages **Graphviz** and **PyQt5** are required, use pip to install
```erb
$ pip install graphviz
$ pip install PyQt5
```
To render the generated DOT source code, you also need to install Graphviz (http://www.graphviz.org/Download.php).
Make sure that the directory containing the ``dot`` executable is on your systems' path.

## Usage

**AntScheduler** is in early phase of development, so there are simple cli ang gui interfaces right now.  To run app, run __main__.py (or run package antscheduler). With cli argument you will run algorithm without gui application. All configurations are specified in file config.xml. Input file is a .csv file containing list of nodes in graph representing the process to be scheduled. Each node represents different operation and is specified by following attributes: name, machine type, time length and list od predecessors (operations that has to be completed before). For example, following list of nodes:
```erb
start,0,0
a1,1,2,start
a2,2,6,a1 b1
b1,1,3,start
b2,3,3,b1
c1,1,2,start
c2,3,7,c1
d1,2,6,start
d2,3,2,d1 e1
end,0,0,a2 b2 c2 d2 e2 f2
```
Will represent following graph (where colors are machine types):
![example_graph](https://github.com/mcalus3/AntScheduler/blob/master/graphics/example_graph.png)

Application creates best schedule found by the algorithm and saves it in file output_schedule.txt. It also prints history of found results in console (to visualize the algorithm convergence).
