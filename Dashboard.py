# Import packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

from google.colab import drive
day_df = pd.read_csv('/content/drive/MyDrive/Proyek Analisis Data/day.csv')
hour_df = pd.read_csv('/content/drive/MyDrive/Proyek Analisis Data/hour.csv')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_monthly_counts_df(df):
  monthly_counts_df = day_df.groupby(by=["mnth","yr"]).agg({"cnt": "sum"}).reset_index()
  return monthly_counts_df
def create_daily_rental_df(df):
  daily_df = day_df.groupby(by='weekday')['cnt'].sum().reindex(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']).reset_index()
  return daily_df
def create_season_pattern_df(df):
  season_pattern_df = day_df.groupby('season')[['registered', 'casual']].sum().reset_index()
  return season_pattern_df
main_df = pd.merge(day_df, hour_df, on="dteday", suffixes=("_day", "_hour"))

# st.dataframe(main_df)

## Menyiapkan berbagai dataframe
monthly_counts_df = create_monthly_counts_df(main_df)
daily_rental_df = create_daily_rental_df(main_df)
season_pattern_df_df = create_season_pattern_df(main_df)

# Streamlit app
st.title("Bike Sharing Data Dashboard")

## Mengubah angka menjadi keterangan pada day_df
day_df['mnth'] = day_df['mnth'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'})
day_df['yr'] = day_df['yr'].map({
    0: '2011', 1: '2012'})
day_df['workingday'] = day_df['workingday'].map({
    0: 'Holiday', 1: 'Workingday'})

## Mengubah tipe data menjadi data kategori pada day_df
day_df['season'] = day_df.season.astype('category')
day_df['yr'] = day_df.yr.astype('category')
day_df['mnth'] = day_df.mnth.astype('category')
day_df['holiday'] = day_df.holiday.astype('category')
day_df['weekday'] = day_df.weekday.astype('category')
day_df['workingday'] = day_df.workingday.astype('category')
day_df['weathersit'] = day_df.weathersit.astype('category')

## Mengubah angka menjadi keterangan pada hour_df
hour_df['mnth'] = hour_df['mnth'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
hour_df['season'] = hour_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
hour_df['weekday'] = hour_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
hour_df['weathersit'] = hour_df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'})
hour_df['yr'] = hour_df['yr'].map({
    0: '2011', 1: '2012'})
hour_df['workingday'] = hour_df['workingday'].map({
    0: 'Holiday', 1: 'Workingday'})

## Mengubah tipe data menjadi data kategori pada hour_df
hour_df['season'] = hour_df.season.astype('category')
hour_df['yr'] = hour_df.yr.astype('category')
hour_df['mnth'] = hour_df.mnth.astype('category')
hour_df['holiday'] = hour_df.holiday.astype('category')
hour_df['weekday'] = hour_df.weekday.astype('category')
hour_df['workingday'] = hour_df.workingday.astype('category')
hour_df['weathersit'] = hour_df.weathersit.astype('category')

main_df = pd.merge(day_df, hour_df, on="dteday", suffixes=("_day", "_hour"))

## Memperbaiki tipe data
datetime_columns = ["dteday"]
for column in datetime_columns:
  day_df[column] = pd.to_datetime(day_df[column])
for column in datetime_columns:
  hour_df[column] = pd.to_datetime(hour_df[column])

# Display data
st.header("Data")
st.subheader("Day Data", divider="blue")
st.dataframe(day_df.head())

st.subheader("Hour Data", divider="blue")
st.dataframe(hour_df.head())

# Perbandingan tren penyewaan sepeda di Tahun 2011 dan 2012
st.header("Explonatory Data Analysis :green[EDA]")
trend_bike = day_df.groupby(by='yr').agg({'cnt': 'mean'})
st.subheader("Perbandingan tren penyewaan sepeda di Tahun 2011 dan 2012")
st.dataframe(trend_bike.head())

# Pola perbandingan penyewaan sepeda harian
st.subheader("Pola perbandingan penyewaan sepeda harian")
st.dataframe(day_df.groupby(by='weekday').agg({
    'cnt': ['max', 'min', 'mean']
}).reindex(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']))

#Pola pengelompokan penyewa sepeda berdasarkan pengaruh musim
st.subheader("Pola pengelompokan penyewa sepeda berdasarkan pengaruh musim")
st.dataframe(day_df.groupby('season').agg({
    'casual': 'mean',
    'registered': 'mean',
    'cnt': ['max', 'min', 'mean']}).reindex(['Spring', 'Summer', 'Fall', 'Winter']))

#Visualisasi Data
st.header("Visualisasi Data")

##Pertanyaan 1
st.subheader("Perbandingan tren jumlah pengguna sepeda di tahun 2011 dan 2012")

day_df['mnth'] = pd.Categorical(day_df['mnth'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],ordered=True)

monthly_counts = day_df.groupby(by=["mnth", "yr"]).agg({"cnt": "sum"}).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))

sns.lineplot(data=monthly_counts, x="mnth", y="cnt", hue="yr", palette="rocket", marker="o", ax=ax)

ax.set_title("Trend Sewa Sepeda")
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.legend(title="Tahun", loc="upper right")
plt.tight_layout()

st.pyplot(fig)

## Pertanyaan 2
st.subheader("Pola perbandingan penyewaan sepeda harian")

fig, ax = plt.subplots(figsize=(10, 6))  # Menggunakan fig, ax = plt.subplots()

sns.barplot(x='weekday', y='cnt', data=day_df, order=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], palette='magma', ax=ax)  # Menambahkan ax=ax
ax.set_title('Perbandingan Penyewa Sepeda Setiap Hari')
ax.set_xlabel(None)
ax.set_ylabel('Jumlah Pengguna Sepeda')

st.pyplot(fig)

## Pertanyaan 3
st.subheader("Pengaruh musim terhadap jumlah penyewaan sepeda")
season_pattern = day_df.groupby('season')[['registered', 'casual']].sum().reset_index()

urutan_musim = ['spring', 'summer', 'fall', 'winter']

fig, ax = plt.subplots(figsize=(10, 6))

plt.bar(season_pattern['season'], season_pattern['registered'], label='Registered', color='tab:blue')
plt.bar(season_pattern['season'], season_pattern['casual'], label='Casual', color='tab:purple')

plt.xlabel(None)
plt.ylabel(None)

plt.title('Jumlah Penyewa Sepeda Berdasarkan Musim')
plt.legend()

st.pyplot(fig)

#Conclusion
st.header("Conclusion")

##Pertanyaan 1
st.subheader("Pertanyaan 1: Bagaimana perbandingan tren jumlah pengguna sepeda di tahun 2011 dan 2012?")
st.text("Tren penyewaan sepeda pengalami peningkatan dari tahun 2011 ke tahun 2012. Peningkatan tersebut dimulai pada bulan Mei hingga September dan terjadi penurunan pada akhir dan awal tahun.")

##Pertanyaan 2
st.subheader("Bagaimana pola perbandingan penyewaan sepeda harian?")
st.text("Jumlah penyewaan sepeda cenderung meningkat secara bertahap sepanjang hari kerja (dari hari Senin hingga Jumat) dengan puncaknya pada hari Jumat. Kemudian, jumlah penyewaan sepeda mengalami penurun pada akhir pekan (hari Minggu). Hal ini mengindikasikan bahwa sepeda lebih sering digunakan untuk kegiatan rutin sehari-hari seperti pergi bekerja atau sekolah, dibandingkan untuk rekreasi pada hari libur.")

##Pertanyaan 3
st.subheader("Pertanyaan 3: Bagaimana pengaruh musim terhadap jumlah penyewaan sepeda?")
st.text("Jumlah penyewaan sepeda mengalami kenaikan secara bertahap seiring pergantian musim. Pada musim semi tercatat angka penyewaan terendah, sementara musim panas dan gugur menjadi puncak popularitas bersepeda. Setelah itu, terjadi sedikit penurunan jumlah penyewaan di musim dingin.")
