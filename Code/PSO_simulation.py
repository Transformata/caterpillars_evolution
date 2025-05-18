from joblib import Parallel, delayed
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# checked
class sum_of_Gaussian_functions:

    def __init__(self, p_min, p_max, standard_deviation):
        self.parameters_range = np.copy(p_max-p_min)
        self.params_min = p_min
        self.standard_deviation = self.parameters_range*standard_deviation

    def calculate_function(self, x):
        Gaussian_functions_array = np.exp(-1*(x-0.75*self.parameters_range-self.params_min)**2/
                                          (2*self.standard_deviation**2))/(self.standard_deviation*(2*np.pi)**0.5)
        return np.sum(Gaussian_functions_array, axis=1)

class simulation_PSO:

    def __init__(self, parameters, parameters_names, parameters_list, parameters_min, parameters_max, PSO_params, fitness_function, 
                 iteration_no = 1, iteration_no_max=5, velocities = [], parameters_best = [], fitness_best = []):
        self.parameters = np.round(np.copy(parameters), 1)
        self.waveplate_index = np.where(np.array(parameters_names) == "waveplate")[0][0]
        self.parameters_list = parameters_list
        self.parameters_list_pd = pd.DataFrame(parameters_list)
        self.parameters_list_np = self.parameters_list_pd.to_numpy()
        self.delta_parameters = np.round(np.abs(self.parameters_list_pd.T.to_numpy()[1] - self.parameters_list_pd.T.to_numpy()[0]),1)
        self.p_min = parameters_min
        self.p_max = parameters_max
        self.parameters_no = len(self.p_min)
        self.parameters_range = np.round((self.p_max - self.p_min)/self.delta_parameters + 1)
        self.w = PSO_params[0]
        self.c1 = PSO_params[1]
        self.c2 = PSO_params[2]
        self.fitness_function = fitness_function
        self.fitness = np.copy(fitness_function(self.parameters))
        self.velocities = np.copy(velocities)
        if iteration_no == 1:
            self.parameters_best = np.copy(self.parameters)
            self.fitness_best = np.copy(self.fitness)
            self.fitness_global_best = -np.inf
            self.update_global_best()
        else:   
            self.parameters_best = np.copy(parameters_best)
            self.fitness_best = np.copy(fitness_best)
            self.update_global_best()
        self.iteration_no = iteration_no
        self.iteration_no_max = iteration_no_max
        self.caterpillars_no = len(parameters)
        self.remove_duplicates(PSO=False)
        return

    # checked
    def reduce_velocities(self, index=[]):
        if len(index) == 1:
            i = index[0]
            where_limit, = np.where(np.abs(self.velocities[i]) > self.p_max-self.p_min)
            if(len(where_limit) != 0):
                where_limit = np.delete(where_limit, np.where(where_limit==self.waveplate_index))
                self.velocities[i][where_limit] = (np.sign(self.velocities[i])*(self.p_max-self.p_min))[where_limit]
        else:
            if len(index) == 0:
                i = np.arange(self.caterpillars_no)
            else:
                i = np.copy(index)
            rows, cols = np.where(np.abs(self.velocities[i]) > self.p_max-self.p_min)
            if len(rows) != 0:
                rows = np.delete(rows, np.where(cols==self.waveplate_index))
                cols = np.delete(cols, np.where(cols==self.waveplate_index))
                self.velocities[rows,cols] = (np.sign(self.velocities[i])*(self.p_max-self.p_min))[rows,cols]
        return

    # checked
    def update_velocities(self): 
        r1 = np.random.random(self.caterpillars_no)
        r1 = np.tile(r1[:, None], (1, self.parameters_no))
        r2 = np.random.random(self.caterpillars_no)
        r2 = np.tile(r2[:, None], (1, self.parameters_no))
        if self.iteration_no == 1:
            self.velocities = self.c1*r1*(self.parameters_best-self.parameters) + self.c2*r2*(self.param_global_best-self.parameters)
        else:
            self.velocities = self.w*self.velocities + self.c1*r1*(self.parameters_best-self.parameters) + self.c2*r2*(self.param_global_best-self.parameters)
        if self.iteration_no == 1 or (self.w == 0 and np.amax(self.fitness) == self.fitness_global_best):
            fitness_global_best_index = np.where(self.fitness_best == self.fitness_global_best)[0][0]
            self.velocities[fitness_global_best_index] = np.random.uniform(-1., 1., self.parameters_no)*(self.p_max-self.p_min)#tutaj było 0.1
        self.reduce_velocities()
        return

    # checked
    def boundary_conditions(self, index = []):
        p_i = self.waveplate_index
        pmin = self.p_min[p_i]
        pmax = self.p_max[p_i]
        if len(index) == 1:
            i = index[0]
            p_copy = np.copy(self.parameters[i])
            if p_copy[p_i] > pmax or p_copy[p_i] < pmin:
                p_range = pmax - pmin + self.delta_parameters[p_i]
                p_copy[p_i] = p_copy[p_i] - np.floor((p_copy[p_i] - pmin)/p_range)*p_range
            self.parameters[i] = p_copy
        else:
            if len(index) == 0:
                i = np.arange(self.caterpillars_no)
            else:
                i = np.copy(index)
            p_copy_T = np.copy(self.parameters[i].T)
            where_change, = np.where( (p_copy_T[p_i] > pmax) + (p_copy_T[p_i] < pmin) )
            if len(where_change) > 0:
                p_to_change = np.copy(p_copy_T[p_i][where_change])
                p_range = pmax - pmin + self.delta_parameters[p_i]
                p_to_change = p_to_change - np.floor((p_to_change - pmin)/p_range)*p_range
                p_copy_T[p_i][where_change] = p_to_change
                self.parameters[i]= p_copy_T.T
        return

    # checked
    def reduce_parameters(self, index=[]):
        if len(index) == 1:
            i = index[0]
            p_copy = np.copy(self.parameters[i])
            where_limit, = np.where(p_copy > self.p_max)
            where_limit = np.delete(where_limit, np.where(where_limit==self.waveplate_index))
            p_copy[where_limit] = np.copy(self.p_max[where_limit])
            where_limit, = np.where(p_copy < self.p_min)
            where_limit = np.delete(where_limit, np.where(where_limit==self.waveplate_index))
            p_copy[where_limit] = np.copy(self.p_min[where_limit])
            self.parameters[i] = p_copy
        else:
            if len(index) == 0:
                i = np.arange(self.caterpillars_no)
            else:
                i = np.copy(index)
            p_copy = np.copy(self.parameters[i])
            rows, cols = np.where(self.parameters[i] > self.p_max)
            rows = np.delete(rows, np.where(cols==self.waveplate_index))
            cols = np.delete(cols, np.where(cols==self.waveplate_index))
            p_copy[rows,cols] = np.copy(self.p_max[cols])
            rows, cols = np.where(self.parameters[i] < self.p_min)
            rows = np.delete(rows, np.where(cols==self.waveplate_index))
            cols = np.delete(cols, np.where(cols==self.waveplate_index))
            p_copy[rows,cols] = np.copy(self.p_min[cols])
            self.parameters[i] = p_copy
        return

    # checked
    def update_parameters(self, index = []):
        if len(index) == 0:
            i = np.arange(self.caterpillars_no)
        elif len(index) == 1:
            i = np.copy(index[0])
        else:
            i = np.copy(index)
        steps_array = np.round(self.velocities[i]/self.delta_parameters)
        v_temp = steps_array*self.delta_parameters
        self.parameters[i] = np.round(self.parameters[i] + v_temp, 1)
        self.boundary_conditions(index)
        self.reduce_parameters(index)
        self.parameters[i] = np.round(self.parameters[i], 1)
        return

    def single_mutation(self, index):
        if len(index) == 1:
            i = index[0]
            p_i = np.random.randint(self.parameters_no)
            p_new = np.random.randint(self.parameters_range[p_i])
            self.parameters[i][p_i] = self.parameters_list_np[p_i][p_new]
        else:
            if len(index) == 0:
                i = np.arange(self.caterpillars_no)
            else:
                i = np.copy(index)
            # parameters_new = np.copy(self.parameters)
            rows_p = np.random.randint(self.parameters_no, size=len(i))
            cols_p = np.random.randint(self.parameters_range[rows_p])
            self.parameters[i,rows_p] = self.parameters_list_np[rows_p,cols_p]
        return

    def remove_duplicates(self, previous_parameters = np.array([]), PSO=True): #tutaj następuje produkcja nanów
        if len(previous_parameters) == 0:
            all_parameters_copy = np.copy(self.parameters)
        else:
            all_parameters_copy = np.append(previous_parameters, self.parameters, axis=0)
        unique_parameters, unique_parameters_index = np.unique(all_parameters_copy, return_index=True, axis=0)
        PSO_step_try = 0
        mutations = 0
        while len(all_parameters_copy) != len(unique_parameters):
            if PSO_step_try == 0:
                index_all = np.arange(len(all_parameters_copy))
            index_duplicates = np.setdiff1d(index_all, unique_parameters_index)
            index_duplicates_p = index_duplicates - len(previous_parameters)
            if PSO_step_try < 5 and PSO:
                r1 = np.random.random(len(index_duplicates_p))
                r1 = np.tile(r1[:, None], (1, self.parameters_no))
                r2 = np.random.random(len(index_duplicates_p))
                r2 = np.tile(r2[:, None], (1, self.parameters_no))
                self.velocities[index_duplicates_p] = self.w*self.velocities[index_duplicates_p] + self.c1*r1*(self.parameters_best[index_duplicates_p]-self.parameters[index_duplicates_p]) + self.c2*r2*(self.param_global_best-self.parameters[index_duplicates_p])
                if self.iteration_no == 1 or self.w == 0:
                    fitness_global_best_index = np.where(self.fitness_best == self.fitness_global_best)[0][0]
                    parameters_global_best = self.parameters_best[fitness_global_best_index]
                    where_random = np.where((self.parameters == parameters_global_best).all(axis=1))[0]
                    self.velocities[where_random] = np.random.uniform(-1., 1., (len(where_random),self.parameters_no))*(self.p_max-self.p_min) #tutaj było 0.1
                # if fitness_global_best_index in self.fitness[index_duplicates_p] and self.fitness[fitness_global_best_index] == self.fitness_global_best:
                #     self.velocities[fitness_global_best_index] = np.random.uniform(-1., 1., self.parameters_no)*(self.p_max-self.p_min)
                self.reduce_velocities(index_duplicates_p)
                self.update_parameters(index_duplicates_p)
                if len(previous_parameters) == 0:
                    all_parameters_copy = np.copy(self.parameters)
                else:
                    all_parameters_copy = np.append(previous_parameters, self.parameters, axis=0)
                unique_parameters, unique_parameters_index = np.unique(all_parameters_copy, return_index=True, axis=0)
                PSO_step_try += 1
            else:
                mutations += len(index_duplicates_p)
                self.single_mutation(index_duplicates_p)
                if len(previous_parameters) == 0:
                    all_parameters_copy = np.copy(self.parameters)
                else:
                    all_parameters_copy = np.append(previous_parameters, self.parameters, axis=0)
                unique_parameters, unique_parameters_index = np.unique(all_parameters_copy, return_index=True, axis=0)
        return mutations

    def update_global_best(self):
        index_max_current = np.argmax(self.fitness_best)
        if self.fitness_best[index_max_current] > self.fitness_global_best:
            self.fitness_global_best = self.fitness_best[index_max_current]
            self.param_global_best = np.copy(self.parameters[index_max_current])
        return

    def update_bests(self):
        where_change_parameters_best = np.argwhere(self.fitness > self.fitness_best)
        where_change_fitness_best = where_change_parameters_best.reshape(len(where_change_parameters_best),)
        np.put(self.fitness_best, where_change_fitness_best, np.take(self.fitness,where_change_fitness_best))
        np.put_along_axis(self.parameters_best, where_change_parameters_best, np.take(self.parameters,where_change_fitness_best, axis=0), axis=0)
        self.update_global_best()
        return

    def step(self, previous_parameters, duplicates=False):
        self.update_velocities()
        self.update_parameters()
        if duplicates:
            count_mutations = 0
        else:
            count_mutations = self.remove_duplicates(previous_parameters)
        self.fitness = self.fitness_function(self.parameters)
        self.update_bests()
        self.iteration_no += 1
        return count_mutations

