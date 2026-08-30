import json
import re
import os
import webbrowser
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def parse_simc_4stat_json(json_path="results.json"):
    print(f"Loading {json_path}...")
    if not os.path.exists(json_path):
        print(f"ERROR: File '{json_path}' not found!")
        return pd.DataFrame()

    with open(json_path, "r", encoding="utf-8") as f:
        data_json = json.load(f)

    results_list = data_json.get("sim", {}).get("profilesets", {}).get("results", [])

    rows = []
    pattern = re.compile(
        r"H(?:aste)?_?(\d+)[_-]?M(?:astery)?_?(\d+)[_-]?C(?:rit)?_?(\d+)[_-]?V(?:ers)?_?(\d+)",
        re.IGNORECASE
    )

    for item in results_list:
        if not isinstance(item, dict):
            continue

        name = item.get("name", "")
        match = pattern.search(name)

        if match:
            haste = float(match.group(1))
            mastery = float(match.group(2))
            crit = float(match.group(3))
            vers = float(match.group(4))
            dps = float(item.get("mean", 0))

            if dps > 0:
                rows.append({
                    "name": name,
                    "haste": haste,
                    "mastery": mastery,
                    "crit": crit,
                    "vers": vers,
                    "dps": dps
                })

    df = pd.DataFrame(rows)
    print(f"Successfully extracted {len(df)} 4-stat profiles.")
    return df

