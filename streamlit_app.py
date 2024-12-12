import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import plotly.express as px

# Judul aplikasi
st.title("🎈Aplikasi Untuk Data Science")

# Fungsi untuk membaca dataset
def load_dataset(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls"):
        return pd.read_excel(uploaded_file)

# Fungsi untuk menampilkan dataset dan informasi umum
def display_dataset_info(df):
    st.write("Dataset yang dipilih:")
    st.write(df)
    st.write("Informasi Dataset:")
    st.write(f"Jumlah Baris: {df.shape[0]}")
    st.write(f"Jumlah Kolom: {df.shape[1]}")

# Fungsi untuk menghapus noise dari dataset
def remove_noise(df):
    df = df.dropna()
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df = df.apply(lambda x: x.astype(str).str.lower() if x.dtype == "object" else x)
    return df

# Fungsi untuk menangani missing values
def handle_missing_values(df, method):
    if method == "Hapus baris":
        df = df.dropna()
        st.success("Baris dengan missing values telah dihapus.")
    elif method == "Isi dengan rata-rata":
        df.fillna(df.mean(), inplace=True)
        st.success("Missing values telah diisi dengan rata-rata.")
    elif method == "Isi dengan modus":
        for column in df.select_dtypes(include=['object']).columns:
            df[column].fillna(df[column].mode()[0], inplace=True)
        st.success("Missing values telah diisi dengan modus.")
    return df

# Fungsi untuk normalisasi data
def normalize_data(df, method):
    if method == "Min-Max Scaling":
        scaler = MinMaxScaler()
        df_normalized = pd.DataFrame(scaler.fit_transform(df.select_dtypes(include=[np.number])), columns=df.select_dtypes(include=[np.number]).columns)
        st.success("Data telah dinormalisasi menggunakan Min-Max Scaling.")
    elif method == "Z-score Normalization":
        scaler = StandardScaler()
        df_normalized = pd.DataFrame(scaler.fit_transform(df.select_dtypes(include=[np.number])), columns=df.select_dtypes(include=[np.number]).columns)
        st.success("Data telah dinormalisasi menggunakan Z-score Normalization.")
    
    for col in df_normalized.columns:
        df[col] = df_normalized[col]
    
    return df

# Fungsi untuk menampilkan visualisasi
def display_visualization(df):
    vis_type = st.selectbox('Pilih Jenis Visualisasi', ['Bar Chart', 'Pie Chart', 'Scatter Plot'])
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

# Masukkan dataset
uploaded_file = st.file_uploader("*Pilih file dataset*", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    df = load_dataset(uploaded_file)
    display_dataset_info(df)
    
    kolom_pilihan = st.multiselect("Pilih Kolom yang Diinginkan:", df.columns)
    
    if kolom_pilihan:
        df_pilihan = df[kolom_pilihan]
        st.write("Kolom yang Dipilih:")
        st.write(df_pilihan)
        
        if df_pilihan.isnull().sum().sum() > 0:
            st.write(f"Noise pada dataset ditemukan. Noise siap dihapus?")
            if st.button("Hapus Noise"):
                df_pilihan = remove_noise(df_pilihan)
                st.write("Hasil Penghapusan Noise:")
                st.write(df_pilihan)

        if st.button("Cek Missing Value"):
            st.write("Jumlah Missing Values per Kolom:")
            st.write(df_pilihan.isnull().sum())

            method = st.radio("Pilih metode penanganan missing values:", ["Hapus baris", "Isi dengan rata-rata", "Isi dengan modus"])
            
            if st.button("Terapkan Penanganan"):
                df_pilihan = handle_missing_values(df_pilihan, method)
                st.write("Hasil Penanganan Missing Values:")
                st.write(df_pilihan)
        
        if st.button("Normalisasi Data"):
            scaler_option = st.radio("Pilih metode normalisasi:", ["Min-Max Scaling", "Z-score Normalization"])
            df_pilihan = normalize_data(df_pilihan, scaler_option)
            st.write("Hasil Normalisasi Data:")
            st.write(df_pilihan)
        
        display_visualization(df_pilihan)