# checked
def get_PSO_params_list(w_range, c1_range, c2_range):
    PSO_params_list = []
    for i in np.arange(w_range[0], w_range[1], w_range[2]):
        for j in np.arange(c1_range[0], c1_range[1], c1_range[2]):
            for k in np.arange(c2_range[0], c2_range[1], c2_range[2]):
                PSO_params_list.append([round(i,2),round(j,2),round(k,2)])
    return PSO_params_list

# checked
def get_new_generation(individuals_no, parameters_list):
    for i in range(0, len(parameters_list)):
        if i == 0:
            params = np.array([np.random.choice(parameters_list[i],individuals_no, replace=True)])
        else:
            params = np.append(params,[np.random.choice(parameters_list[i],individuals_no, replace=True)], axis=0)
    caterpillars_list = params.T
    return caterpillars_list

def append_list_to_string(string, lst, separator=','):
    lst_str = separator.join(map(str, lst))
    return string + separator + lst_str

def append_single_result_to_csv_PSO(PSO_params, path_csv, data_list, standard_deviation, versions, duplicates):
    w = PSO_params[0]
    c1 = PSO_params[1]
    c2 = PSO_params[2]
    if duplicates:
        new_line = 'PSO parameters;{};{};{:.1f};{:.1f};{:.1f};with duplicates'.format(standard_deviation, versions, w, c1, c2)
        name = "with_duplicates"
    else:
        new_line = 'PSO parameters;{};{};{:.1f};{:.1f};{:.1f};no duplicates'.format(standard_deviation, versions, w, c1, c2)
        name = "no_duplicates"
    for data in data_list:
        new_line = append_list_to_string(new_line,data,';')
    with open(path_csv + 'results_{:.2f}_{}.csv'.format(standard_deviation, name),'a') as f:
        f.write(new_line)
        f.write("\n")
    return

