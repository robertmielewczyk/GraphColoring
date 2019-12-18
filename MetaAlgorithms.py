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
        path = arg[14:]
        handler.loadSolution(path)

    if('--solution-score' in arg):
        handler.solutionScore()

    if('--solution-graph' in arg):
        handler.solutionBestGraph()

    if('--solution-history' in arg):
        handler.solutionHistory()

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

    if('--experiment' in arg):
        if('--experiment-save=' in arg):
            file = arg[18:]
            print(file)
            handler.saveExperiment(file)
            continue
        if('--experiment-display' in arg):
            handler.displayExperiment()
            continue
        if('--experiment-plot' in arg):
            handler.plotExperiment()
            continue
        print('EXPERIMENTS:\n--Set Parameters--\nIterations:')
        iterations = input()
        iterations = int(iterations)
        print("Size:")
        size= input()
        size = int(size)
        if(size>9 or size<2):
            size=9
        print("Solver: - must be: Naive/HillClimb/Tabu[TabuSize,Iterations]")
        solver = input()
        handler.performExperiment(iterations, size, solver)

    


    
    
