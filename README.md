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

