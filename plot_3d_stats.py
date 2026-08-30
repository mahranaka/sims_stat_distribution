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

    max_dps = df["dps"].max()
    cutoff_dps = max_dps * (1.0 - threshold_percent)

    # Normalize coordinates to fractions (sum = 1)
    total_budget = df["haste"].iloc[0] + df["mastery"].iloc[0] + df["crit"].iloc[0] + df["vers"].iloc[0]
    
    h = df["haste"].values / total_budget
    m = df["mastery"].values / total_budget
    c = df["crit"].values / total_budget
    v = df["vers"].values / total_budget

    # Map 4D simplex to 3D Cartesian coordinates (regular tetrahedron vertices)
    x = (2 * np.sqrt(2) / 3) * m - (np.sqrt(2) / 3) * c - (np.sqrt(2) / 3) * v
    y = (np.sqrt(6) / 3) * c - (np.sqrt(6) / 3) * v
    z = h - (1 / 3) * m - (1 / 3) * c - (1 / 3) * v

    # Assign 3D coordinates BEFORE pulling top_sim
    df["x"], df["y"], df["z"] = x, y, z
    top_sim = df.loc[df["dps"].idxmax()]

    df_top = df[df["dps"] >= cutoff_dps]
    df_rest = df[df["dps"] < cutoff_dps]

    fig = go.Figure()

    # 1. Background points (Small, semi-transparent)
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
        text=[f"<b>{r['name']}</b><br>DPS: {r['dps']:,.0f}<br>H:{r['haste']:.0f} M:{r['mastery']:.0f} C:{r['crit']:.0f} V:{r['vers']:.0f}" for _, r in df_rest.iterrows()],
        hoverinfo="text",
        name="Other Sims"
    ))

    # 2. Top-performing cloud points (Larger, bright)
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
        text=[f"<b>TOP {threshold_percent*100:.1f}%</b><br>{r['name']}<br>DPS: {r['dps']:,.0f}" for _, r in df_top.iterrows()],
        hoverinfo="text",
        name="Top Performers"
    ))

# 3. Highlight Peak Maximum with clean hover info and stats
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
        name="Absolute Peak"
    ))

    # 4. Add Tetrahedron Wireframe & Axis Vertex Labels
    vertices = {
        "HASTE": (0, 0, 1),
        "MASTERY": (2 * np.sqrt(2) / 3, 0, -1/3),
        "CRIT": (-np.sqrt(2) / 3, np.sqrt(6) / 3, -1/3),
        "VERSATILITY": (-np.sqrt(2) / 3, -np.sqrt(6) / 3, -1/3)
    }

    # Edges connecting all 4 vertices
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

    # Vertex markers and labels
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
        title=f"4-Stat Distribution Tetrahedron (Haste, Mastery, Crit, Vers)<br><sup>Max DPS: {max_dps:,.0f} | Budget: {total_budget:.0f}</sup>",
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor="rgb(15, 15, 22)"
        ),
        template="plotly_dark",
        margin=dict(l=0, r=0, b=0, t=60)
    )

    output_html = "moonkin_4stat_tetrahedron.html"
    fig.write_html(output_html)
    print(f"Saved 3D tetrahedral plot as: {output_html}")
    webbrowser.open("file://" + os.path.realpath(output_html))

if __name__ == "__main__":
    df_results = parse_simc_4stat_json("results.json")
    create_tetrahedral_plot(df_results, threshold_percent=0.02)