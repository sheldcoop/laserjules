import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils import UM_TO_CM, UJ_TO_J

def render():
    # --- HEADER ---
    st.header("Microvia Process Simulator")
    st.info("Interactively simulate a laser drilling process or generate a starting recipe for a specific goal.")
    st.markdown("---")

    # --- MAIN TWO-COLUMN LAYOUT ---
    col1, col2 = st.columns([1, 2]) # Control Panel | Results Canvas

    # --- LEFT COLUMN: THE CONTROL PANEL ---
    with col1:
        st.subheader("Control Panel")
        
        # --- MODE SELECTION ---
        with st.container(border=True):
            st.markdown("<h6>Select Mode</h6>", unsafe_allow_html=True)
            calc_mode = st.radio(
                "Select Mode", 
                ["Interactive Simulator", "Recipe Goal Seeker"], 
                label_visibility="collapsed"
            )

        # --- INTERACTIVE SIMULATOR INPUTS ---
        if calc_mode == "Interactive Simulator":
            
            with st.container(border=True):
                st.markdown("<h6>Laser Parameters</h6>", unsafe_allow_html=True)
                beam_profile = st.selectbox("Beam Profile", ["Gaussian", "Top-Hat"])
                
                # --- NEW: Nested columns for compact layout ---
                param_col1, param_col2 = st.columns(2)
                with param_col1:
                    pe_slider = st.slider("Pulse Energy (µJ)", 0.1, 50.0, 10.0, 0.1)
                    pulse_energy_uJ = st.number_input("PE Value", value=pe_slider, min_value=0.1, max_value=50.0, step=0.01, label_visibility="collapsed")
                with param_col2:
                    bd_slider = st.slider("Beam Spot Diameter (µm)", 5.0, 50.0, 15.0, 0.5)
                    beam_diameter_um = st.number_input("BD Value", value=bd_slider, min_value=5.0, max_value=50.0, step=0.1, label_visibility="collapsed")

            with st.container(border=True):
                st.markdown("<h6>Material Properties</h6>", unsafe_allow_html=True)
                
                # --- NEW: Nested columns for compact layout ---
                mat_col1, mat_col2 = st.columns(2)
                with mat_col1:
                    at_slider = st.slider("Ablation Threshold (J/cm²)", 0.1, 10.0, 1.0, 0.1)
                    ablation_threshold_j_cm2 = st.number_input("AT Value", value=at_slider, min_value=0.1, max_value=10.0, step=0.01, label_visibility="collapsed")
                with mat_col2:
                    ai_slider = st.slider("Penetration Depth (α⁻¹) (µm)", 0.1, 5.0, 0.5, 0.05)
                    alpha_inv = st.number_input("AI Value", value=ai_slider, min_value=0.1, max_value=5.0, step=0.01, label_visibility="collapsed")

            with st.container(border=True):
                st.markdown("<h6>Process Goal</h6>", unsafe_allow_html=True)

                # --- NEW: Nested columns for compact layout ---
                goal_col1, goal_col2 = st.columns(2)
                with goal_col1:
                    ns_slider = st.slider("Number of Shots", 1, 300, 75)
                    number_of_shots = st.number_input("NS Value", value=ns_slider, min_value=1, max_value=300, step=1, label_visibility="collapsed")
                with goal_col2:
                    material_thickness = st.number_input("Material Thickness (µm)", 1.0, 200.0, 50.0)

        # --- RECIPE GOAL SEEKER INPUTS (Already compact, no changes needed) ---
        else: # Recipe Goal Seeker
            # ... (Your existing Goal Seeker code goes here)

    # --- RIGHT COLUMN: THE RESULTS CANVAS ---
    with col2:
        st.subheader("Results Canvas")
        
        # In a real implementation, you would perform the calculations here
        # For now, we can just show a placeholder
        if calc_mode == "Interactive Simulator":
            # --- (Your existing calculation and plotting logic goes here) ---
            st.markdown("<h6>Process Metrics</h6>", unsafe_allow_html=True)
            # ... st.metric for Fluence, Depth per Pulse
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<h6>Predicted Via Geometry</h6>", unsafe_allow_html=True)
            # ... st.metric for Diameters, Taper
            st.markdown("<hr>", unsafe_allow_html=True)
            # ... Plotly figures for Cause and Effect
        else:
            st.info("Your recommended recipe will appear here.")
