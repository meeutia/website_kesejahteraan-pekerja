import streamlit as st


# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("assets/kesejahteraan1.png", width=230)

with col2:
    st.title("Selamat Datang,", anchor=False)
    st.write(
        "Website ini dirancang untuk memberikan visualisasi dan prediksi mendalam tentang indikator kesejahteraan di Indonesia."
    )
    st.write(
        "sumber dataset:(https://www.kaggle.com/datasets/rezkyyayang/pekerja-sejahtera)"
    )
    if st.button("✉️ Mulai"):
        pg = st.navigation([st.Page("views/start.py")])


# --- EXPERIENCE & QUALIFICATIONS ---
st.write("\n")
st.subheader("Anggota kelompok", anchor=False)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Meutia", "👩")
col2.metric("Zhafira", "👩")
col3.metric("Hilmi", "👨")
col4.metric("Zaki", "👨")