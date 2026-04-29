import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Pile Reaction Calculator (Bakhoum 1992)", layout="wide")

st.title("Pile Reaction Calculator by Bakhoum (1992)")
st.markdown("### Unit System: ton, cm")

# ----------------------------
# INPUT
# ----------------------------
Q = st.number_input("Applied Vertical Load Q (ton)", value=100.0)

n = st.number_input("Number of Piles", min_value=1, step=1, value=4)

st.markdown("## Enter Pile Coordinates (cm)")

pile_data = []

for i in range(n):
    col1, col2 = st.columns(2)

    with col1:
        x = st.number_input(f"Pile {i+1} X-coordinate (cm)", key=f"x{i}")

    with col2:
        y = st.number_input(f"Pile {i+1} Y-coordinate (cm)", key=f"y{i}")

    pile_data.append([i+1, x, y])

pile_df = pd.DataFrame(pile_data, columns=["Pile", "x", "y"])

# ----------------------------
# CALCULATION
# ----------------------------
if st.button("Calculate"):

    x = pile_df["x"].values
    y = pile_df["y"].values

    # New Centroid
    x_bar = np.mean(x)
    y_bar = np.mean(y)

    # Relative Coordinates
    x_rel = x - x_bar
    y_rel = y - y_bar

    sum_x2 = np.sum(x_rel**2)
    sum_y2 = np.sum(y_rel**2)

    # Assume Column Load at Origin (0,0)
    ex = x_bar
    ey = y_bar

    Mx = Q * ey      # ton-cm
    My = Q * ex      # ton-cm

    reactions = []

    for i in range(n):

        Ri = Q / n

        if sum_y2 != 0:
            Ri += Mx * y_rel[i] / sum_y2

        if sum_x2 != 0:
            Ri += My * x_rel[i] / sum_x2

        reactions.append(Ri)

    pile_df["Reaction (ton)"] = reactions

    # ----------------------------
    # OUTPUT
    # ----------------------------
    st.success("Calculation Completed")

    st.markdown("## New Centroid")
    st.metric("X̄", f"{x_bar:.2f} cm")
    st.metric("Ȳ", f"{y_bar:.2f} cm")

    st.markdown("## Pile Reactions")
    st.dataframe(pile_df, use_container_width=True)

    st.metric("Maximum Reaction", f"{max(reactions):.2f} ton")
    st.metric("Minimum Reaction", f"{min(reactions):.2f} ton")

    st.markdown("## Summary")
    st.write(f"Eccentricity ex = {ex:.2f} cm")
    st.write(f"Eccentricity ey = {ey:.2f} cm")
    st.write(f"Mx = {Mx:.2f} ton-cm")
    st.write(f"My = {My:.2f} ton-cm")
