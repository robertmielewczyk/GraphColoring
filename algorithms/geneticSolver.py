from algorithms.algorithm import Algorithm
from algorithms.goalFunction import goalFunction
import numpy as np
import random
import math
import copy
class GeneticSolver(Algorithm):
    def __init__(self, graph, population=10, cross_prob=1, mutation_prob=1, generations=500, avg_score_treshold=1, num_parents=2):
        super().__init__()
        population = [self.generateRandomMask(graph) for i in range(population)]
        choice = input("(int) Select termination condition: iter/score : 1 or 2: -->")
        self.run(graph, population, cross_prob, mutation_prob, generations, avg_score_treshold, choice, num_parents)

    def run(self,graph, population, cross_prob, mutation_prob, generations, avg_score_treshold, choice, num_parents):
        t_condition, avg_score = self.termination(graph, generations ,population, avg_score_treshold, choice)
        while(t_condition):
            #Debug
            print("Generation: {} avg_score/tresh: {}/{}".format(generations, avg_score, avg_score_treshold))
            #print(population)
            # Measuring the fitness of each chromosome in the population.
            fitness_list = self.evaluate_fitness(graph, population)
            #print(fitness_list)
            # Selecting best mates
            parents = self.selection(population, fitness_list, num_parents)
            #print("Parents: (Score, Mask) {},{}".format(parents[0], parents[1]))

            # Generate crossover
            children = self.cross(parents, population)
            #print(children)

            # Generate Mutations and update new population (keeping the reversed child off)
            # Mutate
            children_mutations = self.mutation(children)

            #Add parents again
            population.append(parents[0][1])
            population.append(parents[1][1])
            #Add children
            population.append(children[0])
            population.extend(children_mutations)
            #Delete 4 worst - kinda still something wrong here
            for i in range(5):
                indx_worst = np.argmax(fitness_list)
                #print("fitness_list: {} indx: {}".format(fitness_list, indx_worst))
                population.pop(indx_worst)


            # DEBUG PARENTS AND CHILDREN
            #child = goalFunction(graph.applyMask(children[0]))
            #print("Generation: {} Parent1: {} parent2: {} Children: {}".format(generations, parents[0][0], parents[1][0], child))

            # Update t_condition
            generations -=1
            t_condition, avg_score = self.termination(graph, generations ,population, avg_score_treshold, choice)

            #Update score
            graph_indx = np.argmin(fitness_list)
            mask = population[graph_indx]
            score = goalFunction(graph.applyMask(mask))
            if(score<self.score):
                self.history.append(min(fitness_list))
                graph_indx = np.argmin(fitness_list)
                mask = population[graph_indx]
                self.bestGraph = copy.deepcopy(graph.applyMask(mask))
                #print("check: {}".format(goalFunction(self.bestGraph)))
                self.score = score

    def evaluate_fitness(self, graph, population):
        return [goalFunction(graph.applyMask(i)) for i in population]

    def selection(self, population, fitness_list, num_parents):
        # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
        parents = []
        for i in range(num_parents):
            parent_indx = np.argmin(fitness_list)
            parents.append([fitness_list.pop(parent_indx),population[parent_indx]])
        return parents

    def cross(self, parents, population):
        child = []
        cross_point = random.randrange(0, len(parents[0][1])-1)
        #Create children first normal, second reversed
        chromosomeX = [parents[0][1][i] for i in range(0, cross_point)]        
        chromosomeY = [parents[1][1][i] for i in range(cross_point, len(parents[0][1]))]
        child.extend(chromosomeX), child.extend(chromosomeY)
        children = []
        children.append(child), children.append(list(reversed(child)))
        return children


    def mutation(self, children):
        index = random.randrange(0,len(children[0])-1)   
        children[0][index] = random.randrange(0,len(children[0])-1)
        return children         

    def termination(self, graph, generations, population, avg_score_treshold, choice): 
        if(choice==str(1)):
            t_condition = generations > 0
            avg_score = int(np.mean([goalFunction(graph.applyMask(i)) for i in population]))
        else:
            avg_score = np.mean([goalFunction(graph.applyMask(i)) for i in population])
            t_condition = avg_score_treshold > avg_score
        return t_condition, avg_score


