import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Visualisasi")

visual_option = st.selectbox('Pilih', ['Visualisasi 1', 'Visualisasi 2', 'Visualisasi 3','Visualisasi 4'])

if visual_option == 'Visualisasi 1':
    st.subheader('Provinsi dengan rata-rata upah bulanan (asumsi jam kerja adalah 173 jam per bulan) lebih rendah dari UMP')
    if 'result' in st.session_state:
        result = st.session_state['result']
        
        result['Rata-rata Gaji per bulan'] = result['Rata-rata upah per jam'] * 173
        result['Salary-Status'] = np.where(result['Rata-rata Gaji per bulan'] < result['Upah Minimum Provinsi'], 'Dibawah UMP', 'Tidak dibawah UMP')

        all_years = pd.DataFrame({'Tahun': range(result['Tahun'].min(), result['Tahun'].max() + 1)})

        countYearGrouped = (
            result[result["Salary-Status"] == "Dibawah UMP"]
            .groupby("Tahun")
            .size()
            .reset_index(name="Jumlah")
            .merge(all_years, on="Tahun", how="right")
            .fillna(0) 
        )

        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=countYearGrouped['Tahun'],
            y=countYearGrouped['Jumlah'],
            name="Provinsi dengan Gaji dibawah UMP",
            marker_color='#379777'
        ))
        fig1.update_layout(
            title="Jumlah Provinsi dengan rata-rata Gaji di bawah UMP",
            xaxis_title="Tahun",
            yaxis_title="Jumlah",
            xaxis=dict(tickmode='linear')
        )

        countProvince = result.query("`Salary-Status` == 'Dibawah UMP'")
        countProvinceGrouped = countProvince.groupby(['Provinsi']).size().reset_index(name='Jumlah')

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=countProvinceGrouped['Provinsi'],
            y=countProvinceGrouped['Jumlah'],
            name="Provinsi dibawah UMP",
            marker_color='#379777'
        ))
        fig2.update_layout(
            title="Jumlah Kejadian Provinsi di Bawah UMP",
            xaxis_title="",
            yaxis_title="Jumlah"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(fig1)

        with col2:
            st.plotly_chart(fig2)

        st.write("""
        **Jumlah Provinsi dengan Rata-Rata Upah Bulanan Dibawah UMP pada 2015-2022**
        
        - **Tahun 2022** merupakan tahun dengan jumlah provinsi terbanyak dengan rata-rata upah bulanan dibawah UMP, yaitu sebanyak 9 provinsi.
        - **Tahun 2015** tidak terdapat provinsi dengan rata-rata upah bulanan dibawah UMP.
        """)

        st.write("""
        **Frekuensi Provinsi Memiliki Rata-Rata Upah Bulanan Dibawah UMP pada 2015-2022**
        
        - Terdapat 9 provinsi yang setidaknya pernah memiliki rata-rata upah bulanan dibawah UMP pada periode 2015-2022.
        - **Sumatera Selatan** memiliki frekuensi tertinggi dengan rata-rata upah bulanan di bawah UMP sebanyak 7 kali pada periode ini.
        """)
        st.dataframe(result)
    else:
        st.warning("Silakan lakukan preprocessing terlebih dahulu dengan menekan tombol 'Start Preprocessing'.")

elif visual_option == 'Visualisasi 2':
    st.subheader('Korelasi antar atribut')

    if 'result' in st.session_state:
        result = st.session_state['result']

        corr_matrix = result.loc[:, ~result.columns.isin(['Provinsi', 'Tahun', 'Salary-Status'])].corr()

        plt.figure(figsize=(10, 8))

        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, square=True)

        plt.tight_layout()

        st.pyplot(plt)

    else:
        st.warning("Silakan lakukan preprocessing terlebih dahulu dengan menekan tombol 'Start Preprocessing'.")

