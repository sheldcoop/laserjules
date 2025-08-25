import streamlit as st
import pandas as pd
from utils import KHZ_TO_HZ, UM_TO_CM

def render():
    st.header("Analyze Heat Accumulation Risk")
    st.markdown("---")
    st.info("Estimate the risk of heat build-up by comparing the time between pulses to the time it takes for heat to diffuse away from the processed zone.")
    
    col1, col2 = st.columns(2)
    with col1:
        rep_rate_khz = st.number_input("Repetition Rate (kHz)", min_value=1.0, value=100.0, step=10.0)
        beam_diameter_um = st.number_input("Beam Spot Diameter (1/e²) (µm)", min_value=1.0, value=25.0, step=1.0)
        thermal_diffusivity_cm2_s = st.number_input("Material Thermal Diffusivity (D) (cm²/s)", 
                                                     min_value=1e-5, value=0.0014, step=1e-4, format="%.4f",
                                                     help="How quickly heat propagates through a material.")
    with col2:
        with st.expander("Typical Thermal Diffusivity Values (D)"):
            st.table(pd.DataFrame({
                "Material": ["Kapton (Polyimide)", "Silicon (Si)", "Copper (Cu)", "Stainless Steel", "Fused Silica (Glass)"],
                "D (cm²/s)": ["0.0014", "0.9", "1.11", "0.04", "0.0085"]
            }))

    rep_rate_hz = rep_rate_khz * KHZ_TO_HZ
    delta_t_s = 1 / rep_rate_hz
    w0_cm = (beam_diameter_um / 2) * UM_TO_CM
    tau_d_s = (w0_cm**2) / (4 * thermal_diffusivity_cm2_s) if thermal_diffusivity_cm2_s > 0 else 0
    heat_index = tau_d_s / delta_t_s if delta_t_s > 0 else float('inf')

    st.markdown("---")
    st.markdown(f'<p class="results-header">Thermal Analysis</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Time Between Pulses (Δt)", f"{delta_t_s * 1e6:.1f} µs")
    c2.metric("Thermal Diffusion Time (τ_d)", f"{tau_d_s * 1e6:.1f} µs")
    c3.metric("Heat Accumulation Index (τ_d/Δt)", f"{heat_index:.3f}")

    if heat_index < 0.1:
        st.success("✅ **Low Risk:** Heat dissipates much faster than pulses arrive. The process is likely in the single-pulse ablation regime.")
    elif 0.1 <= heat_index < 1.0:
        st.warning("⚠️ **Moderate Risk:** Heat accumulation may begin to influence the process. Material properties can change, potentially affecting ablation quality.")
    else:
        st.error("🚨 **High Risk:** Heat builds up significantly between pulses. This can lead to charring, melting, and a transition to a thermal-dominated process, reducing precision.")