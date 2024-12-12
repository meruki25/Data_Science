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
        
        # Hapus noise pada kolom dan baris yang dipilih
        st.write("Hapus Noise pada Kolom dan Baris yang Dipilih:")
        df_pilihan = df_pilihan.dropna()  # Hapus baris dengan nilai kosong
        df_pilihan = df_pilihan.apply(lambda x: x.str.strip() if x.dtype == "object" else x)  # Hapus spasi pada nilai string
        df_pilihan = df_pilihan.apply(lambda x: x.astype(str).str.lower() if x.dtype == "object" else x)  # Ubah nilai string menjadi lowercase
        
        # Tampilkan hasil penghapusan noise
        st.write("Hasil Penghapusan Noise:")
        st.write(df_pilihan)
