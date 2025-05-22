# 🐛 Caterpillars Evolution: Light-Powered Soft Swimming Robots

This repository contains experimental data, simulation results, and analysis code related to the development and optimization of soft swimming robots powered by light. The project combines physical experiments with evolutionary algorithms, Genetic Algorithm (GA) and Particle Swarm Optimization (PSO), to improve the robots locomotion efficiency.

---

## 📁 Repository Structure

```
caterpillars_evolution/
├── Experimental/                         # Experimental data and video recordings
│   ├── Movies_Optimization/              # Raw .mp4 videos (hosted on Zenodo)
│   ├── Movies_Self-Oscillation/          # One-shot locomotion experiments
│   ├── Data_Position_vs_Time/            # Position vs. time data extracted from videos (.txt)
│   ├── Plots_Position_vs_Time/           # Raw and fitted position-time plots (.png)
│   ├── Tracking_Parameters/              # Tracking config files (.json)
│   └── Results/                          # Aggregated speed and optimization results
│       ├── fitted_speed.txt              # Linear fit results from get_speed.py
│       ├── optimization_results.csv      # Summary of GA and PSO experiments
│       ├── optimization_1.txt            # GA log for generation 1
│       ├── optimization_2.txt            # GA log for generation 2
│       ├── result_PSO.xlsx               # PSO experimental data (Excel)
│       ├── results_GA.xlsx               # GA experimental data (Excel)
│       └── results_archive.xlsx          # All experimental results
│
├── Simulations/                          # Simulated optimization results
│   ├── Genetic_Algorithm/                # GA simulation output files
│   ├── Particle_Swarm_Optimization/      # PSO simulation output files
│   └── Fitness_Function/                 # 2D projections of 8D fitness functions used in simulations
│
├── Code/                                 # Analysis and optimization scripts
│   ├── tracking.py                       # Extracts position data from video using OpenCV
│   ├── get_speed.py                      # Calculates speed from position-time data
│   ├── GA_measurements_and_simulation.py # Runs GA on experiments or simulations
│   ├── PSO_measurements.ipynb            # PSO (Google Colab-compatible notebook)
│   └── PSO_simulations.py                # PSO on synthetic fitness functions
│
├── LICENSE                               # Project license (GPL-3.0)
├── .gitignore                            # Git ignore file
├── README.md                             # Project documentation
└── CITATION.cff                          # Citation metadata (for GitHub citation feature)
```

---

## 🎯 Project Overview

This project explores data-driven optimization of underwater soft robots fabricated from liquid crystal elastomers. By applying GA and PSO directly to real-world performance metrics, the robots evolved to achieve faster swimming speeds and novel locomotion modes.

---

## 🎥 Experimental Videos

Videos are hosted on Zenodo due to file size limitations:

