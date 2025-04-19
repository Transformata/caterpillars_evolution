# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 12:56:14 2022

@author: mikol
"""

from joblib import Parallel, delayed
import random
import glob
from datetime import datetime
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '\\'
path_results = os.path.join(repo_root, 'Experimental','Results') + '\\'
path_csv = os.path.join(repo_root, 'Simulations','Genetic_Algorithm') + '\\'
path_plot_fitness = os.path.join(repo_root, 'Simulations','fitness_functions') + '\\'

# path = "G:\Mój dysk\PNaF\Diamentowy_Grant_2017-2021\Swimming_caterpillars_evolution\wyniki\\"
# path = "G:\Mój dysk\PNaF\Diamentowy_Grant_2017-2021\Swimming_caterpillars_evolution\wyniki\symulacja_AG\tabelka\wykresy\\"
# path_plot_fitness = "G:/Mój dysk/PNaF/Diamentowy_Grant_2017-2021/Swimming_caterpillars_evolution/wyniki/symulacja_AG/average/"
# path_csv = "G:/Mój dysk/PNaF/Diamentowy_Grant_2017-2021/Swimming_caterpillars_evolution/wyniki/symulacja_AG/"

min_genes_mutated = 1
max_genes_mutated = 2
individuals_per_generation = 8

# elite True = 8 the best of all time 
elite = True

# selection techniqes, 0 - Roulette wheel, 1 - Rank
selection_technique = 1

# rank1_probability = rank1_probability_factor/(number of individuals in population)
#rank1_probability_factor = 3

# 14 400 possibilities
frequency_list = [float(i)/10. for i in range(1,51)]
length_list = [6,12,18]
dye_list = [0.2,1]
thickness_list = [50,90]
period_list = [1,2,3]
laserPower_list = [float(i)/2. for i in range(1,9)]
waveplate_list = [7.5*int(i)+30 for i in range(0,12)]
# right side of the film 0 down, 1 up
tail_list = [0,1]

#test
frequency_list = [float(i) for i in range(0,120)]
laserPower_list = [float(i) for i in range(0,120)]


parameters_list = [frequency_list, length_list, dye_list, thickness_list, 
                   period_list, laserPower_list, tail_list, waveplate_list]

colors = [i/individuals_per_generation for i in range(individuals_per_generation)]
#np.random.rand(individuals_per_generation)

class caterpillar:
    names = ["frequency", "length", "dye", "thickness", "period", "laserPower", "tail", "waveplate"]
    genes = [0 for i in range (0, len(names))]
    fitness = 0

    def __init__(self, parameters = [], fitness=0.):
        if len(parameters) == 0:
            for i in range(0, len(self.names)):
                self.genes[i] = random.choice(parameters_list[i])
            self.genes = np.copy(self.genes)

        else:
            for i in range(0, len(parameters)):
                self.genes[i] = parameters[i]
            self.genes = np.copy(self.genes)

        if type(fitness) == None:
            self.fitness = 0
        else:
            self.fitness = fitness

    def change_genes(self, parameters):
        for i in range(0, len(parameters)):
            if parameters[i] != 0:
                self.genes[i] = parameters[i]
            self.genes = np.copy(self.genes)

    def get_genes(self):
        return self.genes

    def print_genes(self):
        genes_string = ''
        for gene in self.genes:
            genes_string = genes_string + str(gene) + ' '
        print(genes_string)

    def get_copy(self):
        cater = caterpillar(list(self.get_genes()), self.fitness)
        return cater

def get_selection(sel_type):    
    if sel_type == 0:
        selection = 'roulette'
    elif sel_type == 1:
        selection = 'rank'
    return selection

def get_all_population(data_path):
    with open(data_path) as f:
        all_population = f.readlines()
        all_population = all_population[:-1]
        all_population = [x[:-1] for x in all_population if x.count(".")==len(parameters_list)+1]
    caterpillars_list = []
    for robot in all_population:
        parameters = list(map(float, (robot.split())))
        if len(parameters) > 1:
            cater = caterpillar(parameters[:-1], parameters[-1])
            caterpillars_list.append(cater.get_copy())
    return caterpillars_list

def get_last_generation(data_path):
    with open(data_path) as f:
        last_generation = f.readlines()[(-1-individuals_per_generation):]
        last_generation = last_generation[:-1]
        last_generation = [x[:-1] for x in last_generation]
    caterpillars_list = []
    for parameters in last_generation:
        parameters = list(map(float, (parameters.split())))

        cater = caterpillar(parameters[:-1], parameters[-1])
        caterpillars_list.append(cater.get_copy())
    return caterpillars_list

def get_2_generations(data_path):
    with open(data_path) as f:
        last_generation = f.readlines()[-20:]
        last_generation = last_generation[:-1]
        del last_generation[-11:-8]
        
        last_generation = [x[:-1] for x in last_generation]
    caterpillars_list = []
    for parameters in last_generation:
        parameters = list(map(float, (parameters.split())))

        cater = caterpillar(parameters[:-1], parameters[-1])
        caterpillars_list.append(cater.get_copy())
    return caterpillars_list

def remove_duplicates(caterpillar_list):
    result = 0
    new_caterpillar_list = [caterpillar_list[0].get_copy()]
    for i,cater in enumerate(caterpillar_list):
        if i != 0:
            genes = cater.get_genes()
            duplicate = False
            for new_caterpillar in new_caterpillar_list:
                if np.array_equiv(genes, new_caterpillar.get_genes()):
                    duplicate = True
                    result += 1
                    continue
            if duplicate:
                # print('duplicate detected')
                # print(i)
                result += 1
                duplicate = False
            else:
                new_caterpillar_list.append(cater)
    if result != 0:
        print('duplicate detected: {}'.format(result))
    return new_caterpillar_list, result

def crossover(cater1, cater2):
    genes1 = cater1.get_genes()
    genes2 = cater2.get_genes()
    indexes = np.random.choice(len(parameters_list),int(len(parameters_list)/2.),replace=False)
    new_genes1 = []
    new_genes2 = []
    for i in range(len(parameters_list)):
        if i in indexes:
            new_genes1.append(genes1[i])
            new_genes2.append(genes2[i])
        else:
            new_genes1.append(genes2[i])
            new_genes2.append(genes1[i])
    new_cater1 = caterpillar(np.copy(new_genes1))
    new_cater2 = caterpillar(np.copy(new_genes2))
    return new_cater1, new_cater2

def selection_probabilities(selection, caterpillars_list):
    cater_len = len(caterpillars_list)
    if selection == 0:
        speeds_sum = 0
        for cater in caterpillars_list:
            speeds_sum += cater.fitness
        probabilities = [caterpillars_list[i].fitness/speeds_sum for i in range(cater_len)]

    if selection == 1:
        rank1_probability_factor = cater_len**(1/3)
        rank1_probability = rank1_probability_factor/cater_len
        probabilities = [rank1_probability*((1-rank1_probability)**i)+((1-rank1_probability)**cater_len)/cater_len for i in range(cater_len)]

    return probabilities

def mutation_chance(mut_minmax, caterpillar, max_speed):
    speed = caterpillar.fitness
    x = speed/max_speed
    mutation_nr = mut_minmax[0] + x * (mut_minmax[1]-mut_minmax[0])
    return mutation_nr

def get_mutation_no(mut_minmax, caterpillar, max_speed):
    mut_chance = mutation_chance(mut_minmax, caterpillar, max_speed)
    mutation_nr = int(mut_chance)
    mutation_chance_reduced = mut_chance-mutation_nr
    if np.random.random() < mutation_chance_reduced:
        mutation_nr += 1
    return mutation_nr

def single_mutation(cater, mutation_nr):
    genes_list = cater.get_genes()
    cater_new = cater.get_copy()
    # draw parameters to mutate
    parameters_indexes = random.sample(range(len(genes_list)), mutation_nr)
    parameters_list_copy = [np.copy(parameters_list[i]) for i in parameters_indexes]
    for i in range(mutation_nr):
        j = parameters_indexes[i]
        parameters_list_copy[i] = np.delete(parameters_list_copy[i], np.where(parameters_list_copy[i] == genes_list[j]))
        genes_list[j] = random.choice(parameters_list_copy[i])
    cater_new.change_genes(genes_list)
    return cater_new

def mutation(mut_minmax, caterpillar1, caterpillar2, max_speed):
    cater1 = caterpillar1.get_copy()
    cater2 = caterpillar2.get_copy()

    mutation_nr = get_mutation_no(mut_minmax, cater1, max_speed)
    cater1 = single_mutation(cater1, mutation_nr)

    mutation_nr = get_mutation_no(mut_minmax, cater2, max_speed)
    cater2 = single_mutation(cater2, mutation_nr)

    return cater1, cater2

def check_for_duplicates(cater, caterpillar_list):
    duplicate = False
    for c in caterpillar_list:
        cater_genes = [round(float(i),1) for i in cater.get_genes()]
        c_genes = [round(float(i),1) for i in c.get_genes()]
        if np.array_equiv(cater_genes, c_genes):
            duplicate = True
    return duplicate

def test_duplicates(new_caterpillar_list):
    checked_duplicates_no = 0
    for c in new_caterpillar_list:
        for cater in new_caterpillar_list:
            if all(c.get_genes() == cater.get_genes()):
                checked_duplicates_no += 1
    if checked_duplicates_no != len(new_caterpillar_list):
        for c in new_caterpillar_list:
            c.print_genes()
            print(c.fitness)
        print(checked_duplicates_no)
        print("test exit")
        print("\n")
        exit(checked_duplicates_no)
    return

def mutate_duplicates(new_caterpillars_list, old_caterpillars_list):
    checked_caterpillars_list = old_caterpillars_list.copy()
    new_caterpillars_list_without_duplicates = []
    for i, cater in enumerate(new_caterpillars_list):
        c = cater.get_copy()
        while check_for_duplicates(c, checked_caterpillars_list):
            c = single_mutation(c, 1)
        checked_caterpillars_list.append(c.get_copy())
        new_caterpillars_list_without_duplicates.append(c.get_copy())
    test_duplicates(checked_caterpillars_list)
    return new_caterpillars_list_without_duplicates

def new_generation(individuals_per_generation, cater_list=[], AG_params=0):
    new_caterpillars_list = []
    caterpillars_list = cater_list.copy()

    if caterpillars_list == []:
        random.seed()
        for i in range(0, individuals_per_generation): 
            cater = caterpillar([])
            new_caterpillars_list.append(cater)
        #print("first generation created")

    else:
        caterpillars_list.sort(key=lambda x: x.fitness, reverse=True)
        if AG_params[0]:
            caterpillars_list = caterpillars_list[:8]
        probabilities = selection_probabilities(AG_params[1], caterpillars_list)

        max_speed = caterpillars_list[0].fitness

        for i in range(0,int(individuals_per_generation/2.)):

            # selection
            cater1, cater2 = np.random.choice(caterpillars_list, 2, replace=False, p=probabilities)

            # mutation
            mut_minmax = [AG_params[2], AG_params[3]]
            cater1, cater2 = mutation(mut_minmax, cater1, cater2, max_speed)

            # crossover
            new_cater1, new_cater2 = crossover(cater1, cater2)
            new_caterpillars_list.append(new_cater1.get_copy())
            new_caterpillars_list.append(new_cater2.get_copy())

    new_caterpillar_list = mutate_duplicates(new_caterpillars_list, cater_list)

    return new_caterpillar_list

def get_results(results_path):
    with open(results_path, "r") as f:
        previous_results = f.readlines()
    return previous_results

def write_generation(data_path, caterpillars_list, results_path=0):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")
    previous_parameters = ""

    if results_path == 0:
        f = open(data_path, "a")

    else:
        old_caterpillars_list = get_last_generation(data_path)

        with open(results_path, "a") as f:

            previous_results = get_results(results_path)
            previous_parameters = [" ".join(result.split()[:-1])+" " for result in previous_results]

            for cater in old_caterpillars_list:
                genes = cater.get_genes()
                genes_str = ""
                for gene in genes:
                    genes_str = genes_str + "{} ".format(gene)
                if not (genes_str in previous_parameters):
                    print(genes_str)
                    previous_parameters.append(genes_str)
                    line = genes_str + "{}".format(cater.fitness) + "\n"
                    previous_results.append(line)
                    f.write(line)

    with open(data_path, "a") as f:
        f.write("{} {}\n".format(today, time_now))

        line = ""
        for name in caterpillars_list[0].names:    
            line = line + name + " "
        line = line + "fitness\n"
        f.write(line)
        
        for cater in caterpillars_list:
            line = ""
            for gene in cater.get_genes():
                line = line + "{} ".format(gene)
            if len(previous_parameters) == 0:
                line = line + "{}\n".format(cater.fitness)
            else:
                if line in previous_parameters:
                    result = [result.split()[-1] for result in previous_results if line in result][0]
                    cater.fitness = result
                    line = line + "{}\n".format(cater.fitness)
                else: line = line + "{}\n".format(cater.fitness)
            f.write(line)
        f.write("\n")

def first_generation(individuals_per_generation, path):
    data_path = path + "parameters_.txt"
    write_generation(data_path, new_generation(individuals_per_generation))

def next_generation(individuals_per_generation, path, AG_params):
    random.seed()
    last_nr = "09"
    data_path = path + "optimization_{}.txt".format(last_nr)
    results_path = path + "results.txt"
    caterpillar_list = get_all_population(data_path)
    caterpillar_list, result = remove_duplicates(caterpillar_list)
    new_caterpillar_list = new_generation(individuals_per_generation, caterpillar_list, AG_params)
    write_generation(data_path, new_caterpillar_list, results_path)
    return

def get_parameters_range():
    parameters_range_list = [[min(parameters_value), max(parameters_value)] for parameters_value in parameters_list]
    return parameters_range_list

def get_parameters_linspace(shape):
    parameters_range_list = get_parameters_range()
    parameters_linspace_list = [np.linspace(parameters_range_list[i][0],parameters_range_list[i][1], shape) for i in range (len(parameters_range_list))]
    return parameters_linspace_list

def fitness_function_1D(p, parameter_range, p_min, center, standard_deviation_factor):
    standard_deviation = parameter_range*standard_deviation_factor
    result = np.exp(-1*(p-0.75*parameter_range-p_min)**2/(2*standard_deviation**2))/(standard_deviation*(2*np.pi)**0.5)
    # result_max = 1/(standard_deviation*(2*np.pi)**0.5)
    """if p >= center:
        result = np.exp(-1*(p-0.75*parameter_range-p_min)**2/(2*standard_deviation**2))/(standard_deviation*(2*np.pi)**0.5)
    if p < center:
        result = 0.5*np.exp(-1*(p-0.25*parameter_range-p_min)**2/(2*standard_deviation**2))/(standard_deviation*(2*np.pi)**0.5)"""
    # result = result/result_max
    return result

def fitness_function_1D_max(parameter_list, parameter_range, p_min, center, standard_deviation_factor):
    result = 0
    result_new = 0
    for p in parameter_list:
        result_new = fitness_function_1D(p, parameter_range, p_min, center, standard_deviation_factor)
        if result_new > result:
            result = result_new
    return result

def fitness_function(parameters, parameters_range_list, standard_deviation_factor):
    result = 0
    for i in range(len(parameters)):
        parameter_list = parameters_range_list[i]
        p = parameters[i]
        p_min = min(parameter_list)
        p_max = max(parameter_list)
        center = (p_max + p_min)/2
        parameter_range = p_max - p_min
        result_1D = fitness_function_1D(p, parameter_range, p_min, center, standard_deviation_factor)
        #result_max = fitness_function_1D_max(parameter_list, parameter_range, p_min, center, standard_deviation_factor)
        result += result_1D#/result_max

    return result

def fitness_function_max_7D(parameters_range_list, standard_deviation_factor):
    result = 0
    for i in range(len(parameters_range_list)):
        parameters = parameters_range_list[i]
        p_min = min(parameters)
        p_max = max(parameters)
        center = (p_max + p_min)/2
        parameter_range = p_max - p_min

        result_p = 0
        result_p_max = 0
        for p in parameters:
            result_p = fitness_function_1D(p, parameter_range, p_min, center, standard_deviation_factor)
            if result_p > result_p_max:
                result_p_max = result_p
        result += result_p_max
    return result

def plot_fitness_function_7D(path, index_x, index_y, plot_args, standard_deviation_factor, maxZ):
    parameters_range_list_short = plot_args[0]
    x_space = plot_args[1]
    y_space = plot_args[2]
    Z = plot_args[4]

    plt.figure(figsize=(8, 8), dpi=100)
    plt.xlim(min(parameters_range_list_short[0]), max(parameters_range_list_short[0]))
    plt.ylim(min(parameters_range_list_short[1]), max(parameters_range_list_short[1]))
    plt.contourf(x_space,y_space,Z,100)
    plt.title('global maximum: {}'.format(maxZ))
    plt.savefig(path + 'fitness_function_sigma_{}.png'.format(standard_deviation_factor), dpi = 300)
    plt.show()
    plt.close()

def count_fitness_value(caterpillars_list, parameters_range_list, standard_deviation_factor, index_x=-1, index_y=-1,):
    new_caterpillars_list = []
    average_fitness = 0

    for cater in caterpillars_list:
        caterpillar_with_fitness = cater.get_copy()
        genes_all = cater.genes.copy()
        if index_x != -1:
            genes = [genes_all[index_x],genes_all[index_y]]
            parameters_range_list_short = [parameters_range_list[index_x], parameters_range_list[index_y]]
        else:
            genes = genes_all
            parameters_range_list_short = parameters_range_list
        caterpillar_with_fitness.fitness = fitness_function(genes, parameters_range_list_short, standard_deviation_factor)
        #print(caterpillar_with_fitness.fitness)
        average_fitness += caterpillar_with_fitness.fitness
        new_caterpillars_list.append(caterpillar_with_fitness.get_copy())
    average_fitness = average_fitness/individuals_per_generation
    return new_caterpillars_list, average_fitness

def get_plot_args(parameters_range_list, index_x, index_y, shape, standard_deviation_factor):
    parameters_range_list_short = [parameters_range_list[index_x],parameters_range_list[index_y]]
    parameters_linspace = get_parameters_linspace(shape)
    x_space = parameters_linspace[index_x]
    y_space = parameters_linspace[index_y]

    #no_list = [int(1+(parameter_range[1]-parameter_range[0])/0.01) for parameter_range in parameters_range_list_short]
    #return [parameters_range_list_short, x_space, y_space, no_list]
    
    z = np.array([fitness_function([x,y], parameters_range_list_short, standard_deviation_factor) for y in y_space for x in x_space])
    Z = z.reshape(shape, shape)
    return [parameters_range_list_short, x_space, y_space, shape, Z]

#nie ma zapisywania do pliku
def plot_generation(path, caterpillars_list, index_x, index_y, plot_args):
    parameters_range_list_short = plot_args[0]
    x_space = plot_args[1]
    y_space = plot_args[2]
    Z = plot_args[4]

    parameters_list_x = np.array([])
    parameters_list_y = np.array([])
    for cater in caterpillars_list:
        caterpillar_parameters = cater.genes
        x = caterpillar_parameters[index_x]
        y = caterpillar_parameters[index_y]
        parameters_list_x = np.append(parameters_list_x, x)
        parameters_list_y = np.append(parameters_list_y, y)

    plt.figure(figsize=(8, 8), dpi=100)
    plt.xlim(parameters_range_list_short[0])
    plt.ylim(parameters_range_list_short[1])
    plt.contourf(x_space,y_space,Z,100)
    plt.scatter(parameters_list_x, parameters_list_y, marker='o', c=colors, s=1000)
    plt.show()
    plt.close()

def plot_fitness_function(path, index_x, index_y, plot_args, standard_deviation_factor):
    parameters_range_list_short = plot_args[0]
    x_space = plot_args[1]
    y_space = plot_args[2]
    Z = plot_args[4]
    maxZ = np.amax(Z)

    plt.figure(figsize=(8, 8), dpi=100)
    plt.xlim(parameters_range_list_short[0])
    plt.ylim(parameters_range_list_short[1])
    plt.contourf(x_space,y_space,Z,100)
    plt.title('global maximum: {}'.format(maxZ))
    plt.savefig(path + 'fitness_function__sigma_factor_{}.png'.format(standard_deviation_factor), dpi = 300)
    plt.show()
    plt.close()
    return maxZ

#useless
def png_to_gif():

    # Create the frames
    frames = []
    imgs = glob.glob("*.png")
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)
 
    # Save into a GIF file that loops forever
    frames[0].save('png_to_gif.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=300, loop=0)

def plot_generation_results(AG_params, path, generations_no_list, max_fitness_list, average_fitness_list, standard_deviation, version):
    plt.plot(generations_no_list, max_fitness_list)
    plt.plot(generations_no_list, average_fitness_list)
    plt.title('measured maximum: {}'.format(np.amax(max_fitness_list)))
    name = 'genetic_algorithm_'
    selection = get_selection(AG_params[1])
    name += 'elite-{}_{}_mingenmut{}_maxgenmut{}_standev{}_v{:02d}'.format(AG_params[0], selection, AG_params[2], AG_params[3], standard_deviation, version)
    plt.savefig(path + name + '.png', dpi = 300)
    plt.show()
    plt.close()

def plot_generation_average_results(AG_params, path, generations_no_list, max_fitness_list, max_fitness_list_errorbars, average_fitness_list, average_fitness_list_errorbars, standard_deviation, versions, maxZ):
    #max_fitness_list_average = max_fitness_list/versions
    #average_fitness_list_average = average_fitness_list/versions
    plt.errorbar(generations_no_list, max_fitness_list, yerr=max_fitness_list_errorbars, elinewidth = 6)
    plt.errorbar(generations_no_list, average_fitness_list, yerr=average_fitness_list_errorbars, elinewidth = 3)
    plt.xlim([1,max(generations_no_list)])
    plt.ylim([0,maxZ])
    plt.axvline(x=5, c="r",linestyle="-")
    plt.axhline(y=2.5, c="r",linestyle="-")
    plt.title('measured maximum: {}'.format(np.amax(max_fitness_list)))
    name = 'genetic_algorithm_average_results_'
    selection = get_selection(AG_params[1])
    name += 'elite-{}_{}_minmut{:.1f}_maxmut{:.1f}_standev{}_v{:02d}'.format(AG_params[0], selection, AG_params[2], AG_params[3], standard_deviation, versions)
    plt.savefig(path + name + '.png', dpi = 300)
    plt.show()
    plt.close()

def simulation(individuals_per_generation, AG_params, parameters_range_list, index_x, index_y, generations_no, shape, standard_deviation_factor, version = 0):
    # plot_args = get_plot_args(parameters_range_list, index_x, index_y, shape, standard_deviation_factor)
    # Z = plot_args[4]
    generations_no_list = np.array([])
    max_fitness_list = np.array([])
    average_fitness_list = np.array([])
    caterpillar_list_all = []

    for i in range(generations_no):
        if i == 0:
            new_caterpillar_list = new_generation(individuals_per_generation)
            new_caterpillar_list, average_fitness = count_fitness_value(new_caterpillar_list, parameters_range_list, standard_deviation_factor, index_x, index_y)
            for cater in new_caterpillar_list:
                caterpillar_list_all.append(cater.get_copy())
            
        else:
            new_caterpillar_list = new_generation(individuals_per_generation, caterpillar_list_all, AG_params)
            new_caterpillar_list, average_fitness = count_fitness_value(new_caterpillar_list, parameters_range_list, standard_deviation_factor, index_x, index_y)
            for cater in new_caterpillar_list:
                caterpillar_list_all.append(cater.get_copy())
            # caterpillar_list_all, result = remove_duplicates(caterpillar_list_all)

        new_caterpillar_list.sort(key=lambda x: x.fitness, reverse=True)
        caterpillar_list_all.sort(key=lambda x: x.fitness, reverse=True)

        max_fitness_list = np.append(max_fitness_list, new_caterpillar_list[0].fitness)        
        average_fitness_list = np.append(average_fitness_list, average_fitness)
        generations_no_list = np.append(generations_no_list, i+1)

    test_duplicates(caterpillar_list_all)
    return generations_no_list, max_fitness_list, average_fitness_list

def append_list_to_string(string, lst, separator=','):
    lst_str = separator.join(map(str, lst))
    return string + separator + lst_str

def append_result_to_csv(AG_params, path_csv, data_list, standard_deviation, versions):
    lines = []
    for i,p in enumerate(AG_params):
        if p[1] == False:
            selection = 'roulette'
        elif p[1] == True:
            selection = 'rank'
        new_line = 'genetic algorithm;{};{:02d};{};{};{:.1f};{:.1f}'.format(standard_deviation, versions, p[0], selection, p[2], p[3])
        for data in data_list[i]:
            new_line = append_list_to_string(new_line,data,';')
        lines.append(new_line)
    with open(path_csv + 'results_{}.csv'.format(standard_deviation),'a') as f:
        for new_line in lines:
            f.write(new_line)
            f.write("\n")
    return

def get_AG_params_list(min_mut_range, max_mut_range):
    AG_params_list = []
    for i in [True, False]:
        for j in [0, 1]:
            for k in np.arange(min_mut_range[0], min_mut_range[1], min_mut_range[2]):
                for m in np.arange(max(max_mut_range[0],k), max_mut_range[1], max_mut_range[2]):
                    AG_params_list.append([i, j, round(k,2), round(m,2)])
    return AG_params_list

def generate_data_and_plot_fitness_function_8D(path, parameters_list, parameters_list_plot, index_x, index_y, shape, standard_deviation_factor):
    maxZ = fitness_function_max_7D(parameters_list, standard_deviation_factor)
    plot_args = get_plot_args(parameters_list_plot, index_x, index_y, shape, standard_deviation_factor)
    plot_fitness_function_7D(path, index_x, index_y, plot_args, standard_deviation_factor, maxZ)
    return maxZ

def do_simulation(path_csv, path_plot_fitness, individuals_per_generation, min_mut_range, max_mut_range, parameters_list, parameters_list_plot, index_x, index_y, generations_no, shape, standard_deviation_factor, versions):
    generate_data_and_plot_fitness_function_8D(path_plot_fitness, parameters_list, parameters_list_plot, index_x, index_y, shape, standard_deviation_factor)
    AG_params_list = get_AG_params_list(min_mut_range, max_mut_range)
    data_list = []
    generations_no_list = []
    for AG_params in AG_params_list:
        max_fitness_list = []
        average_fitness_list = []

        selection = get_selection(AG_params[1])
        print('elite: {}  selection: {}  min gen mut: {:.1f}  max gen mut: {:.1f}'.format(AG_params[0], selection, AG_params[2], AG_params[3]))
    
        # items = [(AG_params, path, parameters_list, index_x, index_y, generations_no, shape, standard_deviation_factor, i+1) for i in range(versions)]
    
        results_list = Parallel(n_jobs=11)(delayed(simulation)(individuals_per_generation, AG_params, parameters_list, index_x, index_y, generations_no, shape, standard_deviation_factor, i+1) for i in range(versions))
        max_fitness_list = np.array([i[1] for i in results_list])
        average_fitness_list = np.array([i[2] for i in results_list])
        max_fitness_list_average = np.average(max_fitness_list, axis = 0)
        max_fitness_list_standard_deviations = np.std(max_fitness_list, axis = 0)
        average_fitness_list_average = np.average(average_fitness_list, axis = 0)
        average_fitness_list_standard_deviations = np.std(average_fitness_list, axis = 0)
        generations_no_list.append(results_list[-1][0].copy())

        data_list.append([max_fitness_list_average, max_fitness_list_standard_deviations, average_fitness_list_average, average_fitness_list_standard_deviations])
    

    append_result_to_csv(AG_params_list, path_csv, data_list, standard_deviation_factor, versions)
        
        # IT WILL PLOT ONLY ONE CHART (FIRST PROBABLY) WHEN UNCOMMENTED
        # max_fitness_list_average, max_fitness_list_standard_deviations, average_fitness_list_average, average_fitness_list_standard_deviations = data_list[i]
        # plot_generation_average_results(AG_params, path_plot_fitness, generations_no_list[i],
        #                                 max_fitness_list_average, max_fitness_list_standard_deviations,
        #                                 average_fitness_list_average, average_fitness_list_standard_deviations,
        #                                 standard_deviation_factor, versions, maxZ)

    print('simulation done')
    return


individuals_per_generation = 8

frequency_list = [float(i)/10. for i in range(1,51)]
length_list = [6,12,18]
dye_list = [0.2,1]
thickness_list = [50,90]
period_list = [1,2,3]
laserPower_list = [float(i)/2. for i in range(1,9)]
waveplate_list = [7.5*int(i)+30 for i in range(0,12)]
# right side of the film 0 down, 1 up
tail_list = [0,1]
frequency_list_plot = [float(i) for i in range(0,120)]
laserPower_list_plot = [float(i) for i in range(0,120)]

parameters_list = [frequency_list, length_list, dye_list, thickness_list, 
                   period_list, laserPower_list, tail_list, waveplate_list]
parameters_list_plot = [frequency_list_plot, length_list, dye_list, thickness_list, 
                        period_list, laserPower_list_plot, tail_list, waveplate_list]

index_x = -1
index_y = -1
index_x_plot = 0
index_y_plot = 5
#point no on each both axis
shape = 120

min_mut_start = 0.0 # 0.4
max_mut_start = 0.0 # 2.5

min_mut_delta = 0.1
max_mut_delta = 0.1

min_mut_max = 2.
max_mut_max = 3.

min_mut_range = [min_mut_start, min_mut_max+min_mut_delta, min_mut_delta]
max_mut_range = [max_mut_start, max_mut_max+max_mut_delta, max_mut_delta]

#when stop
generations_no = 5
#how many times rerun simulation
versions = 1

# AG_params_list = get_AG_params_list(min_mut_range, max_mut_range)
# simulation(individuals_per_generation, AG_params_list[0], path, parameters_list, -1, -1, 5, shape, standard_deviation_factor, version = 100)

print(get_parameters_range())

# standev_list = [0.02,0.04,0.06,0.08,0.1,0.2,0.3,0.4,0.5]
standev_list = [0.05,0.1,0.25,0.5]
for standev in standev_list[:1]:
    do_simulation(path_csv, path_plot_fitness, individuals_per_generation, min_mut_range, max_mut_range, parameters_list, parameters_list_plot, index_x, index_y, generations_no, shape, standev, versions)


#first_generation(individuals_per_generation, path)

#next_generation(individuals_per_generation, path, AG_params)