# -*- coding: utf-8 -*-

import sys
import cv2
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('Agg')
import json
import tkinter as tk
from tkinter import filedialog

# set true for tracking preview
preview = False

# Create a GUI to select a JSON file
def select_json_file(repo_root):
    tracking_params_path = os.path.join(repo_root, 'Experimental','Tracking_Parameters')
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    print("Please select the JSON file with tracking parameters.")
    file_path = filedialog.askopenfilename(
        initialdir=tracking_params_path,
        title="Select Tracking Parameters JSON File",
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
    )
    return file_path

# Load the selected JSON file
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        params = json.load(file)

    # Extract the file name without extension
    json_name = os.path.splitext(os.path.basename(file_path))[0]
    # Remove "_tracking_parameters" if it exists
    if "_tracking_parameters" in json_name:
        json_name = json_name.replace("_tracking_parameters", "")
    return params, json_name

def get_x(c):
    (x, y, w, h) = cv2.boundingRect(c)
    return x

def check_opencv_version():
    version = cv2.__version__.split('.')[0]
    if version == '2' :
        fgbg = cv2.BackgroundSubtractorMOG2()
    if version == '3' or version == '4': 
        fgbg = cv2.createBackgroundSubtractorMOG2()
    return version

def save_position_vs_time_txt_and_plot(data, movie, repo_root, save_plot=False):
    file_name = movie.replace(".mp4", "")
    plot_path = os.path.join(repo_root, 'Experimental','Plots_Position_vs_Time')
    data_path = os.path.join(repo_root, 'Experimental','Data_Position_vs_Time')
    if(len(data) > 200):

        x_data = list()
        y_data = list()
        #numpy arrays are very slow here
        for element in data:
            x_data.append(element[0])
            y_data.append(element[1])

        if save_plot:
            plt.plot(x_data, y_data, '+', color = 'black', markersize = 0.1)
            plt.axis([0, max(x_data), 0, 4.683])
            plt.xlabel('time [s]')
            plt.ylabel('position [cm]')
            plot_save_path = os.path.join(plot_path, file_name)
            plt.savefig(plot_save_path, dpi=500)
            #plt.show()
            plt.close()
        
        data_save_path = os.path.join(data_path, file_name + '.txt')
        with open(data_save_path, 'w') as f:
            for item in data:
                row = str(item[0]) + " " + str(item[1])
                f.write("%s\n" % row)
    else: 
        print(f"not enough data for dataset {file_name}")
        with open('not_enough_data.txt', 'a+') as f:
            f.write(file_name + "\n")
    return

