import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px


st.title("🎈Aplikasi Untuk Data Science")

# Buat tombol untuk memasukkan dataset
uploaded_file = st.file_uploader("*Pilih file dataset*", type=["csv", "xlsx", "xls"])

# Jika tombol ditekan, maka akan memasukkan dataset
if uploaded_file is not None:
    # Baca file dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls"):
        df = pd.read_excel(uploaded_file)
    
    # Tampilkan dataset
    st.write("Dataset yang dipilih:")
    st.write(df)
    
    # Hitung jumlah baris dan kolom
    jumlah_baris = df.shape[0]
    jumlah_kolom = df.shape[1]
    
    # Tampilkan jumlah baris dan kolom
    st.write("Informasi Dataset:")
    st.write(f"Jumlah Baris: {jumlah_baris}")
    st.write(f"Jumlah Kolom: {jumlah_kolom}")
    
    # Pilih kolom yang diinginkan
    st.write("Pilih Kolom yang Diinginkan:")
    kolom_pilihan = st.multiselect("Pilih Kolom", df.columns)
    
    # Tampilkan kolom yang dipilih
    if kolom_pilihan:
        df_pilihan = df[kolom_pilihan]
        st.write("Kolom yang Dipilih:")
        st.write(df_pilihan)
        
        # Hitung jumlah noise pada kolom dan baris yang dipilih
        jumlah_noise = df_pilihan.isnull().sum().sum()
        
        # Tampilkan pesan noise
        if jumlah_noise == 0:
            st.write("Noise pada dataset tidak ditemukan!!")
        else:
            st.write(f"Noise pada dataset ditemukan sebanyak {jumlah_noise}. Noise siap dihapus?")
            
            # Buat tombol untuk menghapus noise
            if st.button("Hapus Noise"):
                df_pilihan = df_pilihan.dropna()  # Hapus baris dengan nilai kosong
                df_pilihan = df_pilihan.apply(lambda x: x.str.strip() if x.dtype == "object" else x)  # Hapus spasi pada nilai string
                df_pilihan = df_pilihan.apply(lambda x: x.astype(str).str.lower() if x.dtype == "object" else x)  # Ubah nilai string menjadi lowercase
                
                # Tampilkan hasil penghapusan noise
                st.write("Hasil Penghapusan Noise:")
                st.write(df_pilihan)
                
            # Buat tombol untuk cek missing value
            if missing_value == 0:
                st.write("Missing Value tidak ditemukan!!!")
            else:                
                # Tampilkan jumlah missing value per kolom
                missing_values = df_pilihan.isnull().sum()
                st.write("Jumlah Missing Values per Kolom:")
                st.write(missing_values[missing_values > 0])
                
                # Pilih metode penanganan missing values
                method = st.radio("Pilih metode penanganan missing values:", ["Hapus baris", "Isi dengan rata-rata", "Isi dengan modus"])
                
                if st.button("Terapkan Penanganan"):
                    if method == "Hapus baris":
                        df_pilihan = df_pilihan.dropna()
                        st.success("Baris dengan missing values telah dihapus.")
                    elif method == "Isi dengan rata-rata":
                        df_pilihan.fillna(df_pilihan.mean(), inplace=True)
                        st.success("Missing values telah diisi dengan rata-rata.")
                    elif method == "Isi dengan modus":
                        for column in df_pilihan.select_dtypes(include=['object']).columns:
                            df_pilihan[column].fillna(df_pilihan[column].mode()[0], inplace=True)
                        st.success("Missing values telah diisi dengan modus.")
                    
                    # Tampilkan hasil penanganan missing values
                    st.write("Hasil Penanganan Missing Values:")
                    st.write(df_pilihan)

            # Normalisasi Data
            if st.button("Normalisasi Data"):
                scaler_option = st.radio("Pilih metode normalisasi:", ["Min-Max Scaling", "Z-score Normalization"])
                
                if scaler_option == "Min-Max Scaling":
                    scaler = MinMaxScaler()
                    df_normalized = pd.DataFrame(scaler.fit_transform(df_pilihan.select_dtypes(include=[np.number])), columns=df_pilihan.select_dtypes(include=[np.number]).columns)
                    st.success("Data telah dinormalisasi menggunakan Min-Max Scaling.")
                elif scaler_option == "Z-score Normalization":
                    scaler = StandardScaler()
                    df_normalized = pd.DataFrame(scaler.fit_transform(df_pilihan.select_dtypes(include=[np.number])), columns=df_pilihan.select_dtypes(include=[np.number]).columns)
                    st.success("Data telah dinormalisasi menggunakan Z-score Normalization.")
                
                # Menyimpan hasil normalisasi ke dalam dataframe asli
                for col in df_normalized.columns:
                    df_pilihan[col] = df_normalized[col]
                
                # Tampilkan hasil normalisasi
                st.write("Hasil Normalisasi Data:")
                st.write(df_pilihan)

             # Pilih jenis visualisasi
            vis_type = st.selectbox(
                'Pilih Jenis Visualisasi',
                ['Bar Chart', 'Pie Chart', 'Scatter Plot']
            )
        
            # Tampilkan opsi kolom untuk plot
            columns_option = st.multiselect('Pilih Kolom untuk Plotting:', list(df.columns))
        
            if len(columns_option) > 0:
                selected_df = df[columns_option].copy()
        
                if vis_type == 'Bar Chart':
                    fig = px.bar(selected_df.melt(), x='variable', y='value')
                    st.plotly_chart(fig)
                
                elif vis_type == 'Pie Chart':
                    fig = px.pie(selected_df.sum().reset_index(name='total'), names=selected_df.columns.tolist())
                    st.plotly_chart(fig)
                
                elif vis_type == 'Scatter Plot':
                    fig = px.scatter(selected_df.reset_index(drop=True))
                    for col in selected_df.columns[:-1]:
                        fig.add_scatter(x=df[col], y=df[selected_df.columns[-1]])
                    
                    st.plotly_chart(fig)
