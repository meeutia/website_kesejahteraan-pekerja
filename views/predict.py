import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

if 'result' in st.session_state:
    result = st.session_state['result']

    # Bersihkan nama kolom dari spasi
    result.columns = result.columns.str.strip()

    # Filter data untuk Nasional
    resultNational = result[result['Provinsi'] == 'INDONESIA']

    # Periksa apakah kolom yang dibutuhkan ada
    required_columns = ['Garis Kemiskinan', 'Upah Minimum Provinsi', 'Pengeluaran per bulan', 'Rata-rata Gaji per bulan']
    missing_columns = [col for col in required_columns if col not in resultNational.columns]

    if missing_columns:
        st.error(f"Kolom berikut hilang dari dataset: {', '.join(missing_columns)}")
    else:
        # Pisahkan fitur dan target untuk setiap variabel
        X = resultNational[['Tahun']]
        y_vars = {
            'Garis Kemiskinan': resultNational['Garis Kemiskinan'],
            'Upah Minimum Provinsi': resultNational['Upah Minimum Provinsi'],
            'Pengeluaran per bulan': resultNational['Pengeluaran per bulan'],
            'Rata-rata Gaji per bulan': resultNational['Rata-rata Gaji per bulan']
        }

        # Tempat menyimpan prediksi untuk tahun mendatang
        future_years = pd.DataFrame({'Tahun': range(2023, 2033)})
        predictions = pd.DataFrame({'Tahun': future_years['Tahun']})
        trained_models = {}

        # Latih model untuk setiap target variabel
        for target_name, y in y_vars.items():
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LinearRegression()
            model.fit(X_train, y_train)
            trained_models[target_name] = model
            predictions[target_name] = model.predict(future_years)

        # Simpan dictionary model ke session state
        st.session_state['trained_models'] = trained_models

        # Visualisasikan data historis dan prediksi
        historical_data = resultNational[['Tahun'] + list(y_vars.keys())]
        st.subheader("Prediksi Data Ekonomi Indonesia 10 Tahun Mendatang (2023-2033)")
        fig = go.Figure()

        # Warna dan gaya garis sesuai dengan kode kedua
        colors = {
            'Garis Kemiskinan': 'red',
            'Upah Minimum Provinsi': 'blue',
            'Pengeluaran per bulan': 'orange',
            'Rata-rata Gaji per bulan': 'green'
        }

        for target_name in y_vars.keys():
            # Tambahkan data historis
            fig.add_trace(go.Scatter(
                x=historical_data['Tahun'], y=historical_data[target_name],
                mode='lines+markers',
                name=f"{target_name} (Historis)",
                line=dict(color=colors[target_name], dash='solid'),
                marker=dict(size=6)
            ))
            # Tambahkan data prediksi
            fig.add_trace(go.Scatter(
                x=predictions['Tahun'], y=predictions[target_name],
                mode='lines+markers',
                name=f"{target_name} (Prediksi)",
                line=dict(color=colors[target_name], dash='dash'),
                marker=dict(size=6)
            ))

        fig.update_layout(
            xaxis_title="Tahun",
            yaxis_title="Value",
            legend_title="Legend",
            template="plotly_white"
        )
        st.plotly_chart(fig)

else:
    st.warning("Silakan lakukan preprocessing data terlebih dahulu dengan menekan tombol 'Start Preprocessing'.")

eval = st.button("Evaluasi Model")
if eval:
    pg = st.navigation([st.Page("views/evaluasi.py")])

st.session_state['resultNational'] = resultNational
