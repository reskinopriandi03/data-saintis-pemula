import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np


st.header('Dashboard Bike Rental')
st.write('selamat datang di web kami. halaman ini adalah hasil analisis dari data "Bike Sharing Dataset".')
st.subheader('sumber data "penyewaan perseason"')
st.write('berikut adalah tampilan ringkas dari data semula :')

###membaca file CSV
# Path file hour_df
day_df = pd.read_csv("https://raw.githubusercontent.com/reskinopriandi03/data-saintis-pemula/main/data/day_df.csv")
# Path file day_df
hour_df = pd.read_csv("https://raw.githubusercontent.com/reskinopriandi03/data-saintis-pemula/main/data/hour_df.csv")

st.code(day_df, language='python')

st.write('setelah melewati beberapa tahapan dalam analisis data, berikut hasil dari analisis kami :')


# Fungsi hitung_penyewaan_per_musim
def hitung_penyewaan_per_musim(day_df, tahun):
    result_season = day_df[day_df['yr'] == tahun].groupby('season')['cnt'].sum().reset_index()
    result_season['season'] = result_season['season'] + 1
    return result_season

# Memanggil fungsi hitung_penyewaan_per_musim untuk tahun 2011 dan 2012
result_season1 = hitung_penyewaan_per_musim(day_df, 0)
result_season2 = hitung_penyewaan_per_musim(day_df, 1)

# Menggabungkan hasil dari kedua tahun
merged_seasons = result_season1.merge(result_season2, on='season', suffixes=('_2011', '_2012'))

# Membuat posisi untuk setiap musim pada sumbu x
bar_width = 0.35  # Lebar setiap bar
r1 = np.arange(len(merged_seasons))  # Posisi untuk tahun 2011
r2 = [x + bar_width for x in r1]  # Posisi untuk tahun 2012

# Membuat plot di Streamlit
fig, ax = plt.subplots(figsize=(10, 6))

# Grafik bar untuk tahun 2011
ax.bar(r1, merged_seasons['cnt_2011'], color='skyblue', width=bar_width, edgecolor='grey', label='2011')

# Grafik bar untuk tahun 2012
ax.bar(r2, merged_seasons['cnt_2012'], color='orange', width=bar_width, edgecolor='grey', alpha=0.7, label='2012')

ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_title('Perbandingan Jumlah Penyewaan di Tahun 2011 dan 2012 untuk Setiap Musim')
ax.set_xticks([r + bar_width / 2 for r in range(len(merged_seasons))])
ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])

ax.legend()

# Menampilkan plot di Streamlit
st.pyplot(fig)
st.write('dari tampilan diagram diatas jumlah pengunjung terbanyak ada pada musim gugur(fall). serta terlihat juga peningkatan secara umum setiap musimnya dari tahun 2011 dan 2012.')
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

st.subheader('sumber data "penyewaan perjam"')
st.write('berikut adalah tampilan ringkas dari data semula :')
st.code(hour_df, language='python')
st.write('setelah melewati beberapa tahapan dalam analisis data, berikut hasil dari analisis kami :')

# Fungsi untuk menghasilkan plot
def plot_hourly_visitors(hour_df):
    # Jumlah banyak pengunjung di tahun 2011 menurut jam operasional
    result_hour1 = hour_df[hour_df['yr'] == 0].groupby('hr')['cnt'].sum().reset_index()
    result_hour1['hr'] = result_hour1['hr']

    # Jumlah banyak pengunjung di tahun 2012 menurut jam operasional
    result_hour2 = hour_df[hour_df['yr'] == 1].groupby('hr')['cnt'].sum().reset_index()
    result_hour2['hr'] = result_hour2['hr']

    # Membuat posisi untuk setiap jam operasional pada sumbu x
    bar_width = 0.35  # Lebar setiap bar
    r1 = np.arange(len(result_hour1))  # Posisi untuk tahun 2011
    r2 = [x + bar_width for x in r1]  # Posisi untuk tahun 2012

    # Membuat plot di Streamlit
    fig, ax = plt.subplots(figsize=(12, 6))

    # Grafik bar untuk tahun 2011
    ax.bar(r1, result_hour1['cnt'], color='skyblue', width=bar_width, edgecolor='grey', label='2011')

    # Grafik bar untuk tahun 2012
    ax.bar(r2, result_hour2['cnt'], color='orange', width=bar_width, edgecolor='grey', alpha=0.7, label='2012')

    ax.set_xlabel('Jam Operasional')
    ax.set_ylabel('Jumlah Pengunjung')
    ax.set_title('Perbandingan Jumlah Pengunjung pada Jam Operasional antara Tahun 2011 dan 2012')
    ax.set_xticks([r + bar_width / 2 for r in range(len(result_hour1))])  # Memberikan label jam operasional pada sumbu x
    ax.set_xticklabels(result_hour1['hr'])
    ax.legend()

    # Menampilkan plot di Streamlit
    st.pyplot(fig)
print(hour_df.info())
# Memanggil fungsi untuk menghasilkan plot
plot_hourly_visitors(hour_df)


st.write('dari diagram diatas terlihat peningkatan jumlah pengunjung dari tahun 2011 hingga 2012. rata - rata waktu ramai pengunjung terjadi pada pukul 16.00 hingga 19.00. serta informasi yang tidak kalah menarik adalah masih terdapat pengunjung yang menyewa sepeda pada dini hari.')

#########################Membuat Komponen Filter######################
#Setelah berhasil menyiapkan DataFrame yang akan digunakan, tahap berikutnya ialah menambahkan filter pada dashboard yang akan dibuat. dalam hal ini, kita akan menggunakan widget date input sebagai filternya dan akan ditempatkan pada bagian sidebar. Selain itu, untuk alasan estetika, kita juga perlu menambahkan logo perusahaan ke dalam sidebar tersebut. 
#Berikut merupakan kode yang dapat Anda gunakan untuk membuat filter dengan widget date input serta menambahkan logo perusahaan pada sidebar.

#membuat sidebar kalender
datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/reskinopriandi03/data-saintis-pemula/blob/main/data/kelinci_bersepeda.jpg?raw=true")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

#Kode di atas akan menghasilkan start_date dan end_date yang selanjutnya akan digunakan untuk memfilter DataFrame. Berikut merupakan tampilan sidebar yang akan dihasilkan dari kode tersebut.
#st.code(all_df, language='python')

#Nah, start_date dan end_date di atas akan digunakan untuk memfilter all_df. Data yang telah difilter ini selanjutnya akan disimpan dalam main_df.
main_date_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]




st.caption('Copyright (c) Data Scientist Pemula 2023.')
