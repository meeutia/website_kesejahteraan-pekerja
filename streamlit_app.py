import streamlit as st


# --- PAGE SETUP ---
about_page = st.Page(
    "views/about_me.py",
    title="About Us",
    icon=":material/account_circle:",
    default=True,
)

project_3_page = st.Page(
    "views/start.py",
    title="Mulai",
    icon=":material/upload:",
)

project_4_page = st.Page(
    "views/preprocessing.py",
    title="Preprocesing",
    icon=":material/smart_toy:",
)

project_5_page = st.Page(
    "views/visualisasi.py",
    title="Visualisasi",
    icon=":material/monitor:",
)

project_6_page = st.Page(
    "views/predict.py",
    title="Prediksi",
    icon=":material/train:",
)

project_7_page = st.Page(
    "views/evaluasi.py",
    title="Evaluasi",
    icon=":material/bar_chart:",
)


# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [about_page],
        "Projects": [project_3_page, project_4_page, project_5_page, project_6_page, project_7_page],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo("assets/logo.png")
st.sidebar.markdown("Made by us")


# --- RUN NAVIGATION ---
pg.run()
