import sys
sys.path.append('.')
from algorithms.geneticSolver import GeneticSolver
from algorithms.naiveSolver import *
from graphStructure.graph import Graph
from libraries.validator import Validator
import itertools
import numpy as np
class GeneticParmeterFinder():
    '''
    This class finds best parameters for a given graph for Genetic Agorithm
    '''
    def __init__(self, graph):
        # User Input - Choose Termination method
        input_validator = Validator()
        params = {}
        params['generations'] = input_validator.range(4, 999999, default=10, message="Generations: ")
        params['avg_tresh'] = input_validator.range(4, 500, default=10, message="Avg_tresh: ")
        params['deviation_tresh'] = input_validator.range(0.1, 500, default=10, message="Deviation_tresh: ")
        params['termination'] = input_validator.exact_string(['Iter','Score', 'Deviation'], message="Select termination condition: Iter/Score/Deviation: ")

        # Population step - Samples
        number_of_possibilities = calculateFullPropagation(graph)
        population_samples = 10

        # Parameters to test
        cross = ['Single', 'Two']
        cross_prob = [i for i in itertools.takewhile(lambda x: x <= 1, itertools.count(0.0, 0.1))]
        mutation_prob = [i for i in itertools.takewhile(lambda x: x <= 1, itertools.count(0.0, 0.1))]
        succesion = ['Tournament', 'Roulette']
        population = [i for i in range(4, number_of_possibilities-1, int(number_of_possibilities/population_samples))]

        # Test all parameters
        tests = []
        iteration = 0
        for cross_i in cross:
            params['cross'] = cross_i
            for succesion_i in succesion:
                params['succesion'] = succesion_i
                for cross_prob_i in cross_prob:
                    params['cross_prob'] = cross_prob_i
                    for mutation_prob_i in mutation_prob:
                        params['mutation_prob'] = mutation_prob_i
                        for population_i in population:
                            params['population'] = population_i
                            iteration+=1
                            print(iteration)
                            # Run test for created parameters
                            test = {}
                            solver = GeneticSolver(graph, params)
                            test['params'], test['solver_score'], test['solver_time'], test['iteration'] = params, solver.score, solver.time, iteration
                            tests.append(test)

        # Assign Important Results
        self.history = tests
        solver_score = [tests[i]['solver_score'] for i in range(len(tests))]
        self.best_parameters_score = tests[np.argmin(solver_score)]
        print('The best parameters are:\n{}'.format(self.best_parameters_score))
        
        name = "experiments/saved_experiments/genetic[iter-{}]graph{}".format(params['generations'], graph.numberOfNodes)
        print("Saving Genetic as: {}".format(name))
        self.save_parameters(name)

    def save_parameters(self, file):
        #Change this terrible thing in future
        string = "Generations: {}\nPopulation: {}\nSuccesion: {}\nAvg_treshold: {}\nTermination: {}\nDeviation_Treshold: {}\nCross Probability: {}\nMutation probability: {}\
                \n\nSolver_score: {}\nSolver_time: {}\nIteration_discovered: {}\n---------".format(self.best_parameters_score['params']['generations'],self.best_parameters_score['params']['population'],\
                self.best_parameters_score['params']['succesion'], self.best_parameters_score['params']['avg_tresh'], self.best_parameters_score['params']['termination'],\
                self.best_parameters_score['params']['deviation_tresh'], self.best_parameters_score['params']['cross_prob'], self.best_parameters_score['params']['mutation_prob'],\
                self.best_parameters_score['solver_score'], self.best_parameters_score['solver_time'], self.best_parameters_score['iteration'])
        f= open(file,"w+")
        f.write(string)
        f.close()
        

if __name__ == "__main__":
    graph = Graph('exampleGraphs/graph3.yaml')
    GeneticParmeterFinder(graph)