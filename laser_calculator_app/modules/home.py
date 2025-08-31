import streamlit as st
import requests
from streamlit_lottie import st_lottie

def load_lottie_from_url(url: str):
    """Helper function to load a Lottie animation from a URL."""
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading Lottie animation: {e}")
        return None

def render():
    """Renders the new, redesigned home page."""

    # --- PAGE LAYOUT ---
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        # --- LOTTIE ANIMATION ---
        lottie_url = "https://lottie.host/8f93e626-c603-4252-a521-392a3442d885/hVd5nAn4qE.json"
        lottie_json = load_lottie_from_url(lottie_url)

        if lottie_json:
            st_lottie(
                lottie_json,
                speed=1,
                reverse=False,
                loop=True,
                quality="high",
                height=300,
                width=300,
                key="lottie_animation",
            )

    with col2:
        # --- WELCOME MESSAGE ---
        st.title("Advanced Laser Process Dashboard")
        st.markdown(
            """
            Welcome to your integrated suite of tools for laser micro-machining.
            Whether you're developing a new process, analyzing material properties, or simulating outcomes,
            this dashboard provides the calculators you need to achieve precision and efficiency.
            """
        )
        st.markdown("---")

        st.subheader("How to Get Started")
        st.info(
            "Use the navigation menu on the left to select a tool. The tools are organized by category "
            "to help you follow a logical workflow, from material analysis to process simulation."
        )

        # --- CALL TO ACTION ---
        if st.button("Explore the Core Workflow", type="primary", use_container_width=True):
            # This button doesn't need to change the page itself, as the user can use the sidebar.
            # It serves as a visual prompt. We can add a little confirmation message.
            st.toast("Great! Select a tool from the 'Core Workflow' section in the sidebar.", icon="👍")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # --- Optional: A brief overview of tool categories ---
    st.header("Tool Categories")
    cat1, cat2, cat3 = st.columns(3)
    
    with cat1:
        with st.container(border=True):
            st.markdown("##### 🔬 Core Workflow")
            st.markdown("Tools for process development, from material characterization to recipe generation.")

    with cat2:
        with st.container(border=True):
            st.markdown("##### 📈 Advanced Analysis")
            st.markdown("In-depth analysis tools for damage threshold testing and thermal modeling.")

    with cat3:
        with st.container(border=True):
            st.markdown("##### ⚡ Fundamental Calculators")
            st.markdown("Quick calculators for essential parameters like pulse energy and fluence.")
