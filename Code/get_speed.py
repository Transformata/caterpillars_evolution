# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

from tqdm import tqdm

def get_params_sets_list(folder_path, cut_length=7):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        raise ValueError(f"The folder '{folder_path}' does not exist.")
    
    # Get all file names in the folder
    files_names = os.listdir(folder_path)
    # Cut and remove duplicates
    short_names = {file_name[:-cut_length] for file_name in files_names if len(file_name) > cut_length and file_name[-3:] == "txt"}
    short_names = list(short_names)
    short_names.sort()

    # Return the unique cut names
    return short_names

def get_index(nr_list, minmax):
    if(minmax == 0):
        mark = min(nr_list)
    if(minmax == 1):
        mark = max(nr_list)
    mark_index = nr_list.index(mark)
    return mark_index

def closest_value(input_list, input_value):
    arr = np.asarray(input_list)
    i = (np.abs(arr - input_value)).argmin()
    result = arr[i]
    return result

def linear_fit_to_position_vs_time(data_path, results_path, plot_path, save_plot = False):
    params_sets_list = get_params_sets_list(data_path, 7)
    params_sets_list.sort()
    rows_with_results = list()
    # line fit interval
    time_min = 5
    time_max = 35
    # if shorter than 40 s, from 2 s to t_max - 2 s
    time_margin = 2
    # 0 - fit to tracked data, 1 - fit to smooth
    data_type = 0

    msg_fit_rows = list()
    msg_no_file_rows = list()
    msg_no_points_rows = list()
    
    file_speed_path = os.path.join(results_path, 'fitted_speed.txt')
    if save_plot:
        plot_data = list()

    for params_set in tqdm(params_sets_list):
        data_files_list = []
        for i in range(5):
            data_files_list.append(params_set+f"_L{i+1}.txt")
            data_files_list.append(params_set+f"_R{i+1}.txt")
        data_files_list.sort()

        for data_file in data_files_list:
    
            if(data_file[0] != "2"): 
                continue
            if data_file[-3:] != "txt": 
                continue
            if data_type == 1 and data_file.split("_")[-1][:8] != "smoothed": 
                continue
            
            x_data = list()
            y_data = list()
            data = list()
            
            data_file_path = os.path.join(data_path, data_file)
            try:
                with open(data_file_path) as f:
                    for line in f:
                        element = line.rstrip('\n').split()
                        x = float(element[0])
                        y = float(element[1])
                        x_data.append(x)
                        y_data.append(y)
                        data.append([x, y])
            
                if(len(x_data) > 200):
                
                    if max(x_data) < 39:
                        time_min_temp = closest_value(x_data, time_margin)
                        time_max_temp = closest_value(x_data, max(x_data)-time_margin)
                    else:
                        time_min_temp = closest_value(x_data, time_min)
                        time_max_temp = closest_value(x_data, time_max)
            
                    time_min_index = x_data.index(time_min_temp)
                    time_max_index = x_data.index(time_max_temp)
                
                    x = np.array(x_data[time_min_index:time_max_index])
                    y = np.array(y_data[time_min_index:time_max_index])
                    parameters = np.polyfit(x, y, 1, full=True)
                    ab = parameters[0]
                    msg_fit_rows.append(f"{data_file}: {round(ab[0]*60,2)}")
                    stats = parameters[1:]
                    row = data_file.replace(".txt", "") + " a (speed [cm/min]) {} b {} chi2, rank, singular values, rcond {}\n".format( str(round(ab[0]*60,2)), ab[1], stats )
                    rows_with_results.append(row)
                    if save_plot:
                        plot_fit_path = os.path.join(plot_path, data_file[:-4] + "_fit.png")
                        plot_data.append([x_data, y_data, x, ab, plot_fit_path])
                    
                else:
                    msg_no_points_rows.append(f"{data_file}: not enough points")
            except:
                msg_no_file_rows.append(f"no file: {data_file}")
        
        if save_plot and len(rows_with_results) >= 10:
            for x_data, y_data, x, ab, plot_fit_path in plot_data:
                plt.plot(x_data, y_data, '+', color = 'black', markersize = 0.1)
                plt.axis([0, max(x_data), 0, 4.683])
                plt.xlabel('time [s]')
                plt.ylabel('position [cm]')
                plt.plot(x, ab[0]*x+ab[1], color = 'b')
                plt.savefig(plot_fit_path, dpi=1000)
                plt.close()
            plot_data = list()
    
    if save_plot:
        if len(plot_data) != 0:
            for x_data, y_data, x, ab, plot_fit_path in plot_data:
                plt.plot(x_data, y_data, '+', color = 'black', markersize = 0.1)
                plt.axis([0, max(x_data), 0, 4.683])
                plt.xlabel('time [s]')
                plt.ylabel('position [cm]')
                plt.plot(x, ab[0]*x+ab[1], color = 'b')
                plt.savefig(plot_fit_path, dpi=1000)
                plt.close()
    
    with open(file_speed_path, 'a+') as f:
        for row in rows_with_results:
            f.write(row)
    for row in msg_fit_rows:
        print(row)
    for row in msg_no_points_rows:
        print(row)
    for row in msg_no_file_rows:
        print(row)

    return

if __name__ == "__main__":
    save_plot = False
    repo_root = '..'
    data_path = os.path.join(repo_root, 'Experimental','Data_Position_vs_Time') 
    results_path = os.path.join(repo_root, 'Experimental', 'Results')
    plot_path = os.path.join(repo_root, 'Experimental','Plots_Position_vs_Time')
    linear_fit_to_position_vs_time(data_path, results_path, plot_path, save_plot)