def append_result_to_csv_PSO(PSO_params, path_csv, data_list, standard_deviation, versions, duplicates):
    if duplicates:
        name = "with_duplicates"
    else:
        name = "no_duplicates"
    lines = []
    for i,p in enumerate(PSO_params):
        w = p[0]
        c1 = p[1]
        c2 = p[2]
        if duplicates:
            new_line = 'PSO parameters;{};{};{:.1f};{:.1f};{:.1f};with duplicates'.format(standard_deviation, versions, w, c1, c2)
        else:
            new_line = 'PSO parameters;{};{};{:.1f};{:.1f};{:.1f};no duplicates'.format(standard_deviation, versions, w, c1, c2)
        for data in data_list[i]:
            new_line = append_list_to_string(new_line,data,';')
        lines.append(new_line)
    with open(path_csv + 'results_{:.2f}_{}.csv'.format(standard_deviation, name),'a') as f:
        for new_line in lines:
            f.write(new_line)
            f.write("\n")
    return

def fitness_function_1D(p, parameter_range, p_min, center, standard_deviation_factor):
    standard_deviation = parameter_range*standard_deviation_factor
    result = np.exp(-1*(p-0.75*parameter_range-p_min)**2/(2*standard_deviation**2))/(standard_deviation*(2*np.pi)**0.5)
    """if p >= center:
        result = np.exp(-1*(p-0.75*parameter_range-p_min)**2/(2*standard_deviation**2))/(standard_deviation*(2*np.pi)**0.5)
    if p < center:
        result = 0.5*np.exp(-1*(p-0.25*parameter_range-p_min)**2/(2*standard_deviation**2))/(standard_deviation*(2*np.pi)**0.5)"""
    return result

