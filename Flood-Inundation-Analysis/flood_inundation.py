"""
flood_inundation.py — Part 1: Synthetic DEM generation and visualisation.

Hydrology / water-resources experiment.
Creates a 100×100 Digital Elevation Model with realistic terrain (slope,
undulations, and small-scale noise) and saves it for later flood analysis.
"""

import os
import numpy as np
import matplotlib.pyplot as plt


def load_dem():
    """Generate, save, display stats for, and plot a synthetic 100×100 DEM.

    Returns
    -------
    dem : np.ndarray, shape (100, 100)
        The generated digital elevation model (metres).
    """
    # ------------------------------------------------------------------ #
    # 1. Build a coordinate grid
    # ------------------------------------------------------------------ #
    nx, ny = 100, 100
    x = np.linspace(0, 10, nx)
    y = np.linspace(0, 10, ny)
    X, Y = np.meshgrid(x, y)

    # ------------------------------------------------------------------ #
    # 2. Gradual regional slope  (north-east → south-west)
    # ------------------------------------------------------------------ #
    slope = 2.0 * X + 1.5 * Y

    # ------------------------------------------------------------------ #
    # 3. Hills and undulations via sine/cosine combinations
    # ------------------------------------------------------------------ #
    rng = np.random.default_rng(42)

    hill1 = 6.0 * np.sin(0.8 * X) * np.cos(1.2 * Y)
    hill2 = 4.0 * np.cos(1.6 * X + 0.5 * Y)
    hill3 = 3.0 * np.sin(1.0 * (X + Y)) * np.cos(0.6 * (X - Y))
    hill4 = 5.0 * np.sin(2.0 * X) + 4.0 * np.cos(1.8 * Y)

    undulations = hill1 + hill2 + hill3 + hill4

    # ------------------------------------------------------------------ #
    # 4. Small-scale random noise  (±1.5 m)
    # ------------------------------------------------------------------ #
    noise = rng.uniform(-1.5, 1.5, (nx, ny))

    # ------------------------------------------------------------------ #
    # 5. Combine and shift into the range 30–80 m
    # ------------------------------------------------------------------ #
    dem = slope + undulations + noise

    # Rescale so min = 30, max = 80
    dmin, dmax = dem.min(), dem.max()
    dem = 30.0 + (dem - dmin) * (80.0 - 30.0) / (dmax - dmin)

    # ------------------------------------------------------------------ #
    # 6. Save to disk
    # ------------------------------------------------------------------ #
    np.save("dem_data.npy", dem)

    # ------------------------------------------------------------------ #
    # 7. Print basic statistics
    # ------------------------------------------------------------------ #
    print(f"DEM shape:       {dem.shape}")
    print(f"Minimum elev.:   {dem.min():.2f} m")
    print(f"Maximum elev.:   {dem.max():.2f} m")
    print(f"Mean elev.:      {dem.mean():.2f} m")

    # ------------------------------------------------------------------ #
    # 8. Visualise
    # ------------------------------------------------------------------ #
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(dem, origin="lower", cmap="terrain",
                   extent=[0, nx, 0, ny])
    cbar = fig.colorbar(im, ax=ax, label="Elevation (m)")
    ax.set_title("Synthetic Digital Elevation Model")
    ax.set_xlabel("Column index")
    ax.set_ylabel("Row index")
    fig.tight_layout()
    fig.savefig("dem_overview.png", dpi=150)
    plt.close(fig)

    return dem


