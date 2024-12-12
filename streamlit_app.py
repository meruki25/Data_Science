import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

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
        if jumlah_noise > 0:
            st.write(f"Noise pada dataset ditemukan sebanyak {jumlah_noise}.")
            
            # Buat tombol untuk cek missing value
            if st.button("Cek Missing Value"):
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

            # Buat tombol untuk menghapus noise (spasi dan lowercase)
            if st.button("Hapus Noise"):
                df_pilihan = df_pilihan.dropna()  # Hapus baris dengan nilai kosong
                df_pilihan = df_pilihan.apply(lambda x: x.str.strip() if x.dtype == "object" else x)  # Hapus spasi pada nilai string
                df_pilihan = df_pilihan.apply(lambda x: x.astype(str).str.lower() if x.dtype == "object" else x)  # Ubah nilai string menjadi lowercase
                
                # Tampilkan hasil penghapusan noise
                st.write("Hasil Penghapusan Noise:")
                st.write(df_pilihan)
