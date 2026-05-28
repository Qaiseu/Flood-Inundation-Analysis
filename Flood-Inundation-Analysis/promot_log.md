# Prompt Log - Specialized Experiment 4
# Flood Inundation Analysis

# Prompt1 DEM Data Preparation:
Create Part 1 of a flood inundation analysis project in Python called flood_inundation.py.

Requirements:

1. Create a function named `load_dem()`.

2. Generate a synthetic Digital Elevation Model (DEM) as a NumPy array with dimensions 100×100.

3. The terrain should resemble realistic topography rather than pure random noise:

   * Include a gradual elevation slope across the domain.
   * Add several hills or undulations using mathematical functions such as sine and cosine waves.
   * Add a small amount of random noise to make the terrain more natural.
   * Final elevation values should generally range between 30 m and 80 m.

4. Save the generated DEM to a file named `dem_data.npy`.

5. Display basic statistics:

   * DEM shape
   * Minimum elevation
   * Maximum elevation
   * Mean elevation

6. Create a visualization of the DEM using matplotlib:

   * Use a terrain-style colormap
   * Include title, axis labels, and colorbar
   * Save the figure as `dem_overview.png`

7. Return the DEM array from the function.

8. Add clear comments and docstrings suitable for a university hydrology or water-resources experiment.

9. Include a main block:

```python
if __name__ == "__main__":
    dem = load_dem()
```

The code should be complete, runnable, and focused only on DEM generation and visualization. Do not implement flood calculations yet.

# Ai generated result:
Done. Here's a summary of what `flood_inundation.py` does:

- **`load_dem()`** generates a 100×100 synthetic DEM combining a regional slope, four sine/cosine-based undulations, and ±1.5 m uniform noise, then rescales to **30–80 m**.
- Saves the array to `dem_data.npy` and the terrain-colormap plot to `dem_overview.png`.
- Prints shape, min, max, and mean elevation to the console.

**Output files created:**
- `dem_data.npy` (80 KB)
- `dem_overview.png` (70 KB)


# Prompt2 Implementing flood inundation calculation:
Extend the existing flood_inundation.py project by implementing Part 2: Flood Simulation.

Requirements:

1. Create a function:

```python
def calculate_flood(dem, water_level):
```

2. The function must:

* Create a boolean flood mask:

  * flooded if elevation < water_level

* Calculate inundation depth:

  * depth = water_level - elevation for flooded cells
  * depth = 0 for non-flooded cells

* Calculate flooded area percentage:

  * (number of flooded cells / total cells) × 100

3. Return:

```python
flooded_mask, depth, flooded_percentage
```

4. Add detailed comments and docstrings explaining the hydrological meaning of each calculation.

5. In the main block:

   * Load or generate the DEM
   * Set water_level = 40
   * Call calculate_flood()
   * Print:

```text
Water Level: 40 m
Flooded Cells: XXXX
Flooded Area: XX.XX %
Maximum Flood Depth: XX.XX m
Average Flood Depth: XX.XX m
```

6. Add validation checks:

   * Flooded percentage must be between 0 and 100
   * Depth values must never be negative

7. Keep all existing DEM generation functionality unchanged.

The code should be clean, modular, and ready for later visualization steps.

# Ai generated result:
Everything works. The script now:

- **`calculate_flood(dem, water_level)`** — creates a boolean flood mask (`dem < water_level`), computes inundation depth (zero for dry cells, positive for flooded), and returns the flooded percentage. Includes `assert` validation that percentage is in [0, 100] and depths are non-negative.

- **Main block** — generates the DEM, then runs the flood calculation with `water_level = 40.0 m` and prints all required diagnostics.

# comment:
At a flood water level of 40 m, 422 cells out of the total 10,000 DEM cells were classified as flooded, corresponding to 4.22% of the study area. The maximum inundation depth reached 10.00 m, which is consistent with the difference between the water level and the minimum terrain elevation. The average inundation depth within flooded regions was 3.63 m, indicating that most flooded cells experienced relatively shallow water depths while only a few low-lying depressions reached the maximum depth. These results are physically realistic because the majority of the generated terrain elevations are above 40 m.

# prompt3 Visualization:
Extend the existing flood_inundation.py project by implementing Part 3: Flood Visualization.

Requirements:

Create a function:

```python
def visualize_flood(dem, flooded_mask, depth, water_level, output_file):
```

The function must create a single figure containing three subplots:

1. Original DEM

   * Display DEM using grayscale colormap ("gray")
   * Add title "Digital Elevation Model"
   * Include colorbar labeled "Elevation (m)"

2. Flood Extent Overlay

   * Display DEM in grayscale
   * Overlay flooded cells in blue using the flood mask
   * Use transparency (alpha ≈ 0.5)
   * Title should include the water level

