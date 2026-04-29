import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Pile Reaction Calculator (Bakhoum 1992)", layout="wide")

st.title("Pile Foundation Moment Design - Bakhoum (1992)")
st.subheader("Pile Reaction for Eccentric Loading")

# -----------------------------
# INPUT SECTION
# -----------------------------
P = st.number_input("Axial Load P (kN)", value=1000.0)

n_piles = st.number_input("Number of Piles", min_value=1, step=1, value=4)

st.markdown("### Input Pile Coordinates")

pile_data = []

cols = st.columns(2)

for i in range(n_piles):
    with cols[i % 2]:
        x = st.number_input(f"Pile {i+1} - x (m)", key=f"x{i}")
        y = st.number_input(f"Pile {i+1} - y (m)", key=f"y{i}")
        pile_data.append([i+1, x, y])

pile_df = pd.DataFrame(pile_data, columns=["Pile", "x", "y"])

st.markdown("### Input New Load Application Point")
x0 = st.number_input("New Centroid X0 (m)", value=0.0)
y0 = st.number_input("New Centroid Y0 (m)", value=0.0)

# -----------------------------
# CALCULATION
# -----------------------------
if st.button("Calculate"):

    x = pile_df["x"].values
    y = pile_df["y"].values

    x_bar = np.mean(x)
    y_bar = np.mean(y)

    ex = x0 - x_bar
    ey = y0 - y_bar

    Mx = P * ey
    My = P * ex

    Ix = np.sum(y**2)
    Iy = np.sum(x**2)

    reactions = []

    for i in range(n_piles):
        Ri = (P / n_piles) + (Mx * y[i] / Ix) + (My * x[i] / Iy)
        reactions.append(Ri)

    pile_df["Reaction (kN)"] = reactions

    qmax = max(reactions)
    qmin = min(reactions)

    # -----------------------------
    # OUTPUT
    # -----------------------------
    st.success("Calculation Complete")

    st.markdown("## Results")
    st.dataframe(pile_df)

    st.metric("Maximum Reaction qmax (kN)", f"{qmax:.2f}")
    st.metric("Minimum Reaction qmin (kN)", f"{qmin:.2f}")

    # Engineering Summary
    st.markdown("## Calculation Summary")
    st.write(f"Pile Group Centroid = ({x_bar:.3f}, {y_bar:.3f}) m")
    st.write(f"Eccentricity ex = {ex:.3f} m")
    st.write(f"Eccentricity ey = {ey:.3f} m")
    st.write(f"Mx = {Mx:.2f} kN-m")
    st.write(f"My = {My:.2f} kN-m")