def calculate_flood(dem, water_level):
    """Identify flooded cells, compute inundation depth, and report extent.

    Hydrological interpretation
    ---------------------------
    A cell is considered 'flooded' when the water surface elevation
    (water_level) exceeds the ground elevation (dem).  The inundation
    depth at each flooded cell represents the depth of standing water
    above the terrain; non-flooded cells have zero depth.

    Parameters
    ----------
    dem : np.ndarray
        Digital Elevation Model (metres).
    water_level : float
        Uniform water-surface elevation (metres).

    Returns
    -------
    flooded_mask : np.ndarray of bool, same shape as dem
        True where elevation < water_level, False otherwise.
    depth : np.ndarray, same shape as dem
        Inundation depth (metres) — zero for dry cells, positive for
        flooded cells.
    flooded_percentage : float
        Percentage of the domain that is inundated, in [0, 100].
    """
    flooded_mask = dem < water_level

    depth = np.where(flooded_mask, water_level - dem, 0.0)

    total_cells = dem.size
    flooded_cells = np.count_nonzero(flooded_mask)
    flooded_percentage = (flooded_cells / total_cells) * 100.0

    # Validation checks
    assert 0.0 <= flooded_percentage <= 100.0, (
        f"Flooded percentage {flooded_percentage:.2f}% is out of [0, 100]."
    )
    assert np.all(depth >= 0.0), (
        "Negative depth values encountered — check water_level and DEM."
    )

    return flooded_mask, depth, flooded_percentage


def calculate_flood_volume(depth, cell_size=30):
    """Compute total flood‑water volume from inundation depths.

    Each grid cell represents a cell_size × cell_size square on the
    ground.  Water depth (m) integrated over each cell's area gives
    the volume of stored flood water.

    Parameters
    ----------
    depth : np.ndarray
        Inundation depth per cell (metres); zero on dry cells.
    cell_size : float, optional
        Side length of a square grid cell (metres).  Default 30 m.

    Returns
    -------
    volume : float
        Total flood volume (m³).
    """
    cell_area = cell_size ** 2
    volume = float(np.sum(depth) * cell_area)
    assert volume >= 0.0, f"Negative flood volume ({volume:.2f} m³) computed."
    return volume


