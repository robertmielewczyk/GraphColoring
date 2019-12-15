#!/usr/bin/env python
'''
This File is used for dealing with console input
run this file in console by ./MetaAlgorithms.py (your arguments)

use --help for list of commands 
'''
#--------------------#
# Initialize Handler #
#--------------------#
import sys
import re
from utilities.commandHandler import CommandHandler
handler = CommandHandler()

#-------------------#
# Control Arguments #
#-------------------#
for arg in sys.argv:
    #Run in Build Mode
    if(arg == 'run'):
        handler.run()

    # Run Command Line
    if(arg == '--help'):
        handler.help()
    
    if(re.search('load_graph=*', arg)):
        path = arg[11:]
        handler.loadGraph(path)

    if('--graph-show' in arg):
        handler.showGraph()

    if(re.search('load_solution=*', arg)):
        solution = arg[14:]
        handler.loadSolution(path)

    if('solver=' in arg):
        if('solver=Tabu['):
            solver = arg[7:]
            handler.loadSolver(solver)
            continue

        solver = arg[7:]
        handler.loadSolver(solver)

    if('--solver-plotHistory' in arg):
        handler.solverPlotHistory()

    if('--solver-bestGraph' in arg):
        handler.solverBestGraph()

    if('--solver-score' in arg):
        handler.solverScore()

    if(re.search('--solver-save=*', arg)):
        name = arg[14:]
        handler.solverSave(name)
    


    
    
