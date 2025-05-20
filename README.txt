# 🐛 Caterpillars Evolution: Light-Powered Soft Swimming Robots

This repository contains experimental data, simulation results, and analysis code related to the development and optimization of soft swimming robots powered by light. The project combines physical experiments with evolutionary algorithms—Genetic Algorithm (GA) and Particle Swarm Optimization (PSO)—to improve the robots’ locomotion efficiency.

---

## 📁 Repository Structure

```
/caterpillars_evolution/
├── /Experimental/
│   ├── /Movies_Optimisation/         # Raw .mp4 videos (hosted on Zenodo)
│   ├── /Movies_Self-Oscillation/     # One-shot locomotion experiments
│   ├── /Data_Position_vs_Time/       # Position vs. time data (.txt)
│   ├── /Plots_Position_vs_Time/      # Raw and fitted plots (.png)
│   ├── /Tracking_Parameters/         # Tracking settings (.json)
│   └── /Results/                     # Aggregated results
│       ├── fitted_speed.txt
│       ├── Optimisation_Results.csv
│       ├── optimization_1.txt
│       ├── optimization_2.txt
│       ├── result_PSO.xlsx
│       ├── results_GA.xlsx
│       └── results_archive.xlsx
│
├── /Simulations/
│   ├── /Genetic_Algorithm/           # GA simulation results
│   ├── /Particle_Swarm_Optimisation/ # PSO simulation results
│   └── /fitness_function/            # 2D visualizations of fitness functions used for simulations
│
├── /Code/
│   ├── tracking.py                   # Position tracking from videos
│   ├── get_speed.py                  # Speed calculation from tracking data
│   ├── GA_measurements_and_simulation.py # GA implementation and simulations
│   ├── PSO_measurements.ipynb        # PSO implementation notebook
│   └── PSO_simulations.py            # PSO simulations on synthetic data
│
├── LICENSE                           # GPL-3.0 license
├── .gitignore                        # Ignored files
├── README.md                         # This file
└── CITATION.cff                      # Citation metadata (optional)
```

---

## 🎯 Project Overview

We explore data-driven optimization of underwater soft robots fabricated from liquid crystal elastomers. By applying GA and PSO directly to real-world performance metrics, the robots evolved to achieve faster swimming speeds and novel locomotion modes.

---

## 🎥 Experimental Videos

Videos are hosted on Zenodo due to size:

📦 [Zenodo Dataset (15158295)](https://zenodo.org/records/15158295)

**Filename Format:**

```
YYYYMMDD_frequency_length_dyeConcentration_thickness_curlLength_power_tailDirection_angleID_directionID.mp4
```

- `tailDirection`: 0 = down, 1 = up
- `angleID`: Raw waveplate setting
- `directionID`: L1–L5 or R1–R5 = scan direction + trial number

---

## 📐 Polarization Angle Calculation

To compute the angle between laser scan and polarization:

```
Polarization–Scan Angle = 2 × (measured angle − 30°)
```

📝 A waveplate setting of `82.5°` becomes:  
`(82.5 - 30) × 2 = 105°`

> ⚠️ The raw waveplate values are used in filenames, not the calculated angle.

---

## 📊 Data Summary

### `/Data_Position_vs_Time/`
- `.txt` files with time-position pairs extracted from videos.

### `/Plots_Position_vs_Time/`
Graphical plots of position vs. time data.

- **Raw Plot:**  
  `YYYYMMDD_..._directionID.png`
- **Fitted Plot (Linear Fit):**  
  `YYYYMMDD_..._directionID_fit.png`

### `/Tracking_Parameters/`
- `.json` files with parameter settings for the script extracting time-position data from movies.

### `/Results/`
- `fitted_speed.txt`: List of fitted speed values.
- `Optimisation_Results.csv`: Full GA/PSO experiments results.
- `optimization_*.txt`: Logs of GA experimental runs necessery to generate subsequential generation by script GA_measurements_and_simulations.py.
- `.xlsx` files: Structured result archives.

---

## 🧪 Simulations

Located in `/Simulations/`, these include parameter sweeps and synthetic fitness tests:

- `/Genetic_Algorithm/`
- `/Particle_Swarm_Optimisation/`
- `/fitness_function/`

---

## 💻 Code Overview

### Analysis Scripts

- `tracking.py`: Extracts position-time data from measured .mp4 files using `.json` tracking files.
- `get_speed.py`: Performs linear fitting and speed calculation to data extracted with tracking.py script.

### Optimization Algorithms

- `GA_measurements_and_simulation.py`: Runs GA for both measurements and simulations.
- `PSO_measurements.ipynb`: Implementation for PSO, originally used in Google Colab environment.
- `PSO_simulations.py`: PSO applied to synthetic fitness landscapes.

---

## 🛠️ Usage Instructions

1. **Extract Position from Videos**
   ```bash
   python tracking.py
   ```
   - Input: `.mp4` from `/Movies_Optimisation/` + `.json` from `/Tracking_Parameters/`
   - Output: `.txt` → `/Data_Position_vs_Time/`, plots → `/Plots_Position_vs_Time/`

2. **Calculate Speed**
   ```bash
   python get_speed.py
   ```
   - Reads `.txt` data in `/Data_Position_vs_Time/` and appends to `fitted_speed.txt`

3. **Run GA or PSO optimisation in experiment**
   - GA: `GA_measurements_and_simulation.py` change value of variable `experiment` to `True` and run
   - PSO: `PSO_measurements.ipynb` contains variables with googlesheet IDs necessary for script to run. It was used in Google Collaboratory environment

4. **Run GA or PSO simulation**
   - GA: `GA_measurements_and_simulation.py` change value of variable `experiment` to `False` and run
	- output: `.csv` → `/Simulations/Genetic_Algorithm/` and `.png` → `/Simulations/fitness_functions/`
   - PSO: run `PSO_simulations.py`
	- output: `.csv` → `/Simulations/Particle_Swarm_Optimisation/`


---

## 📎 Citation

If you use this repository or dataset, please cite:

📄 [Zenodo DOI: 10.5281/zenodo.15158295](https://zenodo.org/records/15158295)

---

## 📜 License

This repository is licensed under the **GNU General Public License v3.0**.  
See the [LICENSE](LICENSE) file.

---
