import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Pile Group Centroid & Reaction", layout="wide")

st.title("Pile Group Design - Bakhoum (1992)")
st.subheader("Centroid Shift and Pile Reactions")

# -------------------------
# INPUT
# -------------------------
P = st.number_input("Axial Load P (kN)", value=1000.0)

n_piles = st.number_input("Number of Piles", min_value=1, step=1, value=4)

st.markdown("## Input Pile Coordinates")

pile_data = []

for i in range(n_piles):
    col1, col2 = st.columns(2)

    with col1:
        x = st.number_input(f"Pile {i+1} X (m)", key=f"x{i}")

    with col2:
        y = st.number_input(f"Pile {i+1} Y (m)", key=f"y{i}")

    pile_data.append([i+1, x, y])

pile_df = pd.DataFrame(pile_data, columns=["Pile", "x", "y"])

# -------------------------
# CALCULATION
# -------------------------
if st.button("Calculate"):

    x = pile_df["x"].values
    y = pile_df["y"].values

    # New Centroid
    x_bar = np.mean(x)
    y_bar = np.mean(y)

    # Shift Coordinates to New Centroid
    x_rel = x - x_bar
    y_rel = y - y_bar

    # Moments of Inertia
    Ix = np.sum(y_rel**2)
    Iy = np.sum(x_rel**2)

    # Assume load applied at original origin (0,0)
    ex = x_bar
    ey = y_bar

    Mx = P * ey
    My = P * ex

    reactions = []

    for i in range(n_piles):
        Ri = (P / n_piles)

        if Ix != 0:
            Ri += (Mx * y_rel[i] / Ix)

        if Iy != 0:
            Ri += (My * x_rel[i] / Iy)

        reactions.append(Ri)

    pile_df["Reaction (kN)"] = reactions

    # -------------------------
    # OUTPUT
    # -------------------------
    st.success("Calculation Completed")

    st.markdown("## New Centroid of Pile Group")
    st.metric("X̄ (m)", f"{x_bar:.3f}")
    st.metric("Ȳ (m)", f"{y_bar:.3f}")

    st.markdown("## Pile Reactions")
    st.dataframe(pile_df)

    st.metric("Maximum Reaction", f"{max(reactions):.2f} kN")
    st.metric("Minimum Reaction", f"{min(reactions):.2f} kN")
