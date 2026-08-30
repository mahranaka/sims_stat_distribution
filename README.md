# sims_stat_distribution

A Python-based workflow designed for **World of Warcraft (Balance Druid / Moonkin)** to generate secondary stat budget matrices, execute SimulationCraft runs, and visualize the resulting DPS distributions using interactive 2D ternary plots.

---

## 🌐 Live Interactive Demo

View the live, interactive ternary plot directly in your browser:
👉 <a href="https://mahranaka.github.io/sims_stat_distribution/moonkin_ternary_stats.html" target="_blank" rel="noopener noreferrer">View Interactive Plotly Report</a>

---

## ⚠️ Disclaimer

* **Base Profile:** The example profile embedded in the grid generator uses the top-simming race profile from Dreamgrove's official race sims ([dreamgrove.gg/static/sims/racesims2m.htm](https://www.dreamgrove.gg/static/sims/racesims2m.htm)).
* **Versatility Neglected:** Versatility is intentionally excluded/zeroed out in this matrix to focus exclusively on evaluating the trade-offs and distribution ratios across Haste, Mastery, and Crit.

---

## 🌟 Features

* **Grid Generation (`generate_grid.py`):** Automatically creates a `.simc` file featuring a realistic secondary stat budget (Haste, Mastery, Crit) with defined step sizes.
* **JSON Parsing (`plot_3d_stats.py`):** Robust parser for SimulationCraft JSON results (`sim.profilesets.results`), extracting profile stat variations and mean DPS outputs.
* **Interactive Ternary Visualization:** Maps 3D secondary stat combinations (Haste + Mastery + Crit = Constant Budget) onto an interactive 2D ternary plot built with Plotly.
* **Dynamic Zone Highlighting:** Automatically highlights the top-performing stat zones (e.g., Top 2% or Top 5% DPS) with a custom convex hull boundary and adaptive labels.

---

## 🛠️ Requirements

Install the necessary Python dependencies using `pip`:

    pip install pandas numpy plotly scipy

---

## 🚀 Quick Start

### 1. Generate the Simulation Input File
Run the grid generator script to build `moonkin_grid.simc` containing your base character profile, Action Priority List (APL), and stat matrix:

    python generate_grid.py

### 2. Run SimulationCraft
Execute the generated file in SimulationCraft (CLI or GUI) and output the results as a JSON file named `results.json`:

    simc moonkin_grid.simc json2=results.json

> **Note:** [SimulationCraft](https://www.simulationcraft.org/) must be installed and added to your system's `PATH` environment variable for the `simc` command to work in your terminal. Alternatively, you can run the generated `.simc` file directly through the SimulationCraft GUI or specify the full path to `simc.exe`.

### 3. Generate the Interactive Plot
Process the simulation results and generate the interactive HTML ternary plot:

    python plot_3d_stats.py

The resulting `moonkin_ternary_stats.html` will automatically open in your default browser.

---

## ⚙️ Configuration & Customization

* **Stat Budget & Step Size:** You can adjust the secondary stat budget and step size inside `generate_grid.py`:
  
      generate_grid_file(output_filename="moonkin_grid.simc", budget=3049, step=100)

* **Top Performance Threshold:** Adjust the highlighted top-performer zone percentage in `plot_3d_stats.py`:
  
      # Set to 0.02 for Top 2%, 0.05 for Top 5%, etc.
      create_ternary_stat_plot(df_results, threshold_percent=0.02)

---

## 📊 Example Output

The output is an interactive dark-themed Plotly HTML file featuring:
* **Mastery** (Top Axis), **Haste** (Left Axis), and **Crit** (Right Axis).
* A full color-gradient spectrum across the entire stat grid based on the **Plasma** color palette.
* A highlighted boundary and marker scaling for top-performing stat allocations.
* Detailed hover tooltips showing exact stat numbers, DPS, and delta percentage to the absolute maximum.