3. Inundation Depth Map

   * Display flood depth using matplotlib's "Blues" colormap
   * Include colorbar labeled "Flood Depth (m)"
   * Title "Inundation Depth"

Additional Requirements:

* Use figsize large enough for clear visualization
* Add axis labels
* Use tight_layout()
* Save the figure using the supplied filename
* Close figures after saving

Main Program:

1. Generate/load DEM
2. Calculate flood for water level = 40 m
3. Create visualization and save as:

flood_extent_40m.png

4. Calculate flood for water level = 50 m
5. Create visualization and save as:

flood_extent_50m.png

6. Print confirmation messages when files are saved

Keep all existing DEM generation and flood calculation functionality unchanged.

Add comments and docstrings appropriate for a university flood inundation experiment.

# Ai generated result:
Everything works. The script now includes:

- **`visualize_flood(dem, flooded_mask, depth, water_level, output_file)`** — creates a 3-panel figure (grayscale DEM, flood extent overlay with translucent blue, inundation depth with Blues colormap), each with title, axis labels, and appropriate colorbars.

- **Main block** — runs flood calculations at **40 m** and **50 m**, prints diagnostics for both, saves `flood_extent_40m.png` and `flood_extent_50m.png`, and prints confirmation messages.

# comment:
Flood extent maps were generated for water levels of 40 m and 50 m. At 40 m, flooding was limited to a few isolated low-elevation depressions, resulting in a flooded area of only 4.22% of the study region. When the water level increased to 50 m, floodwaters expanded into additional low-lying terrain and several flooded regions became interconnected, increasing the inundated area to 31.09%. The inundation depth maps show the greatest depths occurring in the deepest topographic depressions, while shallow flooding occurs near the boundaries of inundated zones. These results demonstrate the strong influence of terrain elevation on flood extent and depth distribution.

# prompt4 Dynamic simulation:
Extend the existing flood_inundation.py project by implementing Part 4: Dynamic Simulation of Rising Water Levels.

Requirements:

Create a function:

```python
def simulate_rising_water(dem):
```

The function must:

1. Generate water levels from 40 m to 50 m inclusive using 1 m increments.

2. For each water level:

   * Call calculate_flood()
   * Store flooded area percentage
   * Print:

```text
Water Level = XX m | Flooded Area = XX.XX %
```

3. Create a line plot:

   * x-axis = Water Level (m)
   * y-axis = Flooded Area (%)
   * marker = circle
   * grid enabled
   * title = "Water Level vs Flooded Area Percentage"

4. Save figure as:

```text
flood_curve.png
```

5. Verify monotonic increase:

```python
np.all(np.diff(percentages) >= 0)
```

6. Print:

```text
Monotonic Increase: True
```

if all flooded percentages increase or remain equal.

7. Return:

   * water_levels
   * flooded_percentages

8. In the main program:

   * call simulate_rising_water(dem)
   * print the minimum and maximum flooded percentages obtained

Keep all previous functionality unchanged.
Add comments and docstrings suitable for a flood risk assessment experiment.

# Ai generated result:
Everything runs correctly. The script now includes:

- **`simulate_rising_water(dem)`** — steps water levels from 40–50 m in 1 m increments, prints each level and flooded percentage, verifies monotonic increase (`True`), plots and saves `flood_curve.png`, and returns both arrays.

- **Main block** — runs the two static flood visualizations as before, then calls `simulate_rising_water(dem)` and prints the min/max flooded area percentages (4.22% and 31.09%).

# comment:
A dynamic flood simulation was performed by increasing water levels from 40 m to 50 m in 1 m increments. The flooded area percentage increased steadily from 4.22% at 40 m to 31.09% at 50 m. The monotonic increase check returned True, confirming that flood extent consistently expanded as water level rose. The relationship between water level and flooded area was nonlinear, indicating that certain elevation bands within the DEM contain larger contiguous low-lying regions. This behavior is physically realistic because floodplain expansion often accelerates when water reaches broader terrain depressions.

# prompt5 Validation:
Extend the existing flood_inundation.py project by implementing Part 5: Physical Validation.

Create a function:

```python
def validate_results(dem):
```

The function must perform the following checks:

1. Monotonic Flood Growth

   * Compute flooded percentages for water levels 40 m through 50 m
   * Verify:

     ```python
     np.all(np.diff(percentages) >= 0)
     ```
   * Print:

     ```
     Monotonic Flood Growth: PASS
     ```

2. Maximum Depth Check
   For water levels 40 m and 50 m:

   Expected:

   ```python
   water_level - np.min(dem)
   ```

   Compare against:

   ```python
   np.max(depth)
   ```

   Print expected and actual values.

3. Percentage Range Check
   Verify all flooded percentages satisfy:

   ```python
   0 <= percentage <= 100
   ```

   Print PASS or FAIL.

4. Edge Case 1
   Water level below minimum elevation:

   ```python
   water_level = np.min(dem) - 1
   ```

   Expected flooded area:

   ```
   0%
   ```

