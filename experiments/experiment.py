from algorithms.goalFunction import *
from algorithms.hillClimbSolver import *
from algorithms.naiveSolver import *
from algorithms.tabuSolver import *
class Experiment():
    def __init__(self, iterations, size, solver):
        self.statistics = []
        self.run(iterations, size, solver)
    
    def run(self, iterations, size, pickSolver):
        # Add first row in statistics
        row = "#Algorithm Size Avg.Time Avg.Score"
        self.statistics.append(row)

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
                elif('Tabu[' in pickSolver):
                    solver = (pickSolver[5:].replace(']','')).split(',')
                    tabuSize = int(solver[0])
                    iterations = int(solver[1])
                    solver = TabuSolver(graph, tabuSize, iterations)
                else:
                    break

                # Update Data from solver
                avgScore+=solver.score
                avgTime+=solver.time
            
            # Evaluation for a given size ended append this information to statistics
            avgScore, avgTime = avgScore/iterations, avgTime/iterations
            row = '{} {} {} {}'.format(solver.type, size, avgTime, avgScore)
            self.statistics.append(row)

    def saveStatistics(self, file):
        f= open(file,"w+")
        for row in self.statistics:
            f.write(row)
            f.write('\n')
        f.close()

    def displayStatistics(self):
        for row in self.statistics:
            print(row)