def fitness_function_1D_max(parameter_list, parameter_range, p_min, center, standard_deviation_factor):
    result = 0
    result_new = 0
    for p in parameter_list:
        result_new = fitness_function_1D(p, parameter_range, p_min, center, standard_deviation_factor)
        if result_new > result:
            result = result_new
    return result

def fitness_function_max_8D(parameters_range_list, standard_deviation_factor):
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

def get_parameters_range():
    parameters_range_list = [[min(parameters_value), max(parameters_value)] for parameters_value in parameters_list]
    return parameters_range_list

def get_parameters_linspace(shape):
    parameters_range_list = get_parameters_range()
    parameters_linspace_list = [np.linspace(parameters_range_list[i][0],parameters_range_list[i][1], shape) for i in range (len(parameters_range_list))]
    return parameters_linspace_list

def fitness_function_plot(parameters, parameters_range_list, standard_deviation_factor):
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

def get_plot_args(parameters_range_list, index_x, index_y, shape, standard_deviation_factor):
    parameters_range_list_short = [parameters_range_list[index_x],parameters_range_list[index_y]]
    parameters_linspace = get_parameters_linspace(shape)
    x_space = parameters_linspace[index_x]
    y_space = parameters_linspace[index_y]
    z = np.array([fitness_function_plot([x,y], parameters_range_list_short, standard_deviation_factor) for y in y_space for x in x_space])
    Z = z.reshape(shape, shape)
    return [parameters_range_list_short, x_space, y_space, shape, Z]

