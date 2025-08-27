import streamlit as st

def render():
    st.markdown("### 🔬 The Science & Formulas Behind the Simulation")
    st.markdown("---")
    
    st.subheader("Core Principles")
    st.markdown("""
    This simulator models how multiple Gaussian laser pulses drill a microvia based on established physical models.
    1.  **Single-Pulse Crater:** The shape of the hole from one pulse is first calculated using a logarithmic model based on the beam's fluence profile and the material's properties.
    2.  **Linear Accumulation:** The total depth is estimated by multiplying the single-pulse crater depth by the number of shots.
    3.  **Via Formation:** The final via shape is the result of this accumulated depth being "clipped" by the material's thickness.
    """)

    st.subheader("Key Parameter Formulas")

    st.markdown(r"**1. Peak Fluence ($F_0$)**")
    st.markdown(r"This formula is for a **Gaussian** beam. For a Top-Hat, $F_0 = E / (\pi w_0^2)$.")
    st.markdown(r"$$ F_0 = \frac{2E}{\pi w_0^2} $$")
    st.markdown(r"- **E**: Pulse Energy (Joules), **$w_0$**: Beam Radius (cm)")

    st.markdown(r"**2. Top Diameter ($D_{top}$)**")
    st.markdown(r"For a Top-Hat beam, the top diameter is simply equal to the beam diameter if $F_0 > F_{th}$.")
    st.markdown(r"$$ D_{top}^2 = 2w_0^2 \ln\left(\frac{F_0}{F_{th}}\right) $$")
    st.markdown(r"- **$F_{th}$**: Ablation Threshold (J/cm²)")

    st.markdown(r"**3. Depth per Pulse ($Z_{max}$)**")
    st.markdown(r"$$ Z_{max} = \alpha^{-1} \ln\left(\frac{F_0}{F_{th}}\right) $$")
    st.markdown(r"- **$\alpha^{-1}$**: Effective Penetration Depth (µm)")

    st.markdown(r"**4. Wall Angle (Taper) ($\theta$)**")
    st.markdown(r"$$ \theta = \arctan\left(\frac{D_{top} - D_{bottom}}{2H}\right) $$")
    st.markdown(r"- **H**: Material Thickness (µm)")

    st.markdown(r"**5. Taper Ratio**")
    st.markdown(r"""
    A unitless measure of the wall's steepness, equal to the tangent of the taper angle.
    $$ \text{Taper Ratio} = \frac{D_{top} - D_{bottom}}{2H} $$
    """)