elif visual_option == 'Visualisasi 3':
    if 'result' in st.session_state:
        result = st.session_state['result']

        resultNational = result[result['Provinsi'] == 'INDONESIA']

        fig3 = go.Figure()
        
        fig3.add_trace(go.Scatter(
            x=resultNational['Tahun'],
            y=resultNational['Garis Kemiskinan'],
            mode='lines+markers',
            name='Garis Kemiskinan',
            line=dict(color='blue')
        ))
        
        fig3.add_trace(go.Scatter(
            x=resultNational['Tahun'],
            y=resultNational['Upah Minimum Provinsi'],
            mode='lines+markers',
            name='Upah Minimum Provinsi (UMP)',
            line=dict(color='orange')
        ))

        fig3.add_trace(go.Scatter(
            x=resultNational['Tahun'],
            y=resultNational['Pengeluaran per bulan'],
            mode='lines+markers',
            name='Pengeluaran Bulanan',
            line=dict(color='green')
        ))

        fig3.add_trace(go.Scatter(
            x=resultNational['Tahun'],
            y=resultNational['Rata-rata Gaji per bulan'],
            mode='lines+markers',
            name='Rata-rata Gaji per Bulan',
            line=dict(color='red')
        ))

        fig3.update_layout(
            xaxis_title="Tahun",
            yaxis_title="Nilai",
            legend_title="Indikator",
            xaxis=dict(tickmode='linear')
        )

        st.plotly_chart(fig3)
    else:
        st.warning("Silakan lakukan preprocessing terlebih dahulu dengan menekan tombol 'Start Preprocessing'.")


if visual_option == 'Visualisasi 4':
    st.subheader('Perbandingan Gaji dan Pengeluaran di Provinsi')
    if 'result' in st.session_state:
        result = st.session_state['result']

        averageProvinceSalary = result.groupby(['Provinsi'])['Rata-rata Gaji per bulan'].mean().round(0)
        averageProvinceExpense = result.groupby(['Provinsi'])['Pengeluaran per bulan'].mean().round(0)

        averageProvince = pd.concat([averageProvinceSalary, averageProvinceExpense], axis=1, join='outer').reset_index()
        averageProvince['Rata-rata Gaji per bulan (dalam Juta)'] = averageProvince['Rata-rata Gaji per bulan'] / 1000000
        averageProvince['Pengeluaran per bulan (dalam Juta)'] = averageProvince['Pengeluaran per bulan'] / 1000000

        fig4_1 = go.Figure()
        fig4_1.add_trace(go.Scatter(
            x=averageProvince['Pengeluaran per bulan (dalam Juta)'],
            y=averageProvince['Rata-rata Gaji per bulan (dalam Juta)'],
            mode='markers',
            marker=dict(size=10, color='#379777'),
            text=averageProvince['Provinsi']
        ))
        fig4_1.update_layout(
            title="Pengeluaran vs. Gaji Bulanan per Provinsi",
            xaxis_title="Pengeluaran per Bulan (dalam Juta)",
            yaxis_title="Rata-rata Gaji per Bulan (dalam Juta)"
        )

        averageProvince['Persentase'] = 100 * averageProvince['Rata-rata Gaji per bulan'] / averageProvince['Pengeluaran per bulan']
        averageProvincePercentage = averageProvince.query("Provinsi != 'INDONESIA'")
        averageProvincePercentage = averageProvincePercentage.sort_values(by=['Persentase'], ascending=False)

        fig4_2 = go.Figure(go.Bar(
            x=averageProvincePercentage['Persentase'],
            y=averageProvincePercentage['Provinsi'],
            orientation='h',
            marker_color='#379777'
        ))
        fig4_2.update_layout(
            title="Ranking Persentase Perbandingan Gaji terhadap Pengeluaran",
            xaxis_title="Persentase (%)",
            yaxis_title="Provinsi"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(fig4_1)

        with col2:
            st.plotly_chart(fig4_2)

        st.write("""
        
        - Provinsi Papua memiliki persentase selisih upah dan pengeluaran tertinggi (358,89%) di Indonesia (pemasukan tinggi, pengeluaran rendah), sedangkan Provinsi Bangka Belitung adalah yang terendah (198,16%)
        - Hampir seluruh provinsi memiliki pemasukan lebih dari 2 kali lipat pengeluaran (200%), kecuali DI Jogjakarta (199,82%) dan Bangka Belitung (198,16%)
        """)

    else:
        st.warning("Silakan lakukan preprocessing terlebih dahulu dengan menekan tombol 'Start Preprocessing'.")

predict = st.button("Prediksi Kesejahteraan 10 tahun kedepan")
if predict :
    pg = st.navigation([st.Page("views/predict.py")])