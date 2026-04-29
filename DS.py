import streamlit as st
import math

st.set_page_config(page_title="Shallow Foundation Bearing Capacity", layout="centered")

st.title("Shallow Foundation Bearing Capacity Calculator")
st.subheader("Terzaghi Bearing Capacity Equation")

st.markdown("### Input Parameters")

B = st.number_input("Footing Width, B (m)", min_value=0.01, value=1.0)
L = st.number_input("Footing Length, L (m)", min_value=0.01, value=1.0)
D = st.number_input("Foundation Depth, D (m)", min_value=0.0, value=1.0)

c = st.number_input("Cohesion, c (kPa)", min_value=0.0, value=25.0)
phi = st.number_input("Friction Angle, φ (degrees)", min_value=0.0, max_value=60.0, value=30.0)
gamma = st.number_input("Unit Weight, γ (kN/m³)", min_value=0.0, value=18.0)

FS = st.number_input("Factor of Safety, FS", min_value=1.0, value=3.0)

if st.button("Calculate"):

    phi_rad = math.radians(phi)

    if phi == 0:
        Nc = 5.7
        Nq = 1.0
        Ngamma = 0.0
    else:
        Nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.radians(45) + phi_rad / 2))**2
        Nc = (Nq - 1) / math.tan(phi_rad)
        Ngamma = 1.5 * (Nq - 1) * math.tan(phi_rad)

    # Shape factors for rectangular footing
    sc = 1 + 0.3 * (B / L)
    sq = 1.0
    sgamma = 1 - 0.2 * (B / L)

    # Surcharge
    q = gamma * D

    # Terzaghi Bearing Capacity Equation
    qu = c * Nc * sc + q * Nq * sq + 0.5 * gamma * B * Ngamma * sgamma

    qall = qu / FS
    qnet = qall - q

    st.markdown("## Results")
    st.success(f"Ultimate Bearing Capacity, qu = {qu:.2f} kPa")
    st.success(f"Allowable Bearing Capacity, qall = {qall:.2f} kPa")
    st.success(f"Net Allowable Bearing Capacity, qnet = {qnet:.2f} kPa")