def tracking_params_set(input_dict, file_name, repo_root, preview, save_plot):
    params_dict = input_dict
    pixel_scale = params_dict["picture_width_px"] / params_dict["picture_width_cm"]
    blur_area = tuple(params_dict["blur_area"])
    y_stop = params_dict["y_start"] + params_dict["delta_y"]

    cv2.ocl.setUseOpenCL(False)
    version = check_opencv_version()

    movies_path = os.path.join(repo_root, 'Experimental','Movies_Optimisation')

    list_of_movies = []
    for i in range(5):
        list_of_movies.append(file_name+f"_L{i+1}.mp4")
        list_of_movies.append(file_name+f"_R{i+1}.mp4")
    list_of_movies.sort()

    for movie in list_of_movies:

        if movie[-3:] != "mp4": 
            continue

        # if not "240310_0100mHz_06mm_0%2_50um_1mm_0500mW_0_030deg0" in movie:
        #     continue

        robot_length = float(movie.split("_")[2][:-2])/10.
        w_min = int(params_dict["min_rect_width"] * pixel_scale * robot_length)
        if preview:
            print("minimal width of the contour: {}".format(w_min))

        side = False
        if params_dict["tracking_side"] == 0:
            if movie[-6] == "L":
                side = True
            else:
                side = False
        elif params_dict["tracking_side"] == 1:
            side = True
        elif params_dict["tracking_side"] == 2:
            side = False

        #read video file
        curr_movie_path = os.path.join(movies_path, movie)
        cap = cv2.VideoCapture(curr_movie_path)

        #if ret is true than no error with cap.isOpened
        ret, frame = cap.read()
        if not ret:
            print('Cannot read video file: ' + movie)
            continue

        frame_nr = 0
        x = 0
        x_old = -10

        data = []
        if preview:
            print('reading: ' + movie)
        elif "L1" in movie:
            print('tracking: ' + movie[:-7])
        
        reason_previous = "no reason"
        while (cap.isOpened):

            frame_nr = frame_nr + 1
            #if ret is true than no error with cap.isOpened
            ret, frame = cap.read()
            if frame_nr < params_dict["frame_start"]: continue

            if ret==True and ret is not None:
                # convert to gray image
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # cropping image
                frame_cropped = frame[params_dict["y_start"]:y_stop, params_dict["x_start"]:params_dict["x_stop"]]

                # Gaussian filtering
                blurred = cv2.GaussianBlur(frame_cropped, (blur_area[0], blur_area[1]), 0)

                # applying morphological transformations and cropping image
                if params_dict["apply_morph"]:
                    morph_kernel_size = tuple(params_dict["morph_kernel_size"])
                    kernel = np.ones(morph_kernel_size, np.uint8)
                    blurred = cv2.morphologyEx(blurred, params_dict["morph_type"], kernel)

                thresh = []
                # Otsu's thresholding
                if params_dict["threshold_mode"] == 0:
                    (T, th) = cv2.threshold(blurred, 0, 255,
                        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                    thresh.append(th)
                    
                # adaptive thresholding
                elif params_dict["threshold_mode"] == 1:
                    th = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                        cv2.THRESH_BINARY_INV, params_dict["adaptive_thresh_area"], params_dict["adaptive_thresh_constant"])
                    thresh.append(th)
                    
                # show all thresholding
                elif params_dict["threshold_mode"] == -1:
                    (T, th1) = cv2.threshold(blurred, 0, 255,
                        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                    thresh.append(th1)
                    th2 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                        cv2.THRESH_BINARY_INV, params_dict["adaptive_thresh_area"], params_dict["adaptive_thresh_constant"])
                    thresh.append(th2)

                else:
                    print("invalid thresholding mode")
                    continue

                if preview:
                    if params_dict["threshold_mode"] == -1: 
                        cv2.imshow("Otsu Thresholding", thresh[0])
                        cv2.imshow("adaptive Thresholding", thresh[1])
                    if params_dict["threshold_mode"] == 0: 
                        cv2.imshow("Otsu's Thresholding", thresh[0])
                    if params_dict["threshold_mode"] == 1: 
                        cv2.imshow("adaptive Thresholding", thresh[0])

                # finding contours
                if version == '2' or version == '4': 
                    (contours, hierarchy) = cv2.findContours(thresh[0].copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                if version == '3' : 
                    (im2, contours, hierarchy) = cv2.findContours(thresh[0].copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                # filtering contours with areas bigger than "min_area" value
                cnts = [c for c in contours if cv2.minEnclosingCircle(c)[1] > params_dict["min_area"]]

                # choosing contour
                if len(cnts) != 0:
                    if side: x = 1580
                    else: x = -100
                    y = 0
                    w = 0
                    h = 0
                    box_found = False
                    reason = "no contour"
                    for c in cnts:
                        (xc, yc, wc, hc) = cv2.boundingRect(c)
                        if cv2.contourArea(c) > params_dict["min_area"] and hc > params_dict["min_rect_height"] and wc > w_min:
                            if side:
                                if xc < x:
                                    x = xc
                                    y = yc
                                    w = wc
                                    h = hc
                            else:
                                if xc+w > x:
                                    y = yc
                                    w = wc
                                    h = hc
                                    x = xc+w

                            if x_old == -10:
                                x_old = x
                                box_found = True
                                box_new = [frame_nr/params_dict["frame_rate"], float(x + params_dict["x_start"])/pixel_scale]

                            elif abs(x-x_old) > params_dict["delta_x"]:
                                # x = x_old
                                box_found = False
                                reason = "position difference greater than delta"
                                
                            else:
                                box_found = True
                                box_new = [frame_nr/params_dict["frame_rate"], float(x + params_dict["x_start"])/pixel_scale]
                                x_old = x

                    if box_found:
                        data.append(box_new)                                
                        #draw bounding box
                        if side:
                            cv2.rectangle(frame, (x + params_dict["x_start"], y + params_dict["y_start"]), (x + w + params_dict["x_start"], y + h + params_dict["y_start"]), (255, 69, 0), 2)
                        else:
                            cv2.rectangle(frame, (x + params_dict["x_start"] - w, y + params_dict["y_start"]), (x + params_dict["x_start"], y + h + params_dict["y_start"]), (255, 69, 0), 2)
                    else:
                        if reason_previous == "no reason" or reason_previous != reason:
                            if preview:
                                print(reason)
                            reason_previous = reason

                cv2.rectangle(frame, (params_dict["x_start"], params_dict["y_start"]), (params_dict["x_stop"], y_stop), (0, 255, 0), 1)

                if preview:
                    cv2.imshow(movie, frame)
                    k = cv2.waitKey(1) & 0xff
                    if k == 27: 
                        cv2.waitKey(1)
                        cv2.destroyAllWindows()
                        sys.exit()

            else: break

        if preview:
            cap.release()
            cv2.destroyAllWindows()
        
        save_position_vs_time_txt_and_plot(data, movie, repo_root, save_plot)

    if preview:
        try:
            cap.release()
            cv2.destroyAllWindows()
        except:
            return

    return

def track_all(preview, save_plot):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    tracking_params_path = os.path.join(repo_root, 'Experimental','Tracking_Parameters')

    # Get all file names in the folder
    files_names = os.listdir(tracking_params_path)
    
    # Filter files
    tracking_parameters_files_list = [file_name for file_name in files_names if file_name[-4:] == "json" and file_name[0] == "2"]
    tracking_parameters_files_list.sort()

    # movies_to_track = list()
    # with open("fit_again.txt", 'r') as file:
    #     for line in file:
    #         movies_to_track.append(line)
    # movies_to_track = [movie[:-4] for movie in movies_to_track]
    # movies_to_track = list(dict.fromkeys(movies_to_track))
    # movies_to_track.sort()
    # tracking_parameters_files_list = [file_name for file_name in tracking_parameters_files_list if file_name.replace("_tracking_parameters.json", "") in movies_to_track]
    # # print(tracking_parameters_files_list)
    # tracking_parameters_files_list.sort()

    for file in tracking_parameters_files_list:
        json_file_path = os.path.join(tracking_params_path, file)
        params_dict, file_name = load_json_file(json_file_path)
        # print(f"Loaded: {file}")
        tracking_params_set(params_dict, file_name, repo_root, preview, save_plot)
    return

if __name__ == "__main__":      
    # Track robot's position
    save_plot = True
    track_all(preview, save_plot)