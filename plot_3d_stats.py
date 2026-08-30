import json
import re
import os
import webbrowser
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def parse_simc_json(json_path="results.json"):
    print(f"Loading {json_path}...")
    if not os.path.exists(json_path):
        print(f"ERROR: File '{json_path}' not found!")
        return pd.DataFrame()

    with open(json_path, "r", encoding="utf-8") as f:
        data_json = json.load(f)

    sim_data = data_json.get("sim", {})
    profilesets = sim_data.get("profilesets", {})
    results_list = profilesets.get("results", [])

    rows = []
    pattern = re.compile(r"H(?:aste)?_?(\d+)[_-]?M(?:astery)?_?(\d+)[_-]?C(?:rit)?_?(\d+)", re.IGNORECASE)

    for item in results_list:
        if not isinstance(item, dict):
            continue

        name = item.get("name", "")
        match = pattern.search(name)

        if match:
            haste = float(match.group(1))
            mastery = float(match.group(2))
            crit = float(match.group(3))
            dps = float(item.get("mean", 0))

            if dps > 0:
                rows.append({
                    "name": name,
                    "haste": haste,
                    "mastery": mastery,
                    "crit": crit,
                    "dps": dps
                })

    df = pd.DataFrame(rows)
    print(f"Successfully extracted {len(df)} stat profiles.")
    return df

def create_ternary_stat_plot(df, threshold_percent=0.02):
    if df.empty:
        print("No valid data found in DataFrame!")
        return
        
    # Dynamische Prozent-Labels erzeugen
    pct_val = threshold_percent * 100
    pct_str = f"{pct_val:.1f}%".rstrip('0').rstrip('.') if pct_val % 1 != 0 else f"{int(pct_val)}%"
    
    max_dps = df["dps"].max()
    cutoff_dps = max_dps * (1.0 - threshold_percent)
    
    top_sim = df.loc[df["dps"].idxmax()]
    total_budget = df["mastery"].iloc[0] + df["haste"].iloc[0] + df["crit"].iloc[0]

    df_top = df[df["dps"] >= cutoff_dps].copy()
    df_rest = df[df["dps"] < cutoff_dps].copy()

    fig = go.Figure()

    # 1. Base points (Hell & gut sichtbar im Hintergrund)
    fig.add_trace(go.Scatterternary(
        mode="markers",
        a=df_rest["mastery"],
        b=df_rest["haste"],
        c=df_rest["crit"],
        marker=dict(
            symbol="circle",
            color=df_rest["dps"],
            colorscale="Plasma",
            cmin=df["dps"].min(),
            cmax=max_dps,
            size=7,
            opacity=0.85,
            showscale=False
        ),
        text=[f"<b>Profile:</b> {row['name']}<br><b>DPS:</b> {row['dps']:,.1f}" for _, row in df_rest.iterrows()],
        hoverinfo="text",
        name="Other Sims"
    ))

    # 2. Highlighted Top-Zone Points (Dynamische Beschriftung)
    fig.add_trace(go.Scatterternary(
        mode="markers",
        a=df_top["mastery"],
        b=df_top["haste"],
        c=df_top["crit"],
        marker=dict(
            symbol="circle",
            color=df_top["dps"],
            colorscale="Plasma",
            cmin=df["dps"].min(),
            cmax=max_dps,
            size=11,
            opacity=1.0,
            line=dict(width=1.5, color="#FFD700"),
            colorbar=dict(title="DPS", len=0.75, x=1.02),
            showscale=True
        ),
        text=[f"<b>TOP {pct_str} Profile:</b> {row['name']}<br><b>DPS:</b> {row['dps']:,.1f}<br><b>Delta to MAX:</b> -{(1 - row['dps']/max_dps)*100:.2f}%" for _, row in df_top.iterrows()],
        hoverinfo="text",
        name=f"Top {pct_str} Zone"
    ))

    # 3. Dynamic Boundary Polygon (Hülle um die gewählte Schwelle)
    if len(df_top) >= 3:
        a_norm = df_top["mastery"].values / total_budget
        c_norm = df_top["crit"].values / total_budget
        
        x_2d = 0.5 * (2 * c_norm + a_norm)
        y_2d = (np.sqrt(3) / 2) * a_norm
        pts = np.column_stack((x_2d, y_2d))
        
        try:
            from scipy.spatial import ConvexHull
            hull = ConvexHull(pts)
            hull_indices = list(hull.vertices) + [hull.vertices[0]]
            hull_df = df_top.iloc[hull_indices]

            fig.add_trace(go.Scatterternary(
                mode="lines",
                a=hull_df["mastery"],
                b=hull_df["haste"],
                c=hull_df["crit"],
                fill="toself",
                fillcolor="rgba(225, 90, 40, 0.18)",
                line=dict(color="#FF7F00", width=2, dash="dash"),
                name=f"Top {pct_str} Area",
                hoverinfo="skip"
            ))
        except ImportError:
            pass

    # 4. Highlight Peak Maximum
    fig.add_trace(go.Scatterternary(
        mode="markers+text",
        a=[top_sim["mastery"]],
        b=[top_sim["haste"]],
        c=[top_sim["crit"]],
        marker=dict(
            symbol="diamond",
            color="#FFF",
            size=16,
            line=dict(width=2.5, color="#000")
        ),
        text=[f"  <b>MAX: {top_sim['dps']:,.0f} DPS</b>"],
        textposition="top center",
        name="Absolute Top Sim",
        hoverinfo="text"
    ))

    axis_config = lambda name: dict(
        title=dict(text=f"<b>{name}</b>", font=dict(size=16, color="#FFFFFF")),
        min=0,
        linewidth=2,
        linecolor="#888888",
        gridwidth=1,
        gridcolor="rgba(150, 150, 150, 0.25)",
        ticks="outside",
        tickfont=dict(size=12, color="#DDDDDD")
    )

    # Fully dynamic Layout Title
    fig.update_layout(
        title=dict(
            text=f"Moonkin Stat Distribution (Top {pct_str} Zone Highlighted)<br><sup>Max DPS: {max_dps:,.0f} | Threshold (>= {100 - pct_val:.1f}% Max): {cutoff_dps:,.0f} DPS</sup>",
            x=0.5,
            y=0.97,
            font=dict(size=20)
        ),
        ternary=dict(
            sum=total_budget,
            aaxis=axis_config("MASTERY (Top)"),
            baxis=axis_config("HASTE (Left)"),
            caxis=axis_config("CRIT (Right)"),
            bgcolor="rgb(15, 15, 22)"
        ),
        template="plotly_dark",
        margin=dict(l=60, r=60, b=60, t=100)
    )

    output_html = "moonkin_ternary_stats.html"
    fig.write_html(output_html)
    print(f"Interactive ternary plot saved as: {output_html}")
    
    try:
        webbrowser.open("file://" + os.path.realpath(output_html))
    except Exception:
        pass

if __name__ == "__main__":
    df_results = parse_simc_json("results.json")
    
    # Hier kannst du beliebig anpassen (z. B. 0.02 für 2% oder 0.05 für 5%)
    create_ternary_stat_plot(df_results, threshold_percent=0.02)