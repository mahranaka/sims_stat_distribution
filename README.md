# sims_stat_distribution

A Python-based workflow designed for **World of Warcraft (Balance Druid / Moonkin) - (can be used for any dps/tank spec - need to change generate_profiles.py)** to generate secondary stat budget matrices, execute SimulationCraft runs, and visualize the resulting DPS distributions using interactive 3D tetrahedral (simplex) plots.

---

## 🌐 Live Interactive Demo

View the live, interactive tetrahedral plot directly in your browser:
👉 <a href="https://mahranaka.github.io/sims_stat_distribution/moonkin_4stat_tetrahedron.html" target="_blank" rel="noopener noreferrer">View Interactive Plotly Report</a>

---

## ⚠️ Disclaimer

* **Base Profile:** The example profile embedded in the grid generator uses the [top sim by clankz](https://www.raidbots.com/simbot/report/iEvzkAYC8XCPr1JrAVNXw5) with a total stat budget of 3236 (flask removed and converted into stat budget).
* **4-Stat Budget Matrix:** Evaluates secondary stat trade-offs across **Haste**, **Mastery**, **Crit**, and **Versatility** simultaneously within a constant stat budget.

---

## 🌟 Features

* **Dynamic Grid Generation (`generate_profiles.py`):** Automatically creates a `.simc` file with a 4-stat secondary budget matrix, calculating dynamic step sizes so stat combinations reach exact $0$ boundary values.
* **JSON Parsing (`plot_3d_stats.py`):** Extracts profile stat variations and mean DPS outputs from SimulationCraft JSON results (`sim.profilesets.results`).
* **Interactive Tetrahedral Visualization:** Maps 4D stat compositions ($Haste + Mastery + Crit + Versatility = \text{Constant Budget}$) into a 3D Cartesian tetrahedron space using Plotly.
* **Smooth Camera Auto-Rotation:** Features automatic camera orbiting in the output HTML that pauses during manual interaction and seamlessly resumes rotation from your new viewpoint after 20 seconds of inactivity.
* **Top-Performer Highlighting & Tooltips:** Color-codes points via the **Plasma** palette, highlights the top-performing stat threshold, and displays custom hover cards with exact stat breakdowns ($H, M, C, V$) and DPS metrics.

---

## 🛠️ Requirements

Install the necessary Python dependencies using `pip`:

    pip install pandas numpy plotly

---

## 🚀 Quick Start

### 1. Generate the Simulation Input File
Run the profile generator script to build `moonkin_grid_4stat.simc` containing your base character profile, Action Priority List (APL), and 4-stat matrix:

    python generate_profiles.py

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

* **Stat Budget & Steps:** Adjust the secondary stat budget and target division steps inside `generate_profiles.py`:
  
      generate_4stat_grid_dynamic(output_filename="moonkin_grid_4stat.simc", budget=3049, steps_per_axis=20)

* **Top Performance Threshold:** Adjust the highlighted top-performer zone percentage in `plot_3d_stats.py`:
  
      # Set to 0.02 for Top 2%, 0.05 for Top 5%, etc.
      create_tetrahedral_plot(df_results, threshold_percent=0.02)

---

## 📊 Example Output

The output is an interactive dark-themed 3D Plotly HTML file (`moonkin_4stat_tetrahedron.html`) featuring:
* A 3D tetrahedral wireframe marking $100\%$ allocations for **Haste**, **Mastery**, **Crit**, and **Versatility**.
* A color-gradient point cloud across the interior volume based on the **Plasma** color palette.
* A gold diamond marker indicating the absolute peak DPS configuration.
* Hover tooltips displaying exact stat values ($H, M, C, V$) and DPS figures.