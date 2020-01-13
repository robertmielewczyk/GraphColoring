import sys
sys.path.append('.')
from algorithms.algorithm import Algorithm
from algorithms.goalFunction import goalFunction
import numpy as np
from multiprocessing import Process
import multiprocessing
import random
import math
import copy
import time
class GeneticParallelSolver(Algorithm):
    def __init__(self, graph, params, num_parents=2, debug=False):
        super().__init__()
        population = [self.generateRandomMask(graph) for i in range(params['population'])]
        self.debug = GeneticDebug(params)
        self.ga = GeneticAlgorithm(params)
        self.type = 'Genetic'
        self.run(graph,population, params, num_parents,debug)

    def run(self,graph, population, params, num_parents,debug):
        start = time.time()
        population = [self.generateRandomMask(graph) for i in range(params['population'])]
        t_condition, avg_score, deviation = self.ga.termination_method(graph ,population)
        while(t_condition):
            # Measuring the fitness of each chromosome in the population. And Updating the population
            #In parallel
            fitness_list, population = self.run_parallel(population, graph)
            
            # Selecting best mates(Parents) and add them to population
            parents = self.ga.selection(population, fitness_list, num_parents)

            # Generate crossover
            if(params['cross_prob']>random.random()):
                children = self.ga.cross_method(population, parents)
                if(params['mutation_prob']>random.random()):
                    # Generate Mutations
                    children_mutations = self.ga.mutation(population, children)

            # Update Population and measuare new fitness
            fitness_list = self.ga.evaluate_fitness(graph, population)

            # Update t_condition
            t_condition, avg_score, deviation = self.ga.termination_method(graph ,population)

            # Update score
            graph_indx = np.argmin(fitness_list)
            mask = population[graph_indx]
            score = goalFunction(graph.applyMask(mask))
            if(score<self.score):
                self.history.append(score)
                self.bestGraph = copy.deepcopy(graph.applyMask(mask))
                self.score = goalFunction(self.bestGraph)

            # Debug
            if(debug):
                self.debug.show_iterations(avg_score, deviation)
                #self.debug.show_parent_children(parents, children, children_mutations, graph)
        end = time.time()
        self.time = end - start

    def run_cpu_tasks_in_parallel(self, tasks):
        running_tasks = [Process(target=task) for task in tasks]
        for running_task in running_tasks:
            running_task.start()
        for running_task in running_tasks:
            running_task.join()

    def run_parallel(self, population, graph):
        # Prepare Data for parallelism
        population_point = int(len(population)/2)
        #fitness_list1, population1 = self.ga.succesion_method(population[0:population_point], graph)
        #fitness_list2, population2 = self.ga.succesion_method(population[population_point:], graph)
        recv_end, send_end = multiprocessing.Pipe(False)

        # Run In parallel
        end = []
        p1 = Process(target=self.ga.succesion_method(population[0:population_point], graph,send_end))
        p1.start(), end.append(recv_end)
        p2 = Process(target=self.ga.succesion_method(population[population_point:], graph,send_end))
        p2.start(), end.append(recv_end)
        p1.join(), p2.join()
        process = [x.recv() for x in end]

        # Return Joined Arrays
        fitness_list = []
        population = []
        fitness_list.extend(process[0]['fitness_list']), fitness_list.extend(process[1]['fitness_list'])
        population.extend(process[0]['population']), population.extend(process[0]['population'])

        return fitness_list, population


#region DEBUG_CLASS
class GeneticDebug():
    def __init__(self, params):
        self.avg_tresh = params['avg_tresh']
        self.deviation_tresh = params['deviation_tresh']
        self.succesion = params['succesion']
        self.termination = params['termination']
        self.generations = params['generations']
        self.population = params['population']
        self.cross_prob = params['cross_prob']
        self.mutation_prob = params['mutation_prob']
        self.generations_counter = 0
        #self.show_parameters()

    def show_parameters(self):
        print("\n--DEBUG--\nGenetic Algorithm Run With These Parameters:\
               \nGenerations: {}\nPopulation: {}\nSuccesion: {}\nAvg_treshold: {}\nTermination: {}\nDeviation_Treshold: {}\nCross Probability: {}\nMutation probability: {}\
                \n---------".format(self.generations, self.population, self.succesion, self.avg_tresh, self.termination, self.deviation_tresh, self.cross_prob, self.mutation_prob))

    def show_iterations(self, avg_score, deviation):
        self.generations_counter+=1
        if(deviation>1):
            deviation = int(deviation)
        print("Generation: {} avg_score/tresh: {}/{} Deviation/tresh: {}/{}".format(self.generations_counter, int(avg_score), self.avg_tresh, deviation, self.deviation_tresh))

    def show_population(self, population):
        pass        

    def show_parent_children(self,generations, parents, children, children_mutations, graph):
        child = goalFunction(graph.applyMask(children[0]))
        print("Generation: {} Parent1: {} parent2: {} Children: {}".format(generations, parents[0][0], parents[1][0], child))
#endregion

#region GENETIC_ALGORITHM
class GeneticAlgorithm():
    def __init__(self, params):
        self.succesion = params['succesion']
        self.termination = params['termination']
        self.avg_tresh = params['avg_tresh']
        self.deviation_tresh = params['deviation_tresh']
        self.generations = params['generations']
        self.cross = params['cross']
        self.termination_method_count =0
#region METHOD_BUILDERS

    def succesion_method(self, population, graph, send_end, best_percentage=0.3):
        paralell = {}
        fitness_list = self.evaluate_fitness(graph, population)
        if(self.succesion == "Tournament"):
            fitness_list, population = (self.tournament(fitness_list, population, best_percentage))
        elif(self.succesion == "Roulette"):
            fitness_list, population = self.roulete(fitness_list, population, graph)
        paralell['fitness_list'] = fitness_list
        paralell['population'] = population
        send_end.send(paralell)

    def termination_method(self, graph, population): 
        deviation, avg_score = self.calculate_standard_deviation(graph, population)
        if(self.termination=="Iter"):
            t_condition = self.termination_method_count<self.generations 
        elif(self.termination=="Score"):
            t_condition = self.avg_tresh < avg_score
        elif(self.termination=="Deviation"):
            t_condition = self.deviation_tresh <deviation
        self.termination_method_count+=1
        return t_condition, avg_score, deviation

    def cross_method(self, population, parent):
        if(self.cross == "Single"):
            return self.single_point_cross(population, parent)
        elif(self.cross == "Two"):
            return self.two_point_cross(population, parent)

#endregion

    def calculate_standard_deviation(self, graph, population):
        import math
        fitness_list = self.evaluate_fitness(graph, population)
        avg_score = np.mean([goalFunction(graph.applyMask(i)) for i in population])
        variance = np.mean([math.pow(i-avg_score,2) for i in fitness_list])
        deviation = math.sqrt(variance)
        return deviation, avg_score

    def evaluate_fitness(self, graph, population):
        return [goalFunction(graph.applyMask(i)) for i in population]

    def selection(self, population, fitness_list, num_parents):
        # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
        parents = []
        for i in range(num_parents):
            parent_indx = np.argmin(fitness_list)
            parents.append([fitness_list.pop(parent_indx),population[parent_indx]])
        
        #Add parents to population    
        population.append(parents[0][1])
        population.append(parents[1][1])
        return parents
#region CROSS_METHODS

    def single_point_cross(self, population, parents):
        '''
        Creates children based of their parents
        Parent1 -> [1011], Parent2 -> [0011]  
        Children -> [Parent1(1bit)xParent2(3bit)] , Children2 -> [Parent2(3bit)xParent1(1bit)]
        '''
        child1 = [] 
        child2 = []
        cross_point = random.randrange(0, len(parents[0][1])-1)
        #Create children first normal, second reversed
        chromosomeX = [parents[0][1][i] for i in range(0, cross_point)]        
        chromosomeY = [parents[1][1][i] for i in range(cross_point, len(parents[0][1]))]
        child1.extend(chromosomeX), child1.extend(chromosomeY)
        child2.extend(chromosomeY), child2.extend(chromosomeX)
        children = []
        children.append(child1), children.append(child2)
        population.extend(children)
        return children

    def two_point_cross(self, population, parents):
        '''
        Creates children based of their parents
        Parent1 -> [10111], Parent2 -> [00110]  
        Children -> [Parent1(1bit)xParent2(3bit)xParent1(1bit)] , Children2 -> [Parent2(3bit)xParent1(1bit)Parent2(1bit)]
        '''
        child1 = [] 
        child2 = []
        cross_points = []

        # Generate Cross Points
        choices = [i for i in range(len(parents[0][1])-1)]
        random.shuffle(choices)
        cross_points.append(choices[0]), cross_points.append(choices[1])
        cross_points.sort()

        # Generate Partials
        #print(cross_points)
        chromosomeX = [parents[0][1][i] for i in range(0, cross_points[0])]        
        chromosomeY = [parents[1][1][i] for i in range(cross_points[0], cross_points[1])]
        chromosomeZ = [parents[0][1][i] for i in range(cross_points[1], len(parents[0][1]))]

        # Apply Cross Rule to children
        child1.extend(chromosomeX), child1.extend(chromosomeY), child1.extend(chromosomeZ)
        child2.extend(chromosomeY), child2.extend(chromosomeX), child2.extend(chromosomeZ)

        # Add them to population
        children = []
        children.append(child1), children.append(child2)
        population.extend(children)
        return children
#endregion

    def mutation(self, population, children):
        '''
        Picks a random position and changes it to random value(within range - NumberOfNodes)
        example:
            [100101] Before
            [100001] After
        '''
        children_mutated = []
        for child in children:
            index = random.randrange(0,len(children[0])-1)   
            child[index] = random.randrange(0,len(children[0])-1)
            children_mutated.append(child)
        population.extend(children_mutated)
        return children_mutated         

#endregion

#region SUCCESION_METHODS
    def tournament(self, fitness_list, population, best_percentage=0.3):
            cur_population = len(population)
            new_population = int(cur_population*best_percentage)
            #print("cur: {} new: {}".format(cur_population, new_population))
            while(len(population)>new_population and len(fitness_list)>new_population and new_population>4):
                del population[np.argmax(fitness_list)]
                del fitness_list[np.argmax(fitness_list)]
            return fitness_list, population

    def roulete(self, fitness_list, population, graph):
        summation= np.sum([goalFunction(graph.applyMask(i)) for i in population])
        u = random.random()
        if(u<0.3):
             u=0.3
        cur_population = len(population)
        new_population = int(cur_population*u)
        #print("cur: {} new: {} u: {}".format(cur_population, new_population, u))
        while(len(population)>new_population and len(fitness_list)>new_population and new_population>4):
            del population[np.argmax(fitness_list)]
            del fitness_list[np.argmax(fitness_list)]
        return fitness_list, population

#endregion