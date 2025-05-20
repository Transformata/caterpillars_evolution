# Swimming Robots Data Repository

This repository contains experimental data, analysis scripts, and metadata related to the movement and optimization of soft swimming robots powered by light. The data is organized into subfolders by experiment type and file type.

---

## 📁 Folder Structure

### `/Swimming_Robots_Data/`
The repository is divided into two main sections: `/Experimental/` and `/Simulations/`. This README focuses on the `/Experimental/` section.

---

### `/Experimental/`
Contains all data, movies, and analysis results from experiments with soft swimming robots.

#### `/Movies_Optimisation/`
Raw video files from optimization experiments.

🚨 **Note:** Due to file size limitations, `.mp4` videos are not stored directly in this GitHub repository.  
They are available via Zenodo in a `.zip` archive:  
👉 [https://zenodo.org/records/15158295](https://zenodo.org/records/15158295)

- **Filename format:**  
  `YYYYMMDD_frequency_length_dyeConcentration_thickness_curlLength_power_tailDirection_angleID_directionID.mp4`  
  - Example: `230506_0200mHz_06mm_0%2_90um_3mm_2000mW_1_082deg5_L1.mp4`
- **Details:**
  - **Tail Direction (1/0):** Indicates the initial bend direction of the robot's right edge at room temperature.
    - `1` – Edge bends upward  
    - `0` – Edge bends downward
  - **Direction ID (L/R):** Indicates the scan direction (Left or Right) and trial number.
  - **Angle ID:** Represents the waveplate setting (see [Polarization Angle Calculation](#polarization-angle-calculation)).
  - **Measurements:** Five trials per direction (left and right).

#### `/Movies_Self-Oscillation/`
Videos from self-oscillation experiments. Each parameter set has a single measurement.
- Same format as `/Movies_Optimisation/` but without trial numbers.
**Example:** `230506_0200mHz_06mm_0%2_90um_3mm_2000mW_1_082deg5_L.mp4`.


#### `/Data_Position_vs_Time/`
Position vs. time data extracted from each video.

- **Filename format:**  
  `YYYYMMDD_frequency_length_dyeConcentration_thickness_curlLength_power_tailDirection_angleID_directionID.txt`
- Logs time-position pairs for each robot trial.

#### `/Plots_Position_vs_Time/`
Graphical plots of position vs. time data.

- **Raw Plot:**  
  `YYYYMMDD_..._directionID.png`
- **Fitted Plot (Linear Fit):**  
  `YYYYMMDD_..._directionID_fit.png`

#### `/Tracking_Parameters/`
Parameter files for tracking robot position in videos.

- **Filename format:**  
  `YYYYMMDD_..._tracking_parameters.txt`

#### `/Results/`
Summarized data and final analysis.

- **`fitted_speed.txt`:**  
  Appends speed values and fitted parameters extracted from position data.
- **`Optimisation_Results.csv`:**  
  Detailed results from Genetic Algorithm (GA1, GA2) and Particle Swarm Optimization (PSO1, PSO2) experiments.

  - **Key columns:**
    - `iteration no`, `robot no`
    - Robot parameters: frequency, length, dye concentration, thickness, curl length, laser power, tail direction, waveplate angle
    - Speeds for each trial (`L1–R5`)
    - Fitness function value (highest average speed)

---

## 📐 Polarization Angle Calculation

The polarization angle was derived from the measured position of the half-wave plate. An angle of **0°** between the polarization direction and the laser scan direction corresponds to a **waveplate position of 30°**. The conversion formula is:

**Polarization–Scan Angle** = 2 × (measured angle − 30°)

**Example:** A waveplate position of 82.5° corresponds to an effective polarization angle of:  
(82.5 − 30) × 2 = **105°**
⚠️ **Note:** This formula was **not used** in the naming of video files or their corresponding data (`.txt`) and plot (`.png`) files. Those files use the **raw waveplate angle** as recorded during the experiment.

---

## 🛠️ Usage Instructions

1. **Track Robot Position:**
   - Run `tracking_script.py` using parameters from `/Tracking_Parameters/`
   - Outputs:
     - `.txt` data files in `/Data_Position_vs_Time/`
     - `.png` plots in `/Plots_Position_vs_Time/`

2. **Calculate Robot Speed:**
   - Run `speed.py` on `.txt` data
   - Outputs:
     - Appends speed values to `/Results/fitted_speed.txt`
     - Creates fitted plots in `/Plots_Position_vs_Time/`

3. **Review Raw Data:**
   - Access raw videos in `/Movies_Optimisation/` and `/Movies_Self-Oscillation/`
   - Use plots and `.txt` files to evaluate movement

4. **Check Tracking Parameters:**
   - Refer to `/Tracking_Parameters/` for setup used in each video

5. **Analyze Optimization Performance:**
   - Use `/Results/Optimisation_Results.csv` for detailed algorithm outcomes

---

## 📂 `/Code/` Folder

Python scripts used for analysis:

- **`tracking_script.py`**  
  Tracks robot positions in videos  
  - **Inputs:** video + parameters  
  - **Outputs:** `.txt` and `.png` files in matching subfolders

- **`speed.py`**  
  Fits linear models to position data and calculates speed  
  - **Inputs:** `.txt` files from `/Data_Position_vs_Time/`  
  - **Outputs:** appends results to `/Results/fitted_speed.txt`, saves plots

---

## 📎 Citation

If you use this dataset or code, please cite the Zenodo record:  
👉 [https://zenodo.org/records/15158295](https://zenodo.org/records/15158295)

---

## 📜 License

This repository is licensed under the [GNU General Public License v3.0](LICENSE).

---



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
│   └── /fitness_function/            # 2D visualizations of fitness function
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
- Raw and fitted `.png` plots of motion.

### `/Tracking_Parameters/`
- `.json` files with parameter settings for each video.

### `/Results/`
- `fitted_speed.txt`: List of fitted speed values.
- `Optimisation_Results.csv`: Full GA/PSO results.
- `optimization_*.txt`: Logs of experimental runs.
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

- `tracking.py`: Extracts position-time data using `.json` tracking files.
- `get_speed.py`: Performs linear fitting and speed calculation.

### Optimization Algorithms

- `GA_measurements_and_simulation.py`: Runs GA for both measurements and simulations.
- `PSO_measurements.ipynb`: Jupyter-based implementation for PSO.
- `PSO_simulations.py`: PSO applied to synthetic fitness landscapes.

---

## 🛠️ Usage Instructions

1. **Extract Position from Videos**
   ```bash
   python tracking.py
   ```
   - Input: `.mp4` + `.json` from `/Tracking_Parameters/`
   - Output: `.txt` → `/Data_Position_vs_Time/`, plots → `/Plots_Position_vs_Time/`

2. **Calculate Speed**
   ```bash
   python get_speed.py
   ```
   - Reads `.txt` data and appends to `fitted_speed.txt`
   - Saves fitted plots

3. **Run GA or PSO**
   - GA: `GA_measurements_and_simulation.py`
   - PSO: `PSO_measurements.ipynb` or `PSO_simulations.py`

---

## 📎 Citation

If you use this repository or dataset, please cite:

📄 [Zenodo DOI: 10.5281/zenodo.15158295](https://zenodo.org/records/15158295)

---

## 📜 License

This repository is licensed under the **GNU General Public License v3.0**.  
See the [LICENSE](LICENSE) file.

---
