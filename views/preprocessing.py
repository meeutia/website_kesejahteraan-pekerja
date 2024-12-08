import streamlit as st
import pandas as pd

st.subheader("Preprocessing")

if 'uploaded_files' in st.session_state:
    uploaded_files = st.session_state['uploaded_files']

    required_files = ["gk.df.csv", "peng.df.csv", "upah.df.csv", "ump.df.csv"]
    if all(file in uploaded_files for file in required_files):

        try:

            gk = uploaded_files["gk.df.csv"]
            pengeluaran = uploaded_files["peng.df.csv"]
            upah = uploaded_files["upah.df.csv"]
            ump = uploaded_files["ump.df.csv"]

            def clean_dataset(df):
                df = df.drop_duplicates()
                df = df.dropna()
                return df

            gk = clean_dataset(gk)
            pengeluaran = clean_dataset(pengeluaran)
            upah = clean_dataset(upah)
            ump = clean_dataset(ump)

            gkJenis = gk.query("jenis == 'TOTAL'").groupby(['tahun', 'provinsi'])['gk'].mean().round(0).reset_index()
            pengeluaranJenis = pengeluaran.query("jenis == 'TOTAL'").groupby(['tahun', 'provinsi'])['peng'].mean().round(0).reset_index()
            gkYearly = gkJenis.query("tahun >= 2015").groupby(['tahun', 'provinsi'])['gk'].mean().round(0)
            umpYearly = ump.query("tahun >= 2015").groupby(['tahun', 'provinsi'])['ump'].mean().round(0)
            pengeluaranYearly = pengeluaranJenis.query("tahun >= 2015").groupby(['tahun', 'provinsi'])['peng'].mean().round(0)
            upahYearly = upah.query("tahun >= 2015").groupby(['tahun', 'provinsi'])['upah'].mean().round(0)

            result = pd.concat([gkYearly, umpYearly, pengeluaranYearly, upahYearly], axis=1, join='outer').reset_index()

            result.rename(columns={
                'tahun': 'Tahun',
                'provinsi': 'Provinsi',
                'ump': 'Upah Minimum Provinsi',
                'gk': 'Garis Kemiskinan',
                'peng': 'Pengeluaran per bulan',
                'upah': 'Rata-rata upah per jam'
            }, inplace=True)

            st.session_state['result'] = result

            st.write("Hasil Preprocessing:")
            st.dataframe(result)

                        # Display dataset info in columns
            st.write("Informasi Dataset Setelah Pembersihan:")
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Garis Kemiskinan (GK):**")
                st.text(gk.info())
                st.write("**Upah:**")
                st.text(upah.info())

            with col2:
                st.write("**Pengeluaran:**")
                st.text(pengeluaran.info())
                st.write("**UMP:**")
                st.text(ump.info())

        except Exception as e:
            st.error(f"Terjadi kesalahan dalam preprocessing: {e}")
    else:
        st.error("Nama file tidak sesuai! Harap unggah file dengan nama berikut:")
        st.write(", ".join(required_files))
else:
    st.warning("Belum ada file yang diunggah. Silakan unggah file di halaman utama.")


visual = st.button("👀 Visualisasi")
if visual :
    pg = st.navigation([st.Page("views/visualisasi.py")])
