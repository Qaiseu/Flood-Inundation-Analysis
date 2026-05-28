# Flood Inundation Analysis (DEM-Based)

A Python-based flood inundation analysis project developed for the **Smart Water Lab Series – Specialized Experiment 4**.  
This project uses a Digital Elevation Model (DEM) to simulate flooding under different water levels, visualize inundation extent, calculate flood depth and flood volume, and validate physical correctness through dynamic simulations.

---

## Project Overview

Flood inundation analysis is an important technique used in:

- Flood risk assessment
- Hydrological studies
- Emergency management
- Urban planning
- Watershed analysis

This project simulates flooding by comparing terrain elevation values against specified water levels using a DEM-based approach.

The system identifies flooded regions, calculates inundation depth, computes flooded area percentages, estimates flood storage volume, and generates both static visualizations and animated flood progression.

---

## Features

### Core Features

- Synthetic DEM generation (100×100 terrain grid)
- Flood extent simulation using water-level thresholding
- Inundation depth calculation
- Flooded area percentage analysis
- Dynamic rising-water simulation
- Physical validation checks
- Scientific visualizations using matplotlib

### Optional Extensions Implemented

- Flood volume calculation
- Water Level vs Flood Volume analysis
- Animated flood inundation GIF
- Edge-case validation testing

---

## Flood Inundation Logic

A DEM cell is considered flooded when:

```math
Elevation < WaterLevel
```

Flood depth is calculated as:

```math
Depth = WaterLevel - Elevation
```

Flooded area percentage:

```math
Flooded Percentage = (Flooded Cells / Total Cells) × 100
```

Flood volume:

```math
Volume = Σ(Depth × Cell Area)
```

Assuming:

- DEM resolution = 30 m × 30 m
- Cell area = 900 m²

---

## Technologies Used

- Python 3.10+
- NumPy
- Matplotlib
- ImageIO

---

## Project Structure

```text
Flood-Inundation-Analysis/
│
├── flood_inundation.py
├── dem_data.npy
├── prompt_log.md
├── README.md
├── requirements.txt
│
├── Results/
│   ├── dem_overview.png
│   ├── flood_extent_40m.png
│   ├── flood_extent_50m.png
│   ├── flood_curve.png
│   ├── flood_volume_curve.png
│   └── flood_animation.gif
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Qaiseu/Flood-Inundation-Analysis.git
cd Flood-Inundation-Analysis
```

Install required libraries:

```bash
pip install -r requirements.txt
```

---

## Running the Project

Run the main script:

```bash
python flood_inundation.py
```

---

## Output Files

| File | Description |
|---|---|
| `dem_data.npy` | Generated DEM dataset |
| `dem_overview.png` | DEM visualization |
| `flood_extent_40m.png` | Flood extent at 40 m |
| `flood_extent_50m.png` | Flood extent at 50 m |
| `flood_curve.png` | Water level vs flooded area |
| `flood_volume_curve.png` | Water level vs flood volume |
| `flood_animation.gif` | Animated flood progression |

---

## Example Results

### DEM Statistics

```text
Minimum elevation: 30.00 m
Maximum elevation: 80.00 m
Mean elevation: 53.71 m
```

### Flood Simulation Results

| Water Level | Flooded Area | Maximum Depth | Flood Volume |
|---|---|---|---|
| 40 m | 4.22% | 10.00 m | 1.38 million m³ |
| 50 m | 31.09% | 20.00 m | 14.46 million m³ |

---

## Dynamic Flood Simulation

Water levels from 40 m to 50 m were simulated dynamically.

The flooded area increased monotonically:

```text
40 m → 4.22%
41 m → 5.54%
42 m → 7.28%
43 m → 8.92%
44 m → 10.67%
45 m → 12.90%
46 m → 15.64%
47 m → 18.74%
48 m → 22.44%
49 m → 26.12%
50 m → 31.09%
```

This confirms physically realistic flood behavior.

---

## Validation

The project includes automatic validation checks:

- Monotonic flood growth verification
- Maximum depth validation
- Percentage range checks
- Edge-case testing

### Validation Results

```text
Overall Validation: PASS
```

---

## Visualization Examples

### Flood Extent Maps

The project generates side-by-side visualizations including:

- DEM terrain map
- Flood extent overlay
- Inundation depth heatmap

### Animated Flood Progression

The animated GIF demonstrates flood expansion as water levels rise from 40 m to 50 m.

---

## Scientific Interpretation

Results demonstrate that flood extent strongly depends on terrain elevation.  
Low-lying depressions flood first, while higher terrain remains dry until water levels rise sufficiently.

The relationship between water level and flooded area is nonlinear, showing that certain elevation bands contain larger connected lowland regions.

Flood volume increases rapidly with water level because both inundation depth and flooded area expand simultaneously.

---

## Future Improvements

Possible future extensions include:

- Real-world DEM integration
- Flood routing algorithms
- Watershed-based analysis
- Building footprint barriers
- Interactive GIS visualization
- Streamlit web dashboard
- Real rainfall-driven flooding

---

## Learning Outcomes

This project demonstrates skills in:

- Spatial analysis
- Hydrological modeling
- Scientific computing
- NumPy array processing
- Data visualization
- Environmental simulation
- Flood-risk analysis
- Python-based scientific programming

---

## Author

Douae Qais  
Master's Student in Computer Science and Technology
