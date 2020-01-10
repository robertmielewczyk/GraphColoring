from graphStructure.graph import Graph 
from utilities.graphFunctions import *
from algorithms.naiveSolver import NaiveSolver
from algorithms.hillClimbSolver import HillClimbSolver
from algorithms.HillClimbShallowSolver import HillClimbShallowSolver
from algorithms.tabuSolver import TabuSolver
from algorithms.simulatedAnnelingSolver import SimulatedAnnelingSolver
from algorithms.geneticSolver import GeneticSolver
from experiments.experiment import *
class CommandHandler():
    def __init__(self):
        self.graph = None
        self.solution = None
        self.solver = None
        self.experiment = None

    def state(self):
        print('graph:    {}'.format(self.graph))
        print('solution: {}'.format(self.solution))
        print('solver:   {}'.format(self.solver))

    def run(self):
        '''
        This is ofcourse bad and dangerous 
        but it's for debugging --> better option is a list
        of allowed commands but thats too many lines of code
        and it will make everything clutered so I'm sticking with this
        '''
        option = ''
        while(option != 'exit'):
            print('>>',end='')
            option = input()
            try:                 
                eval('self.{}'.format(option))  
            except (SyntaxError, NameError, TypeError, ZeroDivisionError, AttributeError):
                self.help()

    def help(self):
        commands = [
            '--help                         Lists Available Commands',
            'load_graph=Path                Load Graph from path',
            '   --graph-show                    Displays Graph'
            'load_solution=Path             Load Solution from path',
            '   --solution-plotHistory          Plots Matlab History',
            '   --solution-bestGraph            Prints Best Graph',
            '   --solution-score                Prints Best Score',
            'solver=Name[size][iter]        Run Solver(Naive, HillClimb[Shallow], Tabu, SimulatedAnneling, Genetic)',
            '   --solver-plotHistory            Plots Matlab History',
            '   --solver-bestGraph              Prints Best Graph',
            '   --solver-score                  Prints Best Score',   
            '   --solver-save=Name              Saves solution',
            '--experiment                   Runs Experiment',
            '   --experiment-save=file          Saves experiment to a file',
            '   --experiment-display            displays experiment',
            '   --experiment-plot               displays plot'
            ]
        for command in commands:
            print(command)

    def loadGraph(self, path):
        try:
            self.graph = Graph(path)
        except (FileNotFoundError):
            print('Couldnt load a file - typo? | file: {}'.format(path))

    def showGraph(self):
        if(self.graph == None):
            print('setup graph before displaying it')
        else:
            self.graph.plotGraph()

    def loadSolution(self, path):
        # Load Solution from File
        self.solution = loadSolution(path)

    def solutionScore(self):
        print(self.solution.score)

    def solutionBestGraph(self):
        print(self.solution.bestGraph)

    def solutionHistory(self):
        print(self.solution.history)

    def loadSolver(self, solver):
        try:
            if(solver == 'Naive'):
                self.solver = NaiveSolver(self.graph)
            elif(solver == 'HillClimb'):
                self.solver = HillClimbSolver(self.graph)
            elif(solver == "HillClimbShallow"):
                iterations = int(input("How many iterations: "))
                self.solver = HillClimbShallowSolver(self.graph, iterations)
            elif('Tabu[' in solver):
                solver = (solver[5:].replace(']','')).split(',')
                tabuSize = int(solver[0])
                iterations = int(solver[1])
                self.solver = TabuSolver(self.graph, tabuSize, iterations)
            elif(solver == 'Tabu'):
                self.solver = TabuSolver(self.graph)
            elif(solver == 'SimulatedAnneling'):
                self.solver = SimulatedAnnelingSolver(self.graph)
            elif(solver == 'Genetic'):
                population = int(input("Population: "))
                if(population>999999 or population<4):
                    population = 10
                generations = int(input("generataion: "))
                if(generations>999999 or generations<4):
                    generations = 10
                avg_tresh = int(input("Score to achive: "))
                if(avg_tresh>300 or avg_tresh<1):
                    avg_tresh=30
                roulete = input("Roulete true? yes/no")
                if(roulete=="yes"):
                    roulete = True
                    tournament = False
                else:
                    roulete = False
                    tournament = True
                self.solver = GeneticSolver(self.graph, population, generations=generations, avg_score_treshold=avg_tresh, roulete=roulete, tournament=tournament)
            else:
                print('This Solver Doesnt Exist - Typo')
        except ():
            print("Solver Error - Probably Graph is not set | graph: {}".format(self.graph))

    def solverPlotHistory(self):
        #Matplot
        if(self.solver == None):
            print('couldnt show history: solver is not defined')
        else:
            self.solver.plotHistory()

    def solverBestGraph(self):
        if(self.solver == None):
            print('couldnt show bestGraph: solver is not defined')
        else:
            self.solver.bestGraph.ToString()

    def solverScore(self):
        if(self.solver == None):
            print('couldnt show score: solver is not defined')
        else:
            print('best score: {}'.format(self.solver.score))

    def solverSave(self, name):
        if(self.solver == None):
            print('couldnt save solver: solver is not defined')
        else:
            self.solver.saveToFile(name)

    def performExperiment(self, iterations, size, solver):
        self.experiment = Experiment(iterations, size, solver)

    def saveExperiment(self, file):
        self.experiment.saveStatistics(file)

    def displayExperiment(self):
        self.experiment.displayStatistics()

    def plotExperiment(self):
        self.experiment.plotStatistics()