def plot_fitness_function_8D(path, index_x, index_y, plot_args, standard_deviation_factor, maxZ):
    parameters_range_list_short = plot_args[0]
    x_space = plot_args[1]
    y_space = plot_args[2]
    Z = plot_args[4]

    plt.figure(figsize=(8, 8), dpi=100)
    plt.xlim(min(parameters_range_list_short[0]), max(parameters_range_list_short[0]))
    plt.ylim(min(parameters_range_list_short[1]), max(parameters_range_list_short[1]))
    plt.contourf(x_space,y_space,Z,100)
    plt.title('global maximum: {}'.format(maxZ))
    plt.savefig(path + 'fitness_function_sigma{:.2f}.png'.format(standard_deviation_factor), dpi = 300)
    plt.show()
    plt.close()

def generate_data_and_plot_fitness_function_8D(path, parameters_list, parameters_list_plot, index_x, index_y, shape, standard_deviation_factor):
    maxZ = fitness_function_max_8D(parameters_list, standard_deviation_factor)
    plot_args = get_plot_args(parameters_list_plot, index_x, index_y, shape, standard_deviation_factor)
    plot_fitness_function_8D(path, index_x, index_y, plot_args, standard_deviation_factor, maxZ)
    return maxZ

def single_simulation_PSO(individuals_per_iteration, parameters_list, parameters_names, parameters_min, parameters_max, PSO_params, interations_no, standard_deviation_factor, duplicates=False, version = 0):
    new_caterpillars_list = get_new_generation(individuals_per_iteration, parameters_list)
    fitness_function = sum_of_Gaussian_functions(parameters_min, parameters_max, standard_deviation_factor)
    simulation = simulation_PSO(new_caterpillars_list, parameters_names, parameters_list, 
                                parameters_min, parameters_max, PSO_params, fitness_function.calculate_function)

    max_fitness_list = np.array([simulation.fitness_global_best])
    average_fitness_list = np.array([np.average(simulation.fitness)])
    caterpillars_list_all = np.copy(simulation.parameters)
    generations_no_list = np.array([simulation.iteration_no])
    mutation_no_list = np.array([0])
    while simulation.iteration_no < interations_no:
        mutation_no = simulation.step(caterpillars_list_all, duplicates)
        mutation_no_list = np.append(mutation_no_list, mutation_no)
        max_fitness_list = np.append(max_fitness_list, simulation.fitness_global_best)
        average_fitness_list = np.append(average_fitness_list, np.average(simulation.fitness))
        caterpillars_list_all = np.append(caterpillars_list_all, simulation.parameters, axis=0)
        generations_no_list = np.append(generations_no_list,simulation.iteration_no)
    return generations_no_list, max_fitness_list, average_fitness_list, mutation_no_list

def do_simulation_PSO(path_csv, path_average, individuals_per_iteration, parameters_list, parameters_names, parameters_min, parameters_max, w_range, c1_range, c2_range, iterations_no, standard_deviation_factor, versions, parameters_list_plot, index_x, index_y, shape, duplicates=False):
    # generate_data_and_plot_fitness_function_8D(path_average, parameters_list, parameters_list_plot, index_x, index_y, shape, standard_deviation_factor)
    PSO_params_list = get_PSO_params_list(w_range, c1_range, c2_range)
    data_list = []
    # generations_no_list = []
    # mutation_no_list = np.array([])
    print('\n')
    for PSO_params in PSO_params_list:
        max_fitness_list = []
        average_fitness_list = []
        print('w: {:.1f}  c1: {:.1f}  c2: {:.1f}'.format(PSO_params[0], PSO_params[1], PSO_params[2]))

        # items = [(AG_params, path, parameters_list, index_x, index_y, generations_no, shape, standard_deviation_factor, i+1) for i in range(versions)]
        results_list = Parallel(n_jobs=11)(delayed(single_simulation_PSO)(individuals_per_iteration, parameters_list, parameters_names, parameters_min, parameters_max, PSO_params, iterations_no, standard_deviation_factor, duplicates, i+1) for i in range(versions))
        max_fitness_list = np.array([i[1] for i in results_list])
        average_fitness_list = np.array([i[2] for i in results_list])
        max_fitness_list_average = np.average(max_fitness_list, axis = 0)
        max_fitness_list_standard_deviations = np.std(max_fitness_list, axis = 0)
        average_fitness_list_average = np.average(average_fitness_list, axis = 0)
        average_fitness_list_standard_deviations = np.std(average_fitness_list, axis = 0)
        # generations_no_list.append(results_list[-1][0].copy())
        # mutation_no_list = np.append(mutation_no_list, np.array([i[3] for i in results_list]))
        mutation_no_list = np.sum(np.array(np.array([i[3] for i in results_list])), axis=0)/versions

        data_list.append([max_fitness_list_average, max_fitness_list_standard_deviations, average_fitness_list_average, average_fitness_list_standard_deviations, mutation_no_list])
        # element = [max_fitness_list_average, max_fitness_list_standard_deviations, average_fitness_list_average, average_fitness_list_standard_deviations, mutation_no_list]
        # append_result_to_csv_PSO(PSO_params, path_csv, element, standard_deviation_factor, versions)
        # del results_list
        # (PSO_params, path_csv, data_list, standard_deviation, versions)
    # for i in range(len(PSO_params_list)):
    #     append_single_result_to_csv_PSO(PSO_params_list[i], path_csv, data_list[i], standard_deviation_factor, versions, duplicates)
    append_result_to_csv_PSO(PSO_params_list, path_csv, data_list, standard_deviation_factor, versions, duplicates)
        # IT WILL PLOT ONLY ONE CHART (FIRST PROBABLY) WHEN UNCOMMENTED
        # max_fitness_list_average, max_fitness_list_standard_deviations, average_fitness_list_average, average_fitness_list_standard_deviations = data_list[i]
        # plot_generation_average_results_PSO(AG_params, path_average, generations_no_list[i],
        #                                 max_fitness_list_average, max_fitness_list_standard_deviations,
        #                                 average_fitness_list_average, average_fitness_list_standard_deviations,
        #                                 standard_deviation_factor, versions, maxZ)

    print('standard deviation {:.2f} simulation done'.format(standard_deviation_factor))
    return data_list

