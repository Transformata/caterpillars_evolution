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

This project explores data-driven optimization of underwater soft robots fabricated from liquid crystal elastomers. By applying GA and PSO directly to real-world performance metrics, the robots evolved to achieve faster swimming speeds and novel locomotion modes.

---

## 🎥 Experimental Videos

Videos are hosted on Zenodo due to file size limitations:

📦 [Zenodo Dataset (15158295)](https://zenodo.org/records/15158295)

**Filename Format:**
```
YYYYMMDD_frequency_length_dyeConcentration_thickness_curlLength_power_tailDirection_angleID_directionID.mp4
```

- `tailDirection`: 0 = downward bend, 1 = upward bend  
- `angleID`: Raw waveplate setting  
- `directionID`: L1–L5 or R1–R5 = scan direction and trial number

---

## 📐 Polarization Angle Calculation

To compute the angle between the laser scan and the polarization direction:

```
Polarization–Scan Angle = 2 × (measured angle − 30°)
```

📝 For example, a waveplate setting of `82.5°` corresponds to:  
`(82.5 - 30) × 2 = 105°`

> ⚠️ Note: Filenames use the raw waveplate angle, not the computed polarization angle.

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
- `.json` files with parameter settings for the tracking script.

### `/Results/`
- `fitted_speed.txt`: Fitted speed values.
- `Optimisation_Results.csv`: Results from GA and PSO experiments.
- `optimization_*.txt`: Logs of GA runs used to generate subsequent generations via `GA_measurements_and_simulation.py`.
- `.xlsx`: Structured results for further analysis.

---

## 🧪 Simulations

Simulations include parameter sweeps and synthetic fitness function evaluations.

- `/Genetic_Algorithm/`: GA performance results  
- `/Particle_Swarm_Optimisation/`: PSO performance results  
- `/fitness_function/`: 2D fitness function visualizations

---

## 💻 Code Overview

### Analysis Scripts

- `tracking.py`: Extracts position-time data from `.mp4` videos using `.json` configuration files.
- `get_speed.py`: Performs linear fitting on extracted data and calculates speed.

### Optimization Algorithms

- `GA_measurements_and_simulation.py`: Runs GA for both experiments and simulations. Set `experiment=True` or `False` accordingly.
- `PSO_measurements.ipynb`: PSO implementation designed for use in Google Colab, requires manual setup of Google Sheet IDs.
- `PSO_simulations.py`: PSO applied to synthetic functions.

---

## 🛠️ Usage Instructions

1. **Extract Position from Videos**
   ```bash
   python tracking.py
   ```
   - Inputs: `.mp4` from `/Movies_Optimisation/`, `.json` from `/Tracking_Parameters/`
   - Outputs: `.txt` → `/Data_Position_vs_Time/`, `.png` → `/Plots_Position_vs_Time/`

2. **Calculate Speed**
   ```bash
   python get_speed.py
   ```
   - Input: `.txt` files in `/Data_Position_vs_Time/`
   - Output: Speed values appended to `/Results/fitted_speed.txt`

3. **Run GA or PSO on Experimental Data**
   - GA: In `GA_measurements_and_simulation.py`, set `experiment = True` and run.
   - PSO: Use `PSO_measurements.ipynb`. Requires pre-filled Google Sheet IDs; intended for use in Google Colab.

4. **Run GA or PSO Simulation**
   - GA: In `GA_measurements_and_simulation.py`, set `experiment = False` and run.
     - Output: `.csv` → `/Simulations/Genetic_Algorithm/`, `.png` → `/Simulations/fitness_function/`
   - PSO: Run `PSO_simulations.py`
     - Output: `.csv` → `/Simulations/Particle_Swarm_Optimisation/`

---

## 📎 Citation

If you use this repository or dataset, please cite:

📄 [Zenodo DOI: 10.5281/zenodo.15158295](https://zenodo.org/records/15158295)

---

## 📜 License

This repository is licensed under the **GNU General Public License v3.0**.  
See the [LICENSE](LICENSE) file for more details.
