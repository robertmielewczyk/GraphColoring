from algorithms.goalFunction import *
from algorithms.hillClimbSolver import *
from algorithms.HillClimbShallowSolver import HillClimbShallowSolver
from algorithms.naiveSolver import *
from algorithms.tabuSolver import *
from algorithms.simulatedAnnelingSolver import *
from algorithms.geneticSolver import GeneticSolver
from libraries.validator import Validator
class Experiment():
    def __init__(self, iterations, size, solver):
        self.statistics = []
        self.rowData = []
        self.run(iterations, size, solver)
    
    def run(self, iterations, size, pickSolver):
        # Add first row in statistics
        row = "#Algorithm Size Avg.Time Avg.Score"
        input_validator = Validator()
        self.statistics.append(row)
        self.params = None

        #Perform experiments for the entire set of graphs - from size 2-size
        for size in range(2,size):
            # Perform experiment
            avgTime = 0
            avgScore = 0
            for i in range(iterations):
                # Pick solver (not the most elegant solution but it doesnt interfere with
                # other classes - I could also use solver from CommandHandler or fix a common
                # solver.run interface but it would actually be more work than just picking it here)
                graph = Graph('exampleGraphs/graph{}.yaml'.format(size))
                if(pickSolver == 'Naive'):
                    solver = NaiveSolver(graph)
                elif(pickSolver == 'HillClimb'):
                    solver = HillClimbSolver(graph)
                elif(pickSolver == 'HillClimbShallow'):
                    iterations = input_validator.range(1, 99999, message="Iterations", default=10)
                    solver = HillClimbShallowSolver(graph, iterations)
                elif('Tabu[' in pickSolver):
                    solver = (pickSolver[5:].replace(']','')).split(',')
                    tabuSize = int(solver[0])
                    iterations = int(solver[1])
                    solver = TabuSolver(graph, tabuSize, iterations)
                elif('SimulatedAnneling' in pickSolver):
                    solver = SimulatedAnnelingSolver(graph)
                elif('Genetic' in pickSolver):
                    self.set_params()
                    solver = GeneticSolver(graph, self.params)
                else:
                    break

                # Update Data from solver
                avgScore+=solver.score
                avgTime+=solver.time
            
            # Evaluation for a given size ended append this information to statistics
            avgScore, avgTime = avgScore/iterations, avgTime/iterations
            row = '{} {} {} {}'.format(solver.type, size, avgTime, avgScore)
            self.statistics.append(row)
            self.rowData.append([solver.type, size, avgScore, avgTime])
    def set_params(self):
        input_validator = Validator()
        if(self.params == None):
            print("Set params - for the best results run ParameterFinder first")
            params = {}
            params['population'] = input_validator.range(4, 999999, default=10, message="Population: ") 
            params['generations'] = input_validator.range(4, 999999, default=10, message="Generations: ")
            params['avg_tresh'] = input_validator.range(4, 500, default=10, message="Avg_tresh: ")
            params['deviation_tresh'] = input_validator.range(0.1, 500, default=10, message="Deviation_tresh: ")
            params['succesion'] = input_validator.exact_string(['Tournament','Roulette'], message="Succesion (Tournament/Roulette)")
            params['termination'] = input_validator.exact_string(['Iter','Score', 'Deviation'], message="Select termination condition: Iter/Score/Deviation: ")
            params['cross'] = input_validator.exact_string(['Single', 'Two'], message="Select Crossover method: Single/Two: ")
            params['cross_prob'] = input_validator.range(0.1, 1, default=1, message="Cross_Probability(0.1, 1): ", floating=True)
            params['mutation_prob'] = input_validator.range(0.1, 1, default=1, message="Mutation_Probability(0.1, 1): ", floating=True)
            self.params = params


    def saveStatistics(self, file):
        f= open(file,"w+")
        for row in self.statistics:
            f.write(row)
            f.write('\n')
        f.close()

    def displayStatistics(self):
        for row in self.statistics:
            print(row)

    def plotStatistics(self):
        import matplotlib.pyplot as plt
        size, avgScore, avgTime = [], [], []
        for row in range(len(self.rowData)):
            size.append(self.rowData[row][1])
            avgScore.append(self.rowData[row][2])
            avgTime.append(self.rowData[row][3])
        #Plot size-score/time
        plt.title('my plot')
        plt.plot(size, avgScore, color='green')
        plt.xlabel('size')
        plt.plot(size, avgTime,color='blue')
        plt.legend({'avg.Score','avg.Time'})
        plt.show()
