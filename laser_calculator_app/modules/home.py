import streamlit as st

def render():
    # ... (Your TOOL_INFO dictionary here) ...

    st.title("Welcome to the Advanced Laser Process Calculator")
    st.markdown(...) # Your markdown introduction

    st.header("Recommended Workflow")
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        # --- KEY CHANGE: Add the CSS class via st.container ---
        with st.container():
            st.markdown('<div class="home-card">...</div>', unsafe_allow_html=True) # This is a placeholder for the content
            # ... (Your content for Step 1: st.markdown, st.button, etc.)
    # ... (Repeat for col2 and col3)

    st.header("Direct Tool Access & Resources")
    colA, colB, colC = st.columns(3, gap="large")
    with colA:
        with st.container():
            st.markdown('<div class="home-card">...</div>', unsafe_allow_html=True)
            # ... (Your content for Advanced Analysis)
    # ... (Repeat for colB and colC)

    # ... (Your dialog/pop-up logic can remain here if you still use it)