5. Edge Case 2
   Water level above maximum elevation:

   ```python
   water_level = np.max(dem) + 1
   ```

   Expected flooded area:

   ```
   100%
   ```

6. Print a final validation summary:

   ```
   ============================
   VALIDATION SUMMARY
   ============================
   Monotonic Growth: PASS
   Depth Check: PASS
   Percentage Range: PASS
   Edge Case Low Water: PASS
   Edge Case High Water: PASS
   Overall Validation: PASS
   ```

7. Call validate_results(dem) at the end of the main program.

Keep all previous functionality unchanged.
Use clear comments and docstrings suitable for an academic flood inundation experiment.

# Ai generated result:
All 7 validation checks pass. The script now includes:

- **`validate_results(dem)`** — runs six physical-consistency tests:
  1. **Monotonic Flood Growth** — verifies flooded area never decreases as water rises
  2. **Max Depth Check** — confirms `max(depth) == water_level - min(dem)` at WL=40 and WL=50
  3. **Percentage Range** — all percentages in [0, 100]
  4. **Edge Case Low** — water below min elevation yields 0% flooded
  5. **Edge Case High** — water above max elevation yields 100% flooded
  6. **Overall Validation** — all PASS / FAIL rolled up at the end

- Called at the end of `main`, printing a formatted summary table.

# Optional extension:
# Prompt Flood Volume:
Extend the existing flood_inundation.py project by adding an optional extension: Flood Volume Calculation.

Requirements:

1. Create a new function:

```python
def calculate_flood_volume(depth, cell_size=30):
```

2. Compute cell area:

```python
cell_area = cell_size ** 2
```

3. Compute total flood volume:

```python
volume = np.sum(depth) * cell_area
```

4. Return volume in cubic meters (m³).

5. Add detailed docstrings explaining:

   * depth is measured in meters
   * cell size is measured in meters
   * resulting volume is measured in cubic meters

6. In the main program:

For both water levels:

* 40 m
* 50 m

calculate and print flood volume.

Example format:

```text
Water Level: 40 m
Flood Volume: 1378000.25 m³

Water Level: 50 m
Flood Volume: 14520000.41 m³
```

7. Add validation:

```python
assert volume >= 0
```

8. Create a second dynamic analysis:

For water levels 40–50 m:

* calculate flood volume at each level
* store volumes in a list

Generate a plot:

Title:
"Water Level vs Flood Volume"

x-axis:
Water Level (m)

y-axis:
Flood Volume (m³)

Use markers and grid.

Save as:

```text
flood_volume_curve.png
```

9. Print:

```text
Minimum Flood Volume: ...
Maximum Flood Volume: ...
```

10. Keep all previous experiment functionality unchanged.
    Add comments suitable for a hydrology and flood-risk analysis project.

# Ai generated result:
All working. The script now includes:

- **`calculate_flood_volume(depth, cell_size=30)`** — computes total flood volume as `sum(depth) * cell_size²`, validated with `assert volume >= 0`.

- **Volume printed** for both WL=40 m (1,377,699.36 m³) and WL=50 m (14,462,769.92 m³) alongside existing diagnostics.

- **Dynamic volume curve** — iterates WL 40–50 m, plots `flood_volume_curve.png` with square markers and grid, prints min/max volumes.

# Prompt Animation:
Extend the flood_inundation.py project by implementing the optional extension: Animated Flood Inundation GIF.

Requirements:

1. Create a function:

```python
def create_flood_animation(dem):
```

2. Simulate water levels from 40 m to 50 m inclusive.

3. For each water level:

   * Calculate flood mask and depth
   * Generate a flood extent figure similar to the existing visualization
   * Save as temporary frame:

```text
frame_40.png
frame_41.png
...
frame_50.png
```

4. Use the imageio library to combine all frames into:

```text
flood_animation.gif
```

5. Animation settings:

   * duration ≈ 0.7 seconds per frame
   * loop forever

6. After GIF creation:

   * delete temporary frame files automatically

7. Print:

```text
Created: flood_animation.gif
Frames: 11
```

8. Add appropriate comments and docstrings.

9. Call create_flood_animation(dem) at the end of the main program after all analyses are complete.

10. Keep all previous experiment functionality unchanged.

11. If imageio is not installed, display a clear message explaining how to install it:

```bash
pip install imageio
```
# Ai generated result:
Everything works. The script now includes:

- **`create_flood_animation(dem)`** — iterates WL 40–50 m, saves a 3-panel frame for each via `visualize_flood`, assembles them into a looping GIF with 0.7 s per frame using `imageio`, then deletes all temporary `frame_*.png` files. If `imageio` is missing, prints an install hint instead of crashing.

- **Output**: `flood_animation.gif` (587 KB, 11 frames), temp frames cleaned up automatically.