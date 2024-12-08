import streamlit as st
import pandas as pd

st.title("Kesejahteraan")

st.subheader("Upload File")

if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = {}

def delete_file(file_name):
    if file_name in st.session_state['uploaded_files']:
        del st.session_state['uploaded_files'][file_name]
        st.success(f"File '{file_name}' berhasil dihapus.")

if st.session_state['uploaded_files']:
    st.write("File yang sudah diunggah:")
    for file_name in list(st.session_state['uploaded_files'].keys()):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"✅ {file_name}")
        with col2:
            if st.button("Hapus", key=f"delete_{file_name}"):
                delete_file(file_name)
else:
    st.info("Belum ada file yang diunggah.")

uploaded_files = st.file_uploader(
    "Tambahkan file baru:",
    accept_multiple_files=True,
    key="new_upload"
)

if uploaded_files:
    for file in uploaded_files:
        if file.name in st.session_state['uploaded_files']:
            st.warning(f"File '{file.name}' sudah ada.")
        else:
            st.session_state['uploaded_files'][file.name] = pd.read_csv(file)
            st.success(f"File '{file.name}' berhasil ditambahkan.")

if len(st.session_state['uploaded_files']) == 4:
    st.success("Sudah cukup 4 file yang diunggah. Siap untuk preprocessing.")
else:
    st.warning(f"Saat ini ada {len(st.session_state['uploaded_files'])} file. Harap unggah tepat 4 file.")

if st.button("✉️ Preprocessing"):
    if len(st.session_state['uploaded_files']) == 4:
        st.success("Navigasi ke halaman Preprocessing.")

        pg = st.navigation([st.Page("views/preprocessing.py")])
    else:
        st.error("Harap unggah tepat 4 file sebelum melanjutkan.")
