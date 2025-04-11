# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 18:45:40 2023

@author: mikol
"""

import os
import shutil

def save_tracking_parameters_in_readme_file(folder_name, path_tracking_script, path_results):
    lines = []
    lines.append(folder_name + "\n")
    lines.append("tracking parameters (ver 13, no data clearing after tracking):\n")

    with open(path_tracking_script) as f:
        start = False
        for line in f:
            if "DON'T CHANGE ANYTHING BELOW" in line:
                break
            if start:
                lines.append(line)
            if "tracking parameters" in line:
                start = True

    with open(path_results + 'README.txt', 'w') as f:
        for line in lines:
            f.write(line)

def archive_results(path_results, path_movies, path_results_archive, path_movies_archive, path_tracking_script):
    directory_movies = os.fsencode(path_movies)
    list_of_files = sorted( filter( lambda x: os.path.isfile(os.path.join(directory_movies, x)),
                        os.listdir(directory_movies) ) )

    movies_name = ""
    for file in list_of_files:
        name = str(os.fsdecode(file))
        if name[-3:] != "mp4":
            continue
        elif movies_name == "":
            movies_name = name.rsplit("_",1)[0]
        if movies_name in name:
            os.replace(path_movies+name, path_movies_archive+name)

    path_archive_result = path_results + movies_name + '\\'
    save_tracking_parameters_in_readme_file(movies_name, path_tracking_script, path_archive_result)
    #os.rename(path_archive_result, path_results_archive + movies_name+'\\')
    shutil.move(path_archive_result, path_results_archive + movies_name + '\\')

path_tracking_script = r"G:\Mój dysk\PNaF\Diamentowy_Grant_2017-2021\Swimming_caterpillars_evolution\python\all_you_need_to_measure\tracking_bacground_substraction_preview_13_only1_contour.py"
path_results = r"G:\Mój dysk\PNaF\Diamentowy_Grant_2017-2021\Swimming_caterpillars_evolution\wyniki\aktualne\tracking_results\\"
path_results_archive = r"G:\Mój dysk\PNaF\Diamentowy_Grant_2017-2021\Swimming_caterpillars_evolution\wyniki\aktualne\zrobione_z_rejestrem\\"
path_movies = r"G:\Mój dysk\PNaF\Diamentowy_Grant_2017-2021\Swimming_caterpillars_evolution\wyniki\aktualne\tracking_movies\\"
path_movies_archive = r"G:\Mój dysk\PNaF\Diamentowy_Grant_2017-2021\Swimming_caterpillars_evolution\wyniki\aktualne\zrobione_z_rejestrem\filmy\\"
archive_results(path_results, path_movies, path_results_archive, path_movies_archive, path_tracking_script)

# path_movies_test = r"C:\Users\mikol\Desktop\test\movies\\"
# path_movies_archive_test = r"C:\Users\mikol\Desktop\test\archive\movies_archive\\"
# path_results_test = r"C:\Users\mikol\Desktop\test\\"
# path_results_archive_test = r"C:\Users\mikol\Desktop\test\archive\\"
# archive_results(path_results_test, path_movies_test, path_results_archive_test, path_movies_archive_test, path_tracking_script)
