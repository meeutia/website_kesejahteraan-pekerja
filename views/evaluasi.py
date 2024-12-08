import streamlit as st
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

st.title("Evaluasi Model")

if 'trained_models' in st.session_state and 'resultNational' in st.session_state:
    # Ambil model dan data
    trained_models = st.session_state['trained_models']  # Dictionary {target_name: model}
    resultNational = st.session_state['resultNational']

    # Siapkan data untuk evaluasi
    X = resultNational[['Tahun']]
    y_vars = {
        'Garis Kemiskinan': resultNational['Garis Kemiskinan'],
        'Upah Minimum Provinsi': resultNational['Upah Minimum Provinsi'],
        'Pengeluaran per bulan': resultNational['Pengeluaran per bulan'],
        'Rata-rata Gaji per bulan': resultNational['Rata-rata Gaji per bulan']
    }

    # Layout evaluasi
    col1, col2, col3, col4 = st.columns(4)
    columns = [col1, col2, col3, col4]

    # Evaluasi tiap target variabel
    for (target_name, y), col in zip(y_vars.items(), columns):
        if target_name in trained_models:
            model = trained_models[target_name]
            predictions = model.predict(X)

            # Hitung metrik evaluasi
            rmse = np.sqrt(mean_squared_error(y, predictions))
            r2 = r2_score(y, predictions)

            # Tampilkan hasil
            with col:
                st.write(f"**{target_name}**")
                st.write(f"RMSE: {rmse:.5f}")
                st.write(f"R²: {r2:.5f}")
        else:
            with col:
                st.warning(f"Model untuk {target_name} tidak ditemukan.")
else:
    st.warning("Model atau data belum tersedia. Silakan pastikan model telah dilatih dan data tersedia di session_state.")