path_csv = "../Simulations/Particle_Swarm_Optimisation/"

individuals_per_iteration = 8

frequency_list = [float(i)/10. for i in range(1,51)]
length_list = [6,12,18]
dye_list = [0.2,1]
thickness_list = [50,90]
period_list = [1,2,3]
laserPower_list = [float(i)/2. for i in range(1,9)]
waveplate_list = [7.5*int(i)+30 for i in range(0,12)]
# right side of the film: 0 down, 1 up
tail_list = [0,1]
frequency_list_plot = [float(i) for i in range(0,120)]
laserPower_list_plot = [float(i) for i in range(0,120)]

parameters_names = ["frequency", "length", "dye", "thickness", "period", "laserPower", "tail", "waveplate"]
parameters_list = [frequency_list, length_list, dye_list, thickness_list, 
                   period_list, laserPower_list, tail_list, waveplate_list]
parameters_min = pd.DataFrame(parameters_list).T.min().to_numpy()
parameters_max = pd.DataFrame(parameters_list).T.max().to_numpy()

parameters_list_plot = [frequency_list_plot, length_list, dye_list, thickness_list, 
                        period_list, laserPower_list_plot, tail_list, waveplate_list]

index_x = -1
index_y = -1
index_x_plot = 0
index_y_plot = 5
#point no on each axis
shape = 120

c0_delta = 0.2
c1_delta = 0.2
c2_delta = 0.2
c0_start = 0. # 0.4
c1_start = 0. # 2.5
c2_start = 0. # 0.5
c0_max = 3.
c1_max = 3.
c2_max = 3.
w_range = [c0_start, c0_max+c0_delta, c0_delta]
c1_range = [c1_start, c1_max+c1_delta, c1_delta]
c2_range = [c2_start, c2_max+c2_delta, c2_delta]

#when stop
iterations_no = 5
#how many times rerun simulation
versions = 1000

#duplicates acceptable?
duplicates = False

standev_list = [0.05,0.1,0.25,0.5]
duplicates = False

for standev in standev_list:
    duplicates = False
    results = do_simulation_PSO(path_csv, path_csv, individuals_per_iteration, parameters_list, parameters_names, parameters_min, parameters_max, w_range, c1_range, c2_range, iterations_no, standev, versions, parameters_list_plot, index_x, index_y, shape, duplicates)
    duplicates = True
    results = do_simulation_PSO(path_csv, path_csv, individuals_per_iteration, parameters_list, parameters_names, parameters_min, parameters_max, w_range, c1_range, c2_range, iterations_no, standev, versions, parameters_list_plot, index_x, index_y, shape, duplicates)

with open(path_csv + 'check.csv','a') as f:
    f.write('DONE')
    f.write("\n")
