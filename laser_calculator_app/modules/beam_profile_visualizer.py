import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils import UM_TO_CM, UJ_TO_J
from fpdf import FPDF
import io
from datetime import datetime

# --- NEW: PDF Report Generation Function ---
def generate_pdf_report(inputs, metrics, fig_fluence, fig_via):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Title
    pdf.cell(0, 10, "Laser Microvia Process Simulation Report", 0, 1, "C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, "C")
    pdf.ln(10)

    # --- Inputs Section ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Input Parameters", 0, 1, "L")
    pdf.set_font("Arial", "", 10)
    
    col_width = pdf.w / 2.2
    for key, value in inputs.items():
        pdf.cell(col_width, 8, f"{key}:", border=1)
        pdf.cell(col_width, 8, str(value), border=1)
        pdf.ln()
    pdf.ln(5)

    # --- Metrics Section ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Predicted Results", 0, 1, "L")
    pdf.set_font("Arial", "", 10)

    for key, value in metrics.items():
        pdf.cell(col_width, 8, f"{key}:", border=1)
        pdf.cell(col_width, 8, str(value), border=1)
        pdf.ln()
    pdf.ln(10)

    # --- Plots Section ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Visualizations", 0, 1, "L")
    
    # Convert plotly figures to in-memory image files
    fluence_img_bytes = fig_fluence.to_image(format="png", width=600, height=400, scale=2)
    via_img_bytes = fig_via.to_image(format="png", width=600, height=400, scale=2)
    
    # Add images to PDF
    pdf.image(io.BytesIO(fluence_img_bytes), x=10, w=pdf.w/2 - 15)
    pdf.image(io.BytesIO(via_img_bytes), x=pdf.w/2 + 5, w=pdf.w/2 - 15)

    return pdf.output(dest='S').encode('latin-1')


def render():
    st.header("Microvia Process Simulator")
    st.markdown("---")

    # State management for mode switching
    if st.session_state.get("switch_to_simulator", False):
        st.session_state.simulator_mode = "Interactive Simulator"
        st.session_state.switch_to_simulator = False

    mode_options = ["Interactive Simulator", "Recipe Goal Seeker"]
    current_mode_index = mode_options.index(st.session_state.get("simulator_mode", "Interactive Simulator"))

    calc_mode = st.radio("Select Mode", options=mode_options, index=current_mode_index, key="simulator_mode", horizontal=True)

    # --- UI and Logic for the Simulator ---
    if calc_mode == "Interactive Simulator":
        params = st.session_state.get("sim_params", {})
        st.info("Adjust the sliders for quick exploration or type exact values for precision.")
        
        st.subheader(" Laser Parameters")
        # --- NEW: Beam Profile Selection ---
        beam_profile = st.selectbox("Beam Profile", ["Gaussian", "Top-Hat"], help="Select the energy distribution of the laser beam.")

        c1, c2 = st.columns([3, 1])
        with c1:
            pe_slider = st.slider("Pulse Energy (µJ)", 0.1, 50.0, params.get("pulse_energy", 10.0), 0.1)
        with c2:
            pulse_energy_uJ = st.number_input("Value", value=pe_slider, min_value=0.1, max_value=50.0, step=0.01, key="pe_num_sim", label_visibility="collapsed")
        
        c1, c2 = st.columns([3, 1])
        with c1:
            bd_slider = st.slider("Beam Spot Diameter (µm)", 5.0, 50.0, params.get("beam_diameter", 25.0), 0.5)
        with c2:
            beam_diameter_um = st.number_input("Value", value=bd_slider, min_value=5.0, max_value=50.0, step=0.1, key="bd_num_sim", label_visibility="collapsed")

        # ... (rest of the UI for Material Properties and Process Goal) ...
        st.subheader(" Material Properties")
        c1, c2 = st.columns([3, 1])
        with c1:
            at_slider = st.slider("Ablation Threshold (J/cm²)", 0.1, 10.0, params.get("ablation_threshold", 1.0), 0.1)
        with c2:
            ablation_threshold_j_cm2 = st.number_input("Value", value=at_slider, min_value=0.1, max_value=10.0, step=0.01, key="at_num_sim", label_visibility="collapsed")
        
        c1, c2 = st.columns([3, 1])
        with c1:
            ai_slider = st.slider("Penetration Depth (α⁻¹) (µm)", 0.1, 5.0, params.get("alpha_inv", 0.5), 0.05)
        with c2:
            alpha_inv = st.number_input("Value", value=ai_slider, min_value=0.1, max_value=5.0, step=0.01, key="ai_num_sim", label_visibility="collapsed")

        st.subheader("🎯 Process Goal")
        c1, c2 = st.columns([3, 1])
        with c1:
            ns_slider = st.slider("Number of Shots", 1, 300, params.get("number_of_shots", 75))
        with c2:
            number_of_shots = st.number_input("Value", value=ns_slider, min_value=1, max_value=300, step=1, key="ns_num_sim", label_visibility="collapsed")
        
        material_thickness = st.number_input("Material Thickness (µm)", 1.0, 200.0, params.get("material_thickness", 50.0), key="mt_num_sim")

    else: # Recipe Goal Seeker (simplified to Gaussian-only for clarity)
        st.info("Define your desired via and calculate a starting recipe for a GAUSSIAN beam.")
        beam_profile = "Gaussian" # Goal seeker is fixed to Gaussian
        # ... (Goal Seeker UI remains largely the same) ...
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("🎯 Desired Via")
            target_diameter_um = st.number_input("Target Top Diameter (µm)", 1.0, 100.0, 25.0, 0.1)
            material_thickness = st.number_input("Material Thickness (µm)", 1.0, 200.0, 40.0, 1.0)
            overkill_shots = st.number_input("Overkill Shots", 0, 100, 10, help="Extra shots to ensure a clean breakthrough and wider exit.")
        with col2:
            st.subheader("⚙️ Machine Constraints")
            beam_diameter_um = st.number_input("Beam Spot Diameter (µm)", 1.0, 100.0, 30.0, 0.5)
        with col3:
            st.subheader("🔬 Material Properties")
            ablation_threshold_j_cm2 = st.number_input("Ablation Threshold (J/cm²)", 0.01, 20.0, 0.9, 0.01)
            alpha_inv = st.number_input("Penetration Depth (α⁻¹) (µm)", 0.01, 10.0, 0.8, 0.01)

        w0_cm = (beam_diameter_um / 2.0) * UM_TO_CM
        d_cm = target_diameter_um * UM_TO_CM
        required_peak_fluence = ablation_threshold_j_cm2 * np.exp((d_cm**2) / (2 * w0_cm**2)) if w0_cm > 0 else 0
        required_energy_J = (required_peak_fluence * np.pi * w0_cm**2) / 2.0
        pulse_energy_uJ = required_energy_J / UJ_TO_J
        max_depth_per_pulse = alpha_inv * np.log(required_peak_fluence / ablation_threshold_j_cm2) if required_peak_fluence > ablation_threshold_j_cm2 else 0
        
        if max_depth_per_pulse > 0:
            min_shots = int(np.ceil(material_thickness / max_depth_per_pulse))
            number_of_shots = min_shots + overkill_shots
        else: number_of_shots = 0

        st.markdown("---")
        st.markdown(f'<p class="results-header" style="color: #007aff;">Recommended Recipe</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric(label="Required Pulse Energy", value=f"{pulse_energy_uJ:.3f} µJ")
        c2.metric(label="Required Number of Shots", value=f"{number_of_shots} shots")

        if st.button("➡️ Load this Recipe in the Interactive Simulator", use_container_width=True, type="primary"):
            st.session_state.sim_params = {"pulse_energy": pulse_energy_uJ, "beam_diameter": beam_diameter_um, "ablation_threshold": ablation_threshold_j_cm2, "alpha_inv": alpha_inv, "number_of_shots": number_of_shots, "material_thickness": material_thickness}
            st.session_state.switch_to_simulator = True
            st.rerun()

    # --- SHARED CALCULATION & VISUALIZATION LOGIC ---
    w0_um = beam_diameter_um / 2
    pulse_energy_j = pulse_energy_uJ * UJ_TO_J
    r_um = np.linspace(-beam_diameter_um * 1.5, beam_diameter_um * 1.5, 501)
    
    # --- NEW: Conditional physics based on beam profile ---
    if beam_profile == 'Gaussian':
        peak_fluence_j_cm2 = (2 * pulse_energy_j) / (np.pi * (w0_um * UM_TO_CM)**2) if w0_um > 0 else 0
        fluence_profile = peak_fluence_j_cm2 * np.exp(-2 * (r_um**2) / w0_um**2)
    else: # Top-Hat
        peak_fluence_j_cm2 = pulse_energy_j / (np.pi * (w0_um * UM_TO_CM)**2) if w0_um > 0 else 0
        fluence_profile = np.where(np.abs(r_um) <= w0_um, peak_fluence_j_cm2, 0)

    depth_profile_um = np.zeros_like(fluence_profile)
    ablation_mask = fluence_profile > ablation_threshold_j_cm2
    
    if np.any(ablation_mask):
        fluence_ratio = fluence_profile[ablation_mask] / ablation_threshold_j_cm2
        depth_profile_um[ablation_mask] = alpha_inv * np.log(fluence_ratio)
        if beam_profile == 'Gaussian':
            log_term = np.log(peak_fluence_j_cm2 / ablation_threshold_j_cm2)
            top_diameter_um = np.sqrt(2 * w0_um**2 * log_term) if log_term > 0 else 0
        else: # Top-Hat
            top_diameter_um = beam_diameter_um if peak_fluence_j_cm2 > ablation_threshold_j_cm2 else 0
    else: 
        top_diameter_um = 0
    
    max_depth_per_pulse = depth_profile_um.max()
    total_depth_profile = number_of_shots * depth_profile_um
    
    through_mask = total_depth_profile >= material_thickness
    if np.any(through_mask):
        exit_indices = np.where(through_mask)[0]
        bottom_diameter_um = r_um[exit_indices[-1]] - r_um[exit_indices[0]]
    else: 
        bottom_diameter_um = 0.0
    
    final_via_profile = np.clip(total_depth_profile, 0, material_thickness)

    if bottom_diameter_um > 0:
        radius_diff = (top_diameter_um - bottom_diameter_um) / 2.0
        taper_angle_deg = np.rad2deg(np.arctan(radius_diff / material_thickness))
        taper_ratio = radius_diff / material_thickness
    else:
        taper_angle_deg = 90.0
        taper_ratio = float('inf')

    # --- METRICS DISPLAY ---
    st.markdown("---")
    # ... (Metrics display code remains the same) ...
    st.subheader("Process Metrics")
    c1, c2 = st.columns(2)
    c1.metric("Peak Fluence", f"{peak_fluence_j_cm2:.2f} J/cm²")
    c2.metric("Depth per Pulse", f"{max_depth_per_pulse:.2f} µm")

    st.subheader("Predicted Via Geometry")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Top Diameter", f"{top_diameter_um:.2f} µm")
    c2.metric("Bottom Diameter", f"{bottom_diameter_um:.2f} µm", help="0 µm means it did not drill all the way through.")
    c3.metric("Wall Angle (Taper)", f"{taper_angle_deg:.2f}°", help="Angle from the vertical. Smaller is better.")
    c4.metric("Taper Ratio", f"{taper_ratio:.3f}", help="Ratio of radial change to depth (tan(θ)). Smaller is better.")


    # --- PLOTTING ---
    st.markdown("---")
    # ... (Plotting code remains the same, it will automatically update with the new profiles) ...
    plot1, plot2 = st.columns(2)

    with plot1:
        fig_fluence = go.Figure()
        fig_fluence.add_trace(go.Scatter(x=r_um, y=fluence_profile, mode='lines', line=dict(color='#ef4444', width=3)))
        fig_fluence.add_trace(go.Scatter(x=r_um, y=np.full_like(r_um, ablation_threshold_j_cm2), mode='lines', line=dict(color='grey', dash='dash')))
        if max_depth_per_pulse > 0:
            y_upper = np.maximum(fluence_profile, ablation_threshold_j_cm2)
            fig_fluence.add_trace(go.Scatter(x=r_um, y=y_upper, fill='tonexty', mode='none', fillcolor='rgba(46, 204, 113, 0.2)'))
        fig_fluence.add_vline(x=top_diameter_um/2, line_dash="dot", opacity=0.5, line_color="#ef4444", annotation_text="Top Radius")
        fig_fluence.add_vline(x=-top_diameter_um/2, line_dash="dot", opacity=0.5, line_color="#ef4444")
        fig_fluence.update_layout(title="<b>Cause:</b> Applied Fluence Profile", xaxis_title="Radial Position (µm)", yaxis_title="Fluence (J/cm²)", yaxis_range=[0, max(peak_fluence_j_cm2 * 1.1, 1.0)], showlegend=False, margin=dict(t=50))
        st.plotly_chart(fig_fluence, use_container_width=True)

    with plot2:
        fig_via = go.Figure()
        material_poly_x = np.concatenate([r_um, r_um[::-1]])
        material_poly_y = np.concatenate([-np.full_like(r_um, material_thickness), -final_via_profile[::-1]])
        fig_via.add_trace(go.Scatter(x=material_poly_x, y=material_poly_y, fill='toself', mode='lines', line_color='#3498db', fillcolor='rgba(220, 220, 220, 0.7)', name='Material'))
        fig_via.add_trace(go.Scatter(x=r_um, y=-final_via_profile, mode='lines', line=dict(color='#3498db', width=3)))
        
        status_text = "SUCCESS" if bottom_diameter_um > 0 else "INCOMPLETE"
        status_color = "green" if bottom_diameter_um > 0 else "red"
        fig_via.add_annotation(x=0, y=-material_thickness/2, text=status_text, showarrow=False, font=dict(color=status_color, size=16), bgcolor="rgba(255,255,255,0.7)")

        fig_via.add_shape(type="line", x0=-top_diameter_um/2, y0=material_thickness*0.1, x1=top_diameter_um/2, y1=material_thickness*0.1, line=dict(color="black", width=1))
        fig_via.add_annotation(x=0, y=material_thickness*0.15, text=f"Top: {top_diameter_um:.2f} µm", showarrow=False, yanchor="bottom", font=dict(size=10))
        if bottom_diameter_um > 0:
            fig_via.add_shape(type="line", x0=-bottom_diameter_um/2, y0=-material_thickness*1.1, x1=bottom_diameter_um/2, y1=-material_thickness*1.1, line=dict(color="black", width=1))
            fig_via.add_annotation(x=0, y=-material_thickness*1.15, text=f"Bottom: {bottom_diameter_um:.2f} µm", showarrow=False, yanchor="top", font=dict(size=10))
        
        fig_via.update_layout(title="<b>Effect:</b> Predicted Microvia Cross-Section", xaxis_title="Radial Position (µm)", yaxis_title="Depth (µm)", yaxis_range=[-material_thickness * 1.5, material_thickness * 0.5], showlegend=False, margin=dict(t=50))
        st.plotly_chart(fig_via, use_container_width=True)


    # --- FINAL: 3D Visualization and PDF Report Download ---
    with st.expander("Show Interactive 3D Via Visualization"):
        # ... (3D plot code remains the same) ...
        if max_depth_per_pulse > 0:
            x_3d = np.linspace(r_um.min(), r_um.max(), 100)
            y_3d = np.linspace(r_um.min(), r_um.max(), 100)
            X, Y = np.meshgrid(x_3d, y_3d)
            R_sq = X**2 + Y**2
            
            if beam_profile == 'Gaussian':
                fluence_3d = peak_fluence_j_cm2 * np.exp(-2 * R_sq / w0_um**2)
            else: # Top-Hat
                fluence_3d = np.where(R_sq <= w0_um**2, peak_fluence_j_cm2, 0)

            depth_3d = np.zeros_like(fluence_3d)
            ablation_mask_3d = fluence_3d > ablation_threshold_j_cm2
            
            if np.any(ablation_mask_3d):
                fluence_ratio_3d = fluence_3d[ablation_mask_3d] / ablation_threshold_j_cm2
                depth_3d[ablation_mask_3d] = alpha_inv * np.log(fluence_ratio_3d)

            total_depth_3d = number_of_shots * depth_3d
            final_via_3d = np.clip(total_depth_3d, 0, material_thickness)
            z_surface = -final_via_3d

            fig3d = go.Figure(data=[go.Surface(z=z_surface, x=X, y=Y, colorscale='Cividis', showscale=False, lighting=dict(ambient=0.6, diffuse=1.0, specular=0.2, roughness=0.5), lightposition=dict(x=100, y=200, z=50))])
            fig3d.update_layout(title='3D View of Via in Material', scene=dict(xaxis_title='X (µm)', yaxis_title='Y (µm)', zaxis_title='Depth (µm)', aspectratio=dict(x=1, y=1, z=0.4), camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))), margin=dict(l=10, r=10, b=10, t=40))
            st.plotly_chart(fig3d, use_container_width=True)
        else:
            st.warning("No ablation occurs with the current settings. Cannot render 3D view.")
    
    st.markdown("---")
    
    # --- NEW: PDF Download Button and Logic ---
    st.subheader("Download Simulation Report")
    
    # Prepare data dictionaries for the report
    input_data = {
        "Beam Profile": beam_profile,
        "Pulse Energy (µJ)": f"{pulse_energy_uJ:.3f}",
        "Beam Diameter (µm)": f"{beam_diameter_um:.2f}",
        "Ablation Threshold (J/cm²)": f"{ablation_threshold_j_cm2:.3f}",
        "Penetration Depth (µm)": f"{alpha_inv:.3f}",
        "Number of Shots": str(number_of_shots),
        "Material Thickness (µm)": f"{material_thickness:.2f}"
    }

    metric_data = {
        "Peak Fluence (J/cm²)": f"{peak_fluence_j_cm2:.2f}",
        "Depth per Pulse (µm)": f"{max_depth_per_pulse:.2f}",
        "Top Diameter (µm)": f"{top_diameter_um:.2f}",
        "Bottom Diameter (µm)": f"{bottom_diameter_um:.2f}",
        "Wall Angle (Taper) (°)": f"{taper_angle_deg:.2f}",
        "Taper Ratio": f"{taper_ratio:.3f}"
    }
    
    # Generate PDF in memory
    pdf_data = generate_pdf_report(input_data, metric_data, fig_fluence, fig_via)
    
    st.download_button(
        label="📄 Download Report as PDF",
        data=pdf_data,
        file_name=f"laser_via_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )