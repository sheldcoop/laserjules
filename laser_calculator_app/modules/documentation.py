import streamlit as st

def render():
    st.header("Scientific Reference & Documentation")
    st.markdown("---")
    
    st.info(
        "This guide provides a comprehensive overview of the scientific principles, formulas, and models "
        "used throughout the Laser Dashboard. Use this reference to understand the 'why' behind the calculations."
    )

    # --- CORE CONCEPTS SECTION ---
    with st.container(border=True):
        st.subheader("🔬 Core Scientific Concepts")
        
        st.markdown("#### 1. The Gaussian Beam")
        st.markdown(
            "Most laser beams do not have a uniform intensity. They follow a **Gaussian distribution**, meaning the energy is most intense at the very center and fades out towards the edges, just like the beam from a flashlight."
        )
        st.markdown(
            "The **Beam Spot Diameter (1/e²)** is the standard engineering definition for the 'size' of the beam. It's the diameter where the beam's intensity has dropped to approximately 13.5% of its peak value."
        )
        st.latex(r'''
        F(r) = F_0 \cdot e^{-2r^2 / w_0^2}
        ''')
        st.markdown(
            "- **F(r)**: Fluence at a radial distance *r* from the center."
            "\n- **$F_0$**: Peak Fluence at the center (r=0)."
            "\n- **$w_0$**: Beam Radius (half of the 1/e² diameter)."
        )

        st.markdown("#### 2. Fluence (Energy Density)")
        st.markdown(
            "Fluence is the single most important parameter in laser processing. It measures the amount of energy delivered per unit area, typically in **Joules per square centimeter (J/cm²)**. Think of it like the intensity of sunlight focused by a magnifying glass."
        )
        st.latex(r'''
        F_0 = \frac{2E}{\pi w_0^2}
        ''')
        st.markdown(
            "- **E**: Pulse Energy (in Joules)."
            "\n- The factor of **2** is specific to Gaussian beams and accounts for the total energy contained within the profile."
        )

        st.markdown("#### 3. The Ablation Process")
        st.markdown(
            "Ablation is the process of removing material by vaporizing it with laser energy. The model used in this application is based on two fundamental material properties that you must determine experimentally:"
        )
        st.markdown(
            "- **Ablation Threshold ($F_{th}$):** The minimum fluence required to cause *any* material removal. Below this value, the laser will heat the material, but not ablate it. Think of it as the minimum temperature needed to get a sunburn."
            "\n- **Effective Penetration Depth ($α^{-1}$):** A property that describes how deeply the laser energy is absorbed to cause ablation. A *small* value (e.g., 0.1 µm) means the energy is absorbed in a very shallow layer, leading to very precise, controlled removal. A *large* value means the energy soaks in deeper, leading to faster but potentially less controlled drilling."
        )

    # --- TOOL-SPECIFIC FORMULAS SECTION ---
    with st.container(border=True):
        st.subheader("⚙️ Tool-Specific Formulas & Logic")

        st.markdown("#### Material Analyzer")
        st.markdown(
            "**Purpose:** To determine your material's two fundamental properties ($F_{th}$ and $α^{-1}$) from experimental data. This is the critical first step in any process development."
            "\n\n**Logic:** The relationship between the ablation rate (depth per pulse) and the fluence is described by the **Beer-Lambert Law**, which is linear when plotted on a semi-logarithmic scale."
        )
        st.latex(r'''
        Z_{pulse} = \alpha^{-1} \cdot \ln\left(\frac{F_0}{F_{th}}\right)
        ''')
        st.markdown(
            "The tool rearranges this into the form of a straight line, `y = mx + c`, by plotting **Ablation Rate (y)** against **ln(Fluence) (x)**. It then performs a linear regression to find the best-fit line."
            "\n- The **slope (m)** of this line is your **Effective Penetration Depth ($α^{-1}$)**."
            "\n- The **x-intercept** of this line gives you the **Ablation Threshold ($F_{th}$)**."
        )
        
        st.markdown("---")
        
        st.markdown("#### Process Recommender")
        st.markdown(
            "**Purpose:** To work backward from a desired outcome (a specific via size) to find a recommended starting recipe (Pulse Energy and Number of Shots)."
            "\n\n**Logic:** It uses the same core formulas but solves them in reverse."
            "\n1. It first calculates the required **Peak Fluence ($F_0$)** needed to create your `Target Top Diameter`."
            "\n2. It then calculates the **Pulse Energy (E)** required to achieve that `Peak Fluence` with your given `Beam Spot Diameter`."
            "\n3. Finally, it calculates the **Depth per Pulse** at that energy and determines the `Number of Shots` needed to drill through the `Material Thickness` (plus any `Overkill Shots`)."
        )
        
        st.markdown("---")
        
        st.markdown("#### Microvia Process Simulator")
        st.markdown(
            "**Purpose:** To work forward from a known recipe (Pulse Energy, Beam Diameter, etc.) to predict the exact geometry of the final microvia."
            "\n\n**Logic:** This is the most comprehensive tool. It simulates the drilling process pulse by pulse."
            "\n1. It first calculates the **Peak Fluence ($F_0$)** from your inputs."
            "\n2. It then calculates the full **depth profile of a single pulse** using the Beer-Lambert formula at every radial position."
            "\n3. It calculates the **Total Accumulated Depth** by multiplying the single-pulse profile by the `Number of Shots`."
            "\n4. It 'clips' this total depth at the `Material Thickness` to create the final via shape."
            "\n5. From this final shape, it measures the **Top Diameter**, **Bottom Diameter**, and calculates the resulting **Wall Angle (Taper)** and **Taper Ratio**."
        )

    st.success("You have reached the end of the documentation. Use the sidebar to navigate to a tool and apply these concepts!")
