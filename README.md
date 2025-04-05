Polarisation angle
For the polarisation angle, the directly measured value was the position of the half-wave plate. The angle between the polarisation direction and the scan direction was 0° for a waveplate position of 30°. To calculate the angle between the polarisation direction and the scan direction, we used the formula:
angle between polarisation and scan direction=2(measured angle - 30°)






# Swimming Robots Data Repository

This repository contains experimental data, analysis files, and metadata related to the movement and optimization of soft swimming robots powered by light. The data is organized into subfolders based on file type and experiment type.

---

## Folder Structure

### `/Swimming_Robots_Data/`
The repository is divided into two main sections: `Experimental` and `Simulations`. This README focuses on the `Experimental` section.

#### `/Experimental/`
Contains data, movies, and results related to experiments with soft swimming robots.

##### `/Movies_Optimisation/` 
Raw video files from optimization experiments.
- **Filename Format:** `YYYYMMDD_frequency_length_dyeConcentration_thickness_curlLength_power_tailDirection_angleID_directionID.mp4`
  - **Example:** `230506_0200mHz_06mm_0%2_90um_3mm_2000mW_1_082deg5_L1.mp4`
- **Details:**
  - **Tail Direction (1/0):** Binary identifier indicating the initial bending direction of the robot's right edge in water at room temperature:
    - `1`: Edge bends upward.
    - `0`: Edge bends downward.
  - **Direction ID (L/R):** Indicates the laser scan direction (Left or Right) and the trial number.  
  - **Angle ID:** Represents the waveplate position. To calculate the angle between the polarisation direction and the scan direction, use the formula:  
    \[
    \text{Angle between polarisation and scan direction} = (\text{angleID} - 30) \times 2
    \]  
    For example, an angleID of 82.5 corresponds to an angle of \((82.5 - 30) \times 2 = 105^\circ\).  
  - **Measurements:** Five trials per direction (left and right).

##### `/Movies_Self-Oscillation/`
Videos from self-oscillation experiments where each parameter set has a single measurement.
- **Filename Format:**  
  Similar to the `Movies_Optimisation` folder but without trial numbers.
  - **Example:** `230506_0200mHz_06mm_0%2_90um_3mm_2000mW_1_082deg5_L.mp4`.

##### `/Data_Position_vs_Time/`
Position vs. time data extracted from each video.
- **Filename Format:** `YYYYMMDD_frequency_length_dyeConcentration_thickness_curlLength_power_tailDirection_angleID_directionID.txt`
  - **Example:** `230506_0200mHz_06mm_0%2_90um_3mm_2000mW_1_082deg5_L1.txt`
- **Description:** Logs robot position over time in time-position pairs.

##### `/Plots_Position_vs_Time/`
Plot files of position vs. time data:
- **Filename Formats:**
  - **Raw Position Plot:** `YYYYMMDD_frequency_length_dyeConcentration_thickness_curlLength_power_tailDirection_angleID_directionID.png`
    - **Example:** `230506_0200mHz_06mm_0%2_90um_3mm_2000mW_1_082deg5_L1.png`.
  - **Fitted Line Plot:** `YYYYMMDD_frequency_length_dyeConcentration_thickness_curlLength_power_tailDirection_angleID_directionID_fit.png`
    - **Example:** `230506_0200mHz_06mm_0%2_90um_3mm_2000mW_1_082deg5_L1_fit.png`.

##### `/Tracking_Parameters/`
Contains `.txt` files specifying tracking parameters for position data extraction:
- **Filename Format:** `YYYYMMDD_frequency_length_dyeConcentration_thickness_curlLength_power_angleID_tracking_parameters.txt`
  - **Example:** `230506_0200mHz_06mm_0%2_90um_3mm_2000mW_1_082deg5_tracking_parameters.txt`.

##### `/Results/`  
Summarized data and optimization results.
- **Filename:** `fitted_speed.txt`  
  - **Description:** Summarizes line fits (speed slopes) for comparative analysis.  
- **Filename:** `Optimisation_Results.csv`  
  - **Description:** Detailed optimization results from Genetic Algorithm (GA1, GA2) and Particle Swarm Optimization (PSO1, PSO2).
  - **Columns:**
    - **Iteration and Robot Identifiers:**
      - `iteration no`: The iteration number in the optimization process.  
      - `robot no`: The robot's identifier within the iteration.  
    - **Parameters:**
      - `frequency [Hz]`: Laser scanning frequency.  
      - `length [mm]`: Robot body length.  
      - `dye [%mol]`: Dye concentration in the elastomer.  
      - `thickness [µm]`: Thickness of the LCE film.  
      - `curl length [mm]`: Curl length of the robot body.  
      - `laser power [W]`: Laser power applied during the experiment.  
      - `right side [down 0, up 1]`: Binary identifier indicating the robot's tail direction (`0` for downward, `1` for upward).  
      - `waveplate angle [deg]`: Represents the waveplate position. To calculate the angle between the polarisation direction and the scan direction, use the formula:  
    	\[
    	\text{Angle between polarisation and scan direction} = (\text{angleID} - 30) \times 2
    	\]  
    	For example, an angleID of 82.5 corresponds to an angle of \((82.5 - 30) \times 2 = 105^\circ\).  
    - **Trial Speeds:** `L1–R5 [cm/min]`: Speeds measured during trials with the laser scanning from left (`L1–L5`) and right (`R1–R5`).  
    - **Fitness Function:** Represents the highest average speed across trials for each robot.  

---

#### `/Code/`
Python scripts used for experimental data analysis.

- **`tracking_script.py`:**  
  Tracks robot positions in `/Movies_Optimisation/` videos and generates `.txt` and `.png` files saved in `/Data_Position_vs_Time/` and `/Plots_Position_vs_Time/`.
  - **Inputs:**  
    - Video files and parameters from `/Tracking_Parameters/`.
  - **Outputs:**  
    - Folder `YYYYMMDD_frequency_length_dyeConcentration_thickness_curlLength_power_tailDirection_angleID_directionID` with subfolders `data` and `plot`
    - Position vs. time `.txt` files in `data` folder
    - Position vs. time `.png` files in `data` folder

- **`speed.py`:**  
  Fits linear functions to position vs. time data and calculates robot speed.
  - **Inputs:**  
    - `.txt` files from `/Data_Position_vs_Time/`.
  - **Outputs:**  
    - adding lines with Speed values and fitted parameters in `/Results/fitted_speed.txt`.
    - Fitted data plots in `/Plots_Position_vs_Time/`.

---

## Usage

1. **Track Robot Position:**
   - Run `tracking_script.py` with the appropriate parameters from `/Tracking_Parameters/` to generate position vs. time `.txt` files and `.png` plots for videos in `/Movies_Optimisation/`.

2. **Calculate Robot Speed:**
   - Use `speed.py` to perform a linear fit on the `.txt` files in `/Data_Position_vs_Time/` and calculate robot speeds.

3. **Analyze Raw Data:**
   - Use `/Movies_Optimisation/` and `/Movies_Self-Oscillation/` for video files.
   - `/Data_Position_vs_Time/` for position vs. time data.
   - `/Plots_Position_vs_Time/` for visualized raw and fitted data.

4. **Tracking Parameter Reference:**
   - Use `/Tracking_Parameters/` to locate tracking settings for specific experiments.

5. **Evaluate Performance:**
   - `/Results/fitted_speed.txt` provides speed summary data.
   - `/Results/Optimisation_Results.csv` contains detailed optimization results.

---

## Exceptions:
- For `240310_0100mHz_12mm_1%0_50um_1mm_3500mW_1_097deg5` there are two set of measurements:
  - `240310_0100mHz_12mm_1%0_50um_1mm_3500mW_1_097deg5_v1`: First set of measurements.
  - `240310_0100mHz_12mm_1%0_50um_1mm_3500mW_1_097deg5`: Second set of measurements.