def visualize_flood(dem, flooded_mask, depth, water_level, output_file):
    """Create a three-panel flood visualisation and save to disk.

    Panel 1 — Digital Elevation Model (grayscale).
    Panel 2 — Flood extent: DEM underlay with flooded cells overlaid in
              translucent blue.
    Panel 3 — Inundation depth shown with the Blues colormap.

    Parameters
    ----------
    dem : np.ndarray
        Digital Elevation Model (metres).
    flooded_mask : np.ndarray of bool
        True for inundated cells.
    depth : np.ndarray
        Water depth above terrain (metres); zero on dry cells.
    water_level : float
        Uniform water-surface elevation used for the title.
    output_file : str
        Path for the saved figure.
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Shared imshow arguments
    kwargs = dict(origin="lower", extent=[0, dem.shape[1], 0, dem.shape[0]])

    # ---- Panel 1: Original DEM (grayscale) ---- #
    im0 = axes[0].imshow(dem, cmap="gray", **kwargs)
    cbar0 = fig.colorbar(im0, ax=axes[0], label="Elevation (m)")
    axes[0].set_title("Digital Elevation Model")
    axes[0].set_xlabel("Column index")
    axes[0].set_ylabel("Row index")

    # ---- Panel 2: Flood extent overlay ---- #
    axes[1].imshow(dem, cmap="gray", **kwargs)
    axes[1].imshow(
        flooded_mask, cmap="Blues", alpha=0.5, **kwargs
    )
    axes[1].set_title(f"Flood Extent (Water Level = {water_level} m)")
    axes[1].set_xlabel("Column index")
    axes[1].set_ylabel("Row index")

    # ---- Panel 3: Inundation depth ---- #
    im2 = axes[2].imshow(depth, cmap="Blues", **kwargs)
    cbar2 = fig.colorbar(im2, ax=axes[2], label="Flood Depth (m)")
    axes[2].set_title("Inundation Depth")
    axes[2].set_xlabel("Column index")
    axes[2].set_ylabel("Row index")

    fig.tight_layout()
    fig.savefig(output_file, dpi=150)
    plt.close(fig)


def simulate_rising_water(dem):
    """Simulate flood extent across a range of rising water levels.

    Iterates from 40 m to 50 m (1 m steps), computes the flooded area
    percentage at each level, and produces a stage‑damage‑style curve
    that shows how inundation grows with water‑surface elevation.

    Parameters
    ----------
    dem : np.ndarray
        Digital Elevation Model (metres).

    Returns
    -------
    water_levels : np.ndarray
        Water levels tested (m).
    flooded_percentages : np.ndarray
        Corresponding flooded‑area percentages.
    """
    water_levels = np.arange(40.0, 51.0, 1.0)
    flooded_percentages = np.empty_like(water_levels)

    for i, wl in enumerate(water_levels):
        _, _, pct = calculate_flood(dem, wl)
        flooded_percentages[i] = pct
        print(f"Water Level = {wl:.0f} m | Flooded Area = {pct:.2f} %")

    # Monotonicity check — as water rises, flooded area must not shrink
    monotonic = np.all(np.diff(flooded_percentages) >= 0.0)
    print()
    print(f"Monotonic Increase: {monotonic}")

    # Plot the stage‑damage curve
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(water_levels, flooded_percentages, marker="o", linestyle="-")
    ax.set_title("Water Level vs Flooded Area Percentage")
    ax.set_xlabel("Water Level (m)")
    ax.set_ylabel("Flooded Area (%)")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig("flood_curve.png", dpi=150)
    plt.close(fig)
    print("Saved: flood_curve.png")

    return water_levels, flooded_percentages


def validate_results(dem):
    """Run a suite of physical‑consistency checks on the flood model.

    Tests include monotonic growth, depth limits, percentage bounds,
    and edge‑case behaviour (no water, total inundation).

    Parameters
    ----------
    dem : np.ndarray
        Digital Elevation Model (metres).
    """
    results = {}

    # ---- 1. Monotonic flood growth ---- #
    wls = np.arange(40.0, 51.0, 1.0)
    pcts = np.array([calculate_flood(dem, wl)[2] for wl in wls])
    monotonic = bool(np.all(np.diff(pcts) >= 0.0))
    results["Monotonic Growth"] = "PASS" if monotonic else "FAIL"
    print(f"Monotonic Flood Growth: {results['Monotonic Growth']}")

    # ---- 2. Maximum depth check at water levels 40 and 50 ---- #
    dem_min = np.min(dem)
    for wl in (40.0, 50.0):
        _, depth, _ = calculate_flood(dem, wl)
        expected = wl - dem_min
        actual = np.max(depth)
        ok = np.isclose(actual, expected)
        results[f"Depth Check (WL={wl:.0f})"] = "PASS" if ok else "FAIL"
        print(f"Depth Check (WL={wl:.0f} m): expected max depth = {expected:.2f} m, "
              f"actual max depth = {actual:.2f} m — "
              f"{results[f'Depth Check (WL={wl:.0f})']}")

    # ---- 3. Percentage range check ---- #
    all_in_range = bool(np.all((pcts >= 0.0) & (pcts <= 100.0)))
    results["Percentage Range"] = "PASS" if all_in_range else "FAIL"
    print(f"Percentage Range Check: {results['Percentage Range']}")

    # ---- 4. Edge case — water below minimum elevation ---- #
    _, _, pct_low = calculate_flood(dem, dem_min - 1.0)
    low_ok = bool(np.isclose(pct_low, 0.0))
    results["Edge Case Low Water"] = "PASS" if low_ok else "FAIL"
    print(f"Edge Case (WL < min elev): "
          f"flooded area = {pct_low:.2f}% — "
          f"{results['Edge Case Low Water']}")

    # ---- 5. Edge case — water above maximum elevation ---- #
    _, _, pct_high = calculate_flood(dem, np.max(dem) + 1.0)
    high_ok = bool(np.isclose(pct_high, 100.0))
    results["Edge Case High Water"] = "PASS" if high_ok else "FAIL"
    print(f"Edge Case (WL > max elev): "
          f"flooded area = {pct_high:.2f}% — "
          f"{results['Edge Case High Water']}")

    # ---- 6. Summary table ---- #
    all_pass = all(v == "PASS" for v in results.values())
    results["Overall Validation"] = "PASS" if all_pass else "FAIL"

    print()
    print("=" * 33)
    print("     VALIDATION SUMMARY")
    print("=" * 33)
    for key in ("Monotonic Growth", "Depth Check (WL=40)",
                "Depth Check (WL=50)", "Percentage Range",
                "Edge Case Low Water", "Edge Case High Water",
                "Overall Validation"):
        print(f"  {key:<26} {results.get(key, 'N/A')}")
    print("=" * 33)


def create_flood_animation(dem):
    """Generate an animated GIF of rising flood inundation.

    Produces individual frame images for water levels 40–50 m, then
    assembles them into a looping GIF with imageio.  Temporary frame
    files are deleted after the GIF is created.

    Parameters
    ----------
    dem : np.ndarray
        Digital Elevation Model (metres).
    """
    try:
        import imageio
    except ImportError:
        print(
            "imageio is required to create the animation.\n"
            "Install it with:  pip install imageio"
        )
        return

    water_levels = np.arange(40.0, 51.0, 1.0)
    frame_paths = []

    for wl in water_levels:
        flooded_mask, depth, _ = calculate_flood(dem, wl)

        path = f"frame_{int(wl):02d}.png"
        visualize_flood(dem, flooded_mask, depth, wl, path)
        frame_paths.append(path)

    frames = [imageio.v3.imread(p) for p in frame_paths]
    imageio.mimsave("flood_animation.gif", frames, duration=0.7, loop=0)

    for p in frame_paths:
        os.remove(p)

    print()
    print(f"Created: flood_animation.gif")
    print(f"Frames: {len(frames)}")


if __name__ == "__main__":
    dem = load_dem()

    for wl in (40.0, 50.0):
        flooded_mask, depth, flooded_pct = calculate_flood(dem, wl)
        volume = calculate_flood_volume(depth)

        flooded_cells = np.count_nonzero(flooded_mask)
        max_depth = depth.max()
        mean_depth = depth[depth > 0].mean() if flooded_cells > 0 else 0.0

        print()
        print(f"Water Level: {wl} m")
        print(f"Flooded Cells: {flooded_cells}")
        print(f"Flooded Area: {flooded_pct:.2f} %")
        print(f"Maximum Flood Depth: {max_depth:.2f} m")
        print(f"Average Flood Depth: {mean_depth:.2f} m")
        print(f"Flood Volume: {volume:.2f} m\u00b3")

        out = f"flood_extent_{int(wl)}m.png"
        visualize_flood(dem, flooded_mask, depth, wl, out)
        print(f"Saved: {out}")

    wls, pcts = simulate_rising_water(dem)
    print()
    print(f"Minimum Flooded Area: {pcts.min():.2f} %")
    print(f"Maximum Flooded Area: {pcts.max():.2f} %")

    # ---- Dynamic flood‑volume analysis ---- #
    volumes = []
    for wl in wls:
        _, depth, _ = calculate_flood(dem, wl)
        volumes.append(calculate_flood_volume(depth))
    volumes = np.array(volumes)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(wls, volumes, marker="s", linestyle="-")
    ax.set_title("Water Level vs Flood Volume")
    ax.set_xlabel("Water Level (m)")
    ax.set_ylabel("Flood Volume (m\u00b3)")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig("flood_volume_curve.png", dpi=150)
    plt.close(fig)
    print()
    print(f"Minimum Flood Volume: {volumes.min():.2f} m\u00b3")
    print(f"Maximum Flood Volume: {volumes.max():.2f} m\u00b3")
    print("Saved: flood_volume_curve.png")

    print()
    validate_results(dem)

    print()
    create_flood_animation(dem)