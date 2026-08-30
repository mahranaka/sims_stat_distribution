# sims_stat_distribution

A Python-based workflow designed for **World of Warcraft (Balance Druid / Moonkin)** to generate secondary stat budget matrices, execute SimulationCraft runs, and visualize the resulting DPS distributions using interactive 3D tetrahedral (simplex) plots.

---

## 🌐 Live Interactive Demo

View the live, interactive tetrahedral plot directly in your browser:
👉 <a href="https://mahranaka.github.io/sims_stat_distribution/moonkin_4stat_tetrahedron.html" target="_blank" rel="noopener noreferrer">View Interactive Plotly Report</a>

---

## ⚠️ Disclaimer

* **Base Profile:** The example profile embedded in the grid generator uses the top-simming race profile from Dreamgrove's official race sims ([dreamgrove.gg/static/sims/racesims2m.htm](https://www.dreamgrove.gg/static/sims/racesims2m.htm)).
* **4-Stat Budget Matrix:** Unlike traditional 3-stat ternary plots, this script evaluates the complete secondary stat trade-off across **Haste**, **Mastery**, **Crit**, and **Versatility** simultaneously within a constant stat budget.

---

## 🌟 Features

* **4D Grid Generation (`generate_grid.py`):** Automatically creates a `.simc` file featuring a full 4-stat secondary budget matrix (Haste, Mastery, Crit, Versatility) with configurable step sizes.
* **JSON Parsing (`plot_3d_stats.py`):** Robust parser for SimulationCraft JSON results (`sim.profilesets.results`), extracting 4-stat variations and mean DPS outputs.
* **Interactive Tetrahedral Visualization:** Projects 4D stat compositions ($Haste + Mastery + Crit + Versatility = \text{Constant Budget}$) into a 3D Cartesian tetrahedron space using Plotly.
* **Top-Performer Highlighting:** Color-codes the entire stat volume via the **Plasma** palette while scaling and highlighting the top-performing stat zones (e.g., Top 2% DPS).
* **Wireframe Axes & Custom Hover Tooltips:** Renders a translucent 3D wireframe connecting all 4 stat vertices ($100\%$ markers) and detailed hover cards showing exact stat breakdowns, DPS, and peak markers.

---

## 🛠️ Requirements

Install the necessary Python dependencies using `pip`:

    pip install pandas numpy plotly

---

## 🚀 Quick Start

### 1. Generate the Simulation Input File
Run the grid generator script to build `moonkin_grid_4stat.simc` containing your base character profile, Action Priority List (APL), and 4-stat matrix:

    python generate_grid.py

### 2. Run SimulationCraft
Execute the generated file in SimulationCraft (CLI or GUI) and output the results as a JSON file named `results.json`:

    simc moonkin_grid_4stat.simc json2=results.json

> **Note:** [SimulationCraft](https://www.simulationcraft.org/) must be installed and added to your system's `PATH` environment variable for the `simc` command to work in your terminal. Alternatively, you can run the generated `.simc` file directly through the SimulationCraft GUI or specify the full path to `simc.exe`.

### 3. Generate the Interactive Plot
Process the simulation results and generate the interactive 3D HTML plot:

    python plot_3d_stats.py

The resulting `moonkin_4stat_tetrahedron.html` will automatically open in your default browser.

---

## ⚙️ Configuration & Customization

* **Stat Budget & Step Size:** You can adjust the secondary stat budget and step size inside `generate_grid.py`:
  
      generate_4stat_grid(output_filename="moonkin_grid_4stat.simc", budget=3000, step=150)

* **Top Performance Threshold:** Adjust the highlighted top-performer zone percentage in `plot_3d_stats.py`:
  
      # Set to 0.02 for Top 2%, 0.05 for Top 5%, etc.
      create_tetrahedral_plot(df_results, threshold_percent=0.02)

---

## 📊 Example Output

The output is an interactive dark-themed 3D Plotly HTML file featuring:
* A 3D tetrahedral wireframe marking $100\%$ allocations for **Haste**, **Mastery**, **Crit**, and **Versatility**.
* A full color-gradient point cloud across the interior volume based on the **Plasma** color palette.
* Gold diamond marker highlighting the absolute peak DPS configuration.
* Clean hover tooltips displaying full stat values ($H, M, C, V$) and exact DPS numbers.