def create_tetrahedral_plot(df, threshold_percent=0.02):
    if df.empty:
        print("No valid data found!")
        return

    pct_val = threshold_percent * 100
    pct_str = f"{pct_val:.1f}%".rstrip('0').rstrip('.') if pct_val % 1 != 0 else f"{int(pct_val)}%"

    max_dps = df["dps"].max()
    cutoff_dps = max_dps * (1.0 - threshold_percent)

    total_budget = df["haste"].iloc[0] + df["mastery"].iloc[0] + df["crit"].iloc[0] + df["vers"].iloc[0]
    
    h = df["haste"].values / total_budget
    m = df["mastery"].values / total_budget
    c = df["crit"].values / total_budget
    v = df["vers"].values / total_budget

    x = (2 * np.sqrt(2) / 3) * m - (np.sqrt(2) / 3) * c - (np.sqrt(2) / 3) * v
    y = (np.sqrt(6) / 3) * c - (np.sqrt(6) / 3) * v
    z = h - (1 / 3) * m - (1 / 3) * c - (1 / 3) * v

    df["x"], df["y"], df["z"] = x, y, z
    top_sim = df.loc[df["dps"].idxmax()]

    df_top = df[df["dps"] >= cutoff_dps].copy()
    df_rest = df[df["dps"] < cutoff_dps].copy()

    fig = go.Figure()

    # 1. Background points
    rest_hover = [
        f"<b>{r['name']}</b><br>"
        f"<b>DPS:</b> {r['dps']:,.0f}<br>"
        f"--------------------<br>"
        f"<b>Haste:</b> {r['haste']:.0f}<br>"
        f"<b>Mastery:</b> {r['mastery']:.0f}<br>"
        f"<b>Crit:</b> {r['crit']:.0f}<br>"
        f"<b>Versatility:</b> {r['vers']:.0f}"
        for _, r in df_rest.iterrows()
    ]

    fig.add_trace(go.Scatter3d(
        x=df_rest["x"], y=df_rest["y"], z=df_rest["z"],
        mode="markers",
        marker=dict(
            size=3,
            color=df_rest["dps"],
            colorscale="Plasma",
            cmin=df["dps"].min(),
            cmax=max_dps,
            opacity=0.25,
            showscale=False
        ),
        text=rest_hover,
        hoverinfo="text",
        hovertemplate="%{text}<extra></extra>",
        name="Other Sims"
    ))

    # 2. Top-performing cloud points
    top_hover = [
        f"<b>TOP {pct_str} PROFILE</b><br>"
        f"<b>Profile:</b> {r['name']}<br>"
        f"<b>DPS:</b> {r['dps']:,.0f}<br>"
        f"<b>Delta to MAX:</b> -{(1 - r['dps']/max_dps)*100:.2f}%<br>"
        f"--------------------<br>"
        f"<b>Haste:</b> {r['haste']:.0f}<br>"
        f"<b>Mastery:</b> {r['mastery']:.0f}<br>"
        f"<b>Crit:</b> {r['crit']:.0f}<br>"
        f"<b>Versatility:</b> {r['vers']:.0f}"
        for _, r in df_top.iterrows()
    ]

    fig.add_trace(go.Scatter3d(
        x=df_top["x"], y=df_top["y"], z=df_top["z"],
        mode="markers",
        marker=dict(
            size=6,
            color=df_top["dps"],
            colorscale="Plasma",
            cmin=df["dps"].min(),
            cmax=max_dps,
            opacity=0.9,
            line=dict(width=1, color="#FFD700"),
            colorbar=dict(title="DPS"),
            showscale=True
        ),
        text=top_hover,
        hoverinfo="text",
        hovertemplate="%{text}<extra></extra>",
        name=f"Top {pct_str} Performers"
    ))

    # 3. Highlight Peak Maximum
    top_x, top_y, top_z = top_sim["x"], top_sim["y"], top_sim["z"]
    
    top_hover_text = (
        f"<b>ABSOLUTE PEAK SIM</b><br>"
        f"<b>DPS:</b> {top_sim['dps']:,.0f}<br>"
        f"--------------------<br>"
        f"<b>Haste:</b> {top_sim['haste']:.0f}<br>"
        f"<b>Mastery:</b> {top_sim['mastery']:.0f}<br>"
        f"<b>Crit:</b> {top_sim['crit']:.0f}<br>"
        f"<b>Versatility:</b> {top_sim['vers']:.0f}"
    )

    fig.add_trace(go.Scatter3d(
        x=[top_x], y=[top_y], z=[top_z],
        mode="markers",
        marker=dict(
            size=12,
            color="gold",
            symbol="diamond",
            line=dict(width=2, color="#000000")
        ),
        text=[top_hover_text],
        hoverinfo="text",
        hovertemplate="%{text}<extra></extra>",
        name="Absolute Peak"
    ))

    # 4. Tetrahedron Wireframe & Axis Vertex Labels
    vertices = {
        "HASTE": (0, 0, 1),
        "MASTERY": (2 * np.sqrt(2) / 3, 0, -1/3),
        "CRIT": (-np.sqrt(2) / 3, np.sqrt(6) / 3, -1/3),
        "VERSATILITY": (-np.sqrt(2) / 3, -np.sqrt(6) / 3, -1/3)
    }

    edges = [
        ("HASTE", "MASTERY"), ("HASTE", "CRIT"), ("HASTE", "VERSATILITY"),
        ("MASTERY", "CRIT"), ("MASTERY", "VERSATILITY"), ("CRIT", "VERSATILITY")
    ]

    for start_node, end_node in edges:
        p1, p2 = vertices[start_node], vertices[end_node]
        fig.add_trace(go.Scatter3d(
            x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[p1[2], p2[2]],
            mode="lines",
            line=dict(color="rgba(200, 200, 200, 0.3)", width=2),
            showlegend=False,
            hoverinfo="skip"
        ))

    vx, vy, vz, vlabels = [], [], [], []
    for name, pos in vertices.items():
        vx.append(pos[0])
        vy.append(pos[1])
        vz.append(pos[2])
        vlabels.append(f"<b>{name} (100%)</b>")

    fig.add_trace(go.Scatter3d(
        x=vx, y=vy, z=vz,
        mode="markers+text",
        marker=dict(size=6, color="#FFFFFF"),
        text=vlabels,
        textposition="top center",
        name="Stat Axes"
    ))

    fig.update_layout(
        title=dict(
            text=f"4-Stat Distribution Tetrahedron (Haste, Mastery, Crit, Vers)<br><sup>Max DPS: {max_dps:,.0f} | Budget: {total_budget:.0f} | Threshold (>= {100 - pct_val:.1f}% Max): {cutoff_dps:,.0f} DPS</sup>",
            x=0.5,
            y=0.97,
            font=dict(size=20)
        ),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor="rgb(15, 15, 22)",
            camera=dict(
                eye=dict(x=1.3, y=1.3, z=0.9)
            )
        ),
        template="plotly_dark",
        margin=dict(l=0, r=0, b=0, t=80)
    )

    output_html = "moonkin_4stat_tetrahedron.html"
    
    html_content = fig.to_html(include_plotlyjs="cdn", full_html=True)

    # Injected HTML/JS UI elements: Top-Left Toggle Button with Dynamic Countdown
    auto_spin_js = """
    <button id="spin-toggle-btn" style="
        position: absolute;
        top: 15px;
        left: 15px;
        z-index: 9999;
        background: #1e1e28;
        color: #ffb703;
        border: 1px solid #ffb703;
        padding: 8px 14px;
        border-radius: 6px;
        font-family: sans-serif;
        font-size: 13px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.5);
        transition: all 0.2s ease;
        min-width: 170px;
        text-align: center;
    ">Auto-Rotation: ON</button>

    <script>
    document.addEventListener("DOMContentLoaded", function() {
        var gd = document.querySelector('.plotly-graph-div');
        var btn = document.getElementById('spin-toggle-btn');
        if (!gd || !btn) return;

        var radius = 1.8;
        var theta = Math.atan2(1.3, 1.3);
        var currentZ = 0.9;
        var autoSpinEnabled = true;
        var isUserInteracting = false;
        
        var countdownSecs = 20;
        var countdownTimer = null;

        function rotateCamera() {
            if (!autoSpinEnabled || isUserInteracting) return;
            theta += 0.005;
            var x = radius * Math.cos(theta);
            var y = radius * Math.sin(theta);
            
            Plotly.relayout(gd, {
                'scene.camera.eye': {x: x, y: y, z: currentZ}
            });
        }

        setInterval(rotateCamera, 30);

        function updateButtonText() {
            if (!autoSpinEnabled) {
                btn.innerText = "Auto-Rotation: OFF";
                btn.style.borderColor = "#666666";
                btn.style.color = "#888888";
            } else if (isUserInteracting) {
                btn.innerText = "Resuming in " + countdownSecs + "s...";
                btn.style.borderColor = "#00b4d8";
                btn.style.color = "#00b4d8";
            } else {
                btn.innerText = "Auto-Rotation: ON";
                btn.style.borderColor = "#ffb703";
                btn.style.color = "#ffb703";
            }
        }

        function handleUserInteraction() {
            if (!autoSpinEnabled) return;
            
            isUserInteracting = true;
            countdownSecs = 20;
            updateButtonText();

            if (countdownTimer) clearInterval(countdownTimer);

            countdownTimer = setInterval(function() {
                countdownSecs--;
                if (countdownSecs <= 0) {
                    clearInterval(countdownTimer);
                    countdownTimer = null;

                    // Read current manual camera state before resuming
                    if (gd.layout && gd.layout.scene && gd.layout.scene.camera && gd.layout.scene.camera.eye) {
                        var eye = gd.layout.scene.camera.eye;
                        radius = Math.sqrt(eye.x * eye.x + eye.y * eye.y);
                        theta = Math.atan2(eye.y, eye.x);
                        currentZ = eye.z;
                    }

                    isUserInteracting = false;
                    updateButtonText();
                } else {
                    updateButtonText();
                }
            }, 1000);
        }

        btn.addEventListener('click', function() {
            autoSpinEnabled = !autoSpinEnabled;
            if (countdownTimer) {
                clearInterval(countdownTimer);
                countdownTimer = null;
            }

            if (autoSpinEnabled) {
                isUserInteracting = false;
                updateButtonText();
            } else {
                isUserInteracting = true;
                updateButtonText();
            }
        });

        gd.addEventListener('mousedown', handleUserInteraction);
        gd.addEventListener('wheel', handleUserInteraction);
        gd.addEventListener('touchstart', handleUserInteraction);
    });
    </script>
    </body>
    """

    html_content = html_content.replace("</body>", auto_spin_js)

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Saved 3D tetrahedral plot with countdown button as: {output_html}")
    
    try:
        webbrowser.open("file://" + os.path.realpath(output_html))
    except Exception:
        pass

if __name__ == "__main__":
    df_results = parse_simc_4stat_json("results.json")
    create_tetrahedral_plot(df_results, threshold_percent=0.02)