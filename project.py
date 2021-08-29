# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 20:50:34 2018

@author: shayanSM
"""
import math
import random
import matplotlib.pyplot as plt
"""
Artificial Intelligence
Computer Assignment NO.2
student : Shayan Shafiee Moghadam
studentID : 810994076
major : Industrial engineering
"""
"""
object airport contains:
    1) name of the airport
    2) latitude
    3) longitude
"""
class Airport(object):
    
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        
    def __str__(self):
        return self.name + " \n(" + str(self.latitude) + " , " + str(self.longitude) + " )"


"""
object airline contains:
    1) id
    2) number of passengers
    3) origin
    4) destination
    5) distance
"""
class Airline(object):
    
    ID = 1
    # id = 0 is for not an airline

    def __init__(self, passangers, src, des):
        self.id = Airline.ID
        Airline.ID += 1
        self.passengers = passangers
        self.src = src
        self.des = des
        coords_1 = (airports[src].latitude, airports[src].longitude)
        coords_2 = (airports[des].latitude, airports[des].longitude)
        self.distance = Airline.distance(coords_1, coords_2)
    
    @staticmethod
    def distance(origin, destination):
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6371  # km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c
        return d
    
    def __str__(self):
        return 'airline number : ' + str(self.id) + " from " +self.src+ " to " +self.des+ "\n number of passengers : " + str(self.passengers) + "\n distance : " + str(self.distance)


"""
object aircraft contains:
    1) id
    2) name
    3) capacity
    4) price
    5) per seat price
    6) per seat loss
    7) max available number
"""
class Aircraft(object):
    
    chromosomeLen = 0 
    
    def __init__(self, name, capacity, price, profit, loss, number):
        self.name = name
        self.capacity = capacity
        self.price = price
        self.profit = profit
        self.loss = loss
        self.number = number
        Aircraft.chromosomeLen += number
    
    def __str__(self):
        return 'aircraft '+ self.name + "\ncapacity : " + str(self.capacity) + "\nprice : " + str(self.price) + "\nprofit: " + str(self.profit) + "    loss: " + str(self.loss) 
     

"""
object decision variable contains:
    1) ij : airline
    2) k : aircraft
    3) value 
"""
class decision_Variable(object):
    
    def __init__(self,ij,k,value):
        self.ij = ij
        self.k = k
        self.value = value
        
    def haveExisted(self,ij,k):
        return (ij == self.ij) and (k == self.k)
    
    def __str__(self):
        return "X ( " + str(self.ij) + " , " + self.k  + " ) = " + str(self.value)


"""
a function which returns the sign of a number
"""
def sign(number):
    if number > 0:
        return 1
    return 0


"""
object individual
all chromosome and its fitness stores in this function
so there is list to store the chromosome
and a function to calculate the fitness function
it also has s static method to create a chromosome randomly
most importantly it contains to important functions:
    mutation and crossover
finally, it has a method to return a string for the output of GA
based on what you have stated in the computer assignment pdf
"""
class Individual(object):
    
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = Individual.fitness_function(chromosome) 
    
    @staticmethod
    def calculatorZ(chromosome):
        z = budget 
        for k in range(len(chromosome)):
            z -= aircrafts[planes[k]].price*sign(chromosome[k])
        return z
    
    @staticmethod
    def createX(chromosome):
        X = dict()
        for i in range(len(chromosome)):
            k = planes[i]
            ij = chromosome[i]
            if ij != 0:
                if ij in X.keys():
                    state = False
                    for j in X[ij]:
                        if j.haveExisted(ij,k):
                            state = True
                            j.value += 1       
                    if not state:
                        j = decision_Variable(ij,k,1)
                        X[ij].append(j)
                else:
                    X[ij] = []
                    j = decision_Variable(ij,k,1)
                    X[ij].append(j)
        return X
    
    @staticmethod
    def balanceVariables(lst,T):
        d = round(T / len(lst))
        for i in lst:
            i.value = d
        return lst

    @staticmethod
    def fitness_function(chromosome):
        z = budget 
        for k in range(len(chromosome)):
            z -= aircrafts[planes[k]].price*sign(chromosome[k])
        if z < 0:
            return z
        X = Individual.createX(chromosome)
        Y = dict()
        for ij in X.keys():
            Y[ij] = []
            for var in X[ij]:
                k = var.k
                value = var.value
                value *= aircrafts[k].capacity
                newVar = decision_Variable(ij,k,value)
                Y[ij].append(newVar)
        for ij in Y.keys():
            sum = 0
            for var in Y[ij]:
                sum += var.value
            if sum > airlines[ij].passengers:
                Y[ij] = Individual.balanceVariables(Y[ij],airlines[ij].passengers) 
        z = 0
        for ij in Y.keys():
            for k in range(len(Y[ij])):
                z += (Y[ij][k].value*airlines[ij].distance*aircrafts[Y[ij][k].k].profit)/100
                z -= (((X[ij][k].value*aircrafts[Y[ij][k].k].capacity) - Y[ij][k].value )*airlines[ij].distance*aircrafts[Y[ij][k].k].loss)/100
        return z
    
    @staticmethod
    def creating_chromosome():
        chromosome = [0] * Aircraft.chromosomeLen
        while 0 in chromosome:
            k = random.choice(range(Aircraft.chromosomeLen))
            ij = random.choice(range(len(airlines.keys())+1))
            chromosome[k] = ij
            if Individual.calculatorZ(chromosome) < 0:
                chromosome[k] = 0
                return chromosome
        return chromosome
    
    def __add__(self, other):
        #uniform crossover
        parent1 = self.chromosome
        parent2 = other.chromosome
        children1, children2 = [] , []
        for i in range(len(parent1)):
            prob = random.random() 
            if prob < 0.5:
                children1.append(parent1[i])
                children2.append(parent2[i])
            else:
                children1.append(parent2[i])
                children2.append(parent1[i])
        offspring1 = Individual(children1)
        offspring2 = Individual(children2)
        return offspring1, offspring2
    
    def mutation(self):#__add__
        chromosome = self.chromosome
        rnd1 = random.choice(range(len(chromosome)))
        rnd2 = random.choice(range(len(chromosome)))
        while rnd2 == rnd1:
            rnd2 = random.choice(range(len(chromosome)))
        if rnd1 > rnd2:
            rnd1 , rnd2 = rnd2 , rnd1
        mutate = chromosome[rnd1:rnd2]
        mutate.reverse()
        chromosome[rnd1:rnd2] = mutate
        individual = Individual(chromosome)
        return individual
    
    
    def __str__(self):
        cost = budget - Individual.calculatorZ(self.chromosome)
        profit = self.fitness
        X = Individual.createX(self.chromosome)
        output = "cost " + str(cost) + "\nprofit "+ str(profit)
        show = dict()
        for ij in X.keys():
            lst = [airlines[ij].src , airlines[ij].des]
            lst.sort()
            [src , des] = lst
            airlineKey = src + " " + des
            if airlineKey in show.keys():
                for var in X[ij]:
                    state = False
                    for j in show[airlineKey]:
                        if (j.haveExisted(ij+1,var.k) or j.haveExisted(ij-1,var.k)):
                            state = True
                            j.value += 1
                    if not state:
                       show[airlineKey] += [var]
            else:
                show[airlineKey] = X[ij]
        for key in sorted(show):
            lst = [key]
            for var in show[key]:
                lst.append(var.k)
                lst.append(var.value)
            string = " ".join(str(x) for x in lst)
            output +=  ("\n" + string)
        return output
            

"""
this object will be used to store individuals as population 
for aading an individual into the population --> insert
for deleting individuals form population(who have bad fitness function)
                                                -->delete
for showing the best individual from the population based on its 
                                fitness functions --> best
"""
class PriorityQueue(object): 
    
    def __init__(self): 
        self.queue = [] 
  
    def __str__(self): 
        return ' '.join([str(i) for i in self.queue]) 
   
    def insert(self, individual): 
        self.queue.append(individual) 
  
    # return the best individual with largest fitness function  
    def best(self): 
            max = 0
            for i in range(len(self.queue)): 
                if self.queue[i].fitness > self.queue[max].fitness: 
                    max = i 
            item = self.queue[max] 
            return item
    
    # delete individual with least fitness function
    def delete(self):
            min = 0
            for i in range(len(self.queue)): 
                if self.queue[i].fitness < self.queue[min].fitness: 
                    min = i 
            del self.queue[min] 
            
    def getQueue(self):
        return self.queue
    
    
"""
dictionaries for saving inormations
"""
airports = dict()
airlines = dict()
aircrafts = dict()
planes = dict()
"""
getting input from text
"""    
def get_text():
    
    airporttxt = open("airports.txt","r")
    airportInformations = airporttxt.readlines()
    for i in airportInformations:
        string = i.split(" ")
        name = str(string[0])
        latitude = float(string[1])
        longitude = float(string[2])
        newAirport = Airport(name,latitude,longitude)
        airports [name] = newAirport

    passengerstxt = open("passengers.txt","r")
    passengersInformations = passengerstxt.readlines()
    for i in passengersInformations:
        string = i.split(" ")
        airport1 = str(string[0])
        airport2 = str(string[1])
        passangers12 = int(string[2])
        passangers21 = int(string[3])
        if passangers12 != 0:
            newAirline = Airline(passangers12,airport1,airport2)
            airlines[newAirline.id] = newAirline
        if passangers21 != 0:
            newAirline = Airline(passangers21,airport2,airport1)
            airlines[newAirline.id] = newAirline
    
    aircrafttxt = open("aircrafts.txt","r")
    aircraftInformations = aircrafttxt.readlines()
    planeID = 0
    for i in aircraftInformations:
        string = i.split(" ")
        name = str(string[0])
        capacity = int(string[1])
        price = float(string[2])
        profit = float(string[3])
        loss = float(string[4])
        number = int(string[5])
        newAircraft = Aircraft(name, capacity, price, profit, loss, number)
        aircrafts [newAircraft.name] = newAircraft
        for i in range(number):
            planes[planeID] = name
            planeID += 1


"""
function for creating initial population
"""
def initial_pop():
    population = PriorityQueue()
    for i in range(pop_number):
        individual = Individual (Individual.creating_chromosome())
        population.insert(individual)
    return population


"""
function for selecting individuals from population randomly
"""
def selection(population, number):
    rnd1 = random.choice(range(len(population)))
    Tuple = (population[rnd1],)
    if number == 1:
        return population[rnd1]
    if number > 1:
        rnd2 = random.choice(range(len(population)))
        while rnd2 == rnd1:
            rnd2 = random.choice(range(len(population)))
        Tuple = Tuple + (population[rnd2],)
    return Tuple


"""
when the GA whould stop?
"""
def stop_criteria(iteration):
    if iteration > 100:
        return True
    return False


"""
the main genetic algorithm 
"""
def Genetic_Algorithm():
    population = initial_pop() # population is a PriorityQueue
    iteration = 0
    crossover_number = round(crossover_percent*pop_number/2)
    mutation_number = round(mutation_percent*pop_number)
    ans = [population.best()]
    while not (stop_criteria(iteration)):
        iteration += 1
        new_population = PriorityQueue()
        populationList = population.getQueue()
        # crossover
        for i in range(crossover_number):
            p1 , p2 = selection(populationList,2)
            c1 , c2 = p1 + p2
            new_population.insert(c1)
            new_population.insert(c2)
        # mutation
        for i in range(mutation_number):
            p = selection(populationList,1)
            c = p.mutation()
            new_population.insert(c)
        # mixing old and new population
        new_populationList = new_population.getQueue()
        for i in new_populationList:
            population.insert(i)
        # creating new population
        while len(population.getQueue()) > pop_number:
            population.delete()
        ans += [population.best()]
    return ans


"""
main code
"""
get_text()
#budget = 200000
budget = float(input("please enter the total budget: "))
pop_number = 100
mutation_percent = 0.3
crossover_percent = 0.8
best_answer = 0
default = 1
for i in range(default):
    answer = Genetic_Algorithm()
    x_axis = range(len(answer))
    y_axis = []
    for x in answer:
        y_axis += [x.fitness]
    plt.plot(x_axis,y_axis)
    plt.title('improvement of fitness function during running genetinc algorithm')
    plt.xlabel('iteration')
    plt.ylabel('ptofit')
    if best_answer < answer[-1].fitness:
        best_answer = answer[-1].fitness
        output = answer[-1]
print(output)
print("""\n\n\n\tthis genetic algorithm is running with following parameters
        for better results, you can increase them in the code""")
print('number of population : ' + str(pop_number) + '\t\t\t\t\t line 462')
print("number of iteration inside the genetic algorithm : 100 \t\t line 416")
print('number of repeating genetic algorithm : ' + str(default) + '\t\t\t line 466')
print('crossover percentage : ' + str(crossover_percent) + '\t\t\t\t\t line 464')
print('mutation percentage : ' + str(mutation_percent) + '\t\t\t\t\t line 463')