📦 [Zenodo Dataset (15158295)](https://zenodo.org/records/15158295)

**Filename format:**
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

> ⚠️ Filenames use the raw waveplate angle, not the computed polarization angle.

---

## 📊 Data Summary (`/Experimental/`)

### `/Data_Position_vs_Time/`
- `.txt` files containing time-position pairs extracted from videos.

### `/Plots_Position_vs_Time/`
- **Raw Plot:** `YYYYMMDD_..._directionID.png`  
- **Fitted Plot:** `YYYYMMDD_..._directionID_fit.png`

### `/Tracking_Parameters/`
- `.json` files specifying tracking parameters used by `tracking.py`.

### `/Results/`
- `fitted_speed.txt`: Fitted speed values.
- `optimization_results.csv`: Summary of all optimization experiments.
- `optimization_*.txt`: Logs of GA iterations, required to generate subsequent generations using `GA_measurements_and_simulation.py`.
- `.xlsx`: Structured results for both (GA and PSO) optimization experiments.

---

## 🧪 `/Simulations/`

Simulation results include GA/PSO runs and synthetic fitness function evaluations.

- `/Genetic_Algorithm/`: GA simulation performance results  
- `/Particle_Swarm_Optimization/`: PSO simulation performance results  
- `/Fitness_Function/`: 2D fitness function visualizations for different standard deviation values (σ)

---

## 💻 `/Code/`

### Analysis Scripts

- `tracking.py`:  
  **Note:** Before running the script, download the videos from the [Zenodo Repository](https://zenodo.org/records/15158295) and place them in `/Experimental/Movies_Optimization/`.  
  This script extracts position vs. time data from `.mp4` videos using `.json` configuration files.
  - Tracking is performed using **OpenCV (opencv-python)** with **adaptive thresholding**.
  - Outputs `.txt` files to `/Data_Position_vs_Time/`.  
  - If `save_plot=True`, it also saves `.png` plots to `/Plots_Position_vs_Time/`.  
  - Use `preview=True` to display a tracking preview during processing.

- `get_speed.py`:  
  Performs linear fitting on `.txt` files from `/Data_Position_vs_Time/` and:  
  - Appends results to `/Results/fitted_speed.txt`  
  - Saves `.png` plots of the fitted data to `/Plots_Position_vs_Time/`


### Optimization Scripts

Simulation outputs are saved to the appropriate subfolder in `/Simulations/`.

- `GA_measurements_and_simulation.py`: Runs GA for both experimental and simulation modes.  
  Set `experiment=True` or `False`.  
  - In experiment mode, it reads `/Experimental/Results/optimization_*.txt` and appends new generations.

- `PSO_measurements.ipynb`: PSO implementation designed for Google Colab.  
  Requires Google Sheet ID setup. Google Sheets used during experiments are mirrored in `/Experimental/Results/` as `.xlsx`. Each run updates the corresponding sheet.

- `PSO_simulations.py`: PSO applied to synthetic fitness functions.

---

## 🛠️ Usage Instructions

1. **Extract Position from Videos**
   ```bash
   python tracking.py
   ```
   - Inputs: `.mp4` from `/Movies_Optimization/`, `.json` from `/Tracking_Parameters/`
   - Outputs: `.txt` → `/Data_Position_vs_Time/`, `.png` → `/Plots_Position_vs_Time/`

2. **Calculate Speed**
   ```bash
   python get_speed.py
   ```
   - Input: `.txt` files in `/Data_Position_vs_Time/`
   - Output: Appends results to `/Results/fitted_speed.txt`

3. **Run GA or PSO on Experimental Data**
   - GA: Run `GA_measurements_and_simulation.py` with `experiment = True`
   - PSO: Run `PSO_measurements.ipynb` (requires Google Sheets access)

4. **Run GA or PSO Simulations**
   - GA: Set `experiment = False` in `GA_measurements_and_simulation.py`
     - Outputs: `.csv` → `/Simulations/Genetic_Algorithm/`, `.png` → `/Simulations/Fitness_Function/`
   - PSO: Run `PSO_simulations.py`
     - Outputs: `.csv` → `/Simulations/Particle_Swarm_Optimization/`

---

## 🧰 Development Environment

All `.py` scripts were developed and tested using:

- **Spyder 6.0.5**
- **Python 3.12.0**

---

## 📦 Python Dependencies

The following Python packages were used in this project:

| Package         | Version |
| --------------- | ------- |
| `opencv-python` | 4.11.0  |
| `matplotlib`    | 3.10.1  |
| `numpy`         | 2.2.4   |
| `tqdm`          | 4.67.1  |
| `joblib`        | 1.4.2   |
| `pandas`        | 2.2.3   |
| `Pillow`        | 11.1.0  |

You can install all dependencies with:

```bash
pip install opencv-python==4.11.0 matplotlib==3.10.1 numpy==2.2.4 tqdm==4.67.1 joblib==1.4.2 pandas==2.2.3 Pillow==11.1.0
```

---

## 📎 Citation

If you use this repository or dataset, please cite:

📄 [Zenodo DOI: 10.5281/zenodo.15158295](https://zenodo.org/records/15158295)

---

## 📜 License

This repository is licensed under the **GNU General Public License v3.0**.  
See the [LICENSE](LICENSE) file for full terms.
