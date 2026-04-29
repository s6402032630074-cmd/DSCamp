import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Pile Reaction Calculator (Bakhoum 1992)", layout="wide")

st.title("Pile Reaction Calculator by Bakhoum (1992)")
st.markdown("### Unit: ton, cm")

Q = st.number_input("Applied Vertical Load Q (ton)", value=100.0)
n = st.number_input("Number of Piles", min_value=1, step=1, value=4)

st.markdown("## Enter Pile Coordinates (cm)")

pile_data = []

for i in range(n):
    col1, col2 = st.columns(2)

    with col1:
        x = st.number_input(f"Pile {i+1} X (cm)", key=f"x{i}")

    with col2:
        y = st.number_input(f"Pile {i+1} Y (cm)", key=f"y{i}")

    pile_data.append([i+1, x, y])

pile_df = pd.DataFrame(pile_data, columns=["Pile", "x", "y"])

if st.button("Calculate"):

    x = pile_df["x"].values
    y = pile_df["y"].values

    x_bar = np.mean(x)
    y_bar = np.mean(y)

    x_rel = x - x_bar
    y_rel = y - y_bar

    sum_x2 = np.sum(x_rel**2)
    sum_y2 = np.sum(y_rel**2)

    ex = x_bar
    ey = y_bar

    Mx = Q * ey
    My = Q * ex

    uniform_load = Q / n

    reactions = []
    mx_loads = []
    my_loads = []

    for i in range(n):

        add_mx = Mx * y_rel[i] / sum_y2 if sum_y2 != 0 else 0
        add_my = My * x_rel[i] / sum_x2 if sum_x2 != 0 else 0

        Ri = uniform_load + add_mx + add_my

        mx_loads.append(add_mx)
        my_loads.append(add_my)
        reactions.append(Ri)

    pile_df["Uniform Load (ton)"] = uniform_load
    pile_df["Load from Mx (ton)"] = mx_loads
    pile_df["Load from My (ton)"] = my_loads
    pile_df["Total Pile Reaction (ton)"] = reactions

    st.success("Calculation Completed")

    st.markdown("## New Centroid")
    st.metric("X̄", f"{x_bar:.2f} cm")
    st.metric("Ȳ", f"{y_bar:.2f} cm")

    st.markdown("## Load Acting on Each Pile")
    st.dataframe(pile_df, use_container_width=True)

    st.metric("Maximum Load", f"{max(reactions):.2f} ton")
    st.metric("Minimum Load", f"{min(reactions):.2f} ton")
