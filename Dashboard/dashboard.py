import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import math
sns.set(style='dark')

# Menyiapkan monthlysum_df
def create_monthlysum_df(d_df):
    d_df['dteday'] = pd.to_datetime(d_df['dteday'])
    monthlysum_df = d_df.resample(rule = 'ME', on = 'dteday').agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
    }).reset_index()
    
    monthlysum_df['dteday'] = monthlysum_df['dteday'].dt.to_period('M').astype(str)

    return monthlysum_df

# Menyiapkan comptype_df
def create_comptype_df(d_df):
    comptype_df = pd.DataFrame({
    'Type': ['Casual', 'Registered'],
    'Total': [d_df['casual'].sum(), d_df['registered'].sum()]})

    return comptype_df

# Menyiapkan daily_df
def create_daily_df(d_df):
    daily_df = d_df.resample(rule = 'D', on = 'dteday').agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
    }).reset_index()
    
    daily_df['dteday'] = daily_df['dteday'].dt.to_period('D').astype(str)

    return daily_df

# Menyiapkan cntsort_df
def create_cntsort_df(d_df):
    cntsort_df = d_df.resample(rule = 'ME', on = 'dteday').agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
    }).reset_index().sort_values(by = ['cnt'], ascending=False)
    
    cntsort_df['dteday'] = cntsort_df['dteday'].dt.to_period('M').astype(str)

    return cntsort_df

# Menyiapkan monthly2011_df
def create_monthly2011_df(m_df):
    monthly2011_df = m_df[m_df['dteday'].str.startswith('2011')]

    return monthly2011_df

# Menyiapkan monthly2012_df
def create_monthly2012_df(m_df):
    monthly2012_df = m_df[m_df['dteday'].str.startswith('2012')]

    return monthly2012_df

# Menyiapkan hourmean_df
def create_hourmean_df(h_df):
    hourmean_df = h_df[h_df['holiday'] == 1].groupby('hr')['cnt'].mean().sort_values(ascending=False).reset_index()

    return hourmean_df

# Menyiapkan timecat_df
def create_timecat_df(h_df):
    timecat_df = h_df.groupby([
    h_df['hr'].apply(lambda j: 'Pagi Buta' if j <= 5 else 'Pagi' if j <= 10 else 'Siang' if j <= 15 else 'Sore' if j <= 19 else 'Malam')
    ])[['casual','registered','cnt']].mean().reset_index()

    return timecat_df

# Menyiapkan yearmean_df
def create_yearmean_df(d_df):
    yearmen_df = d_df.groupby(d_df['dteday'].dt.year)['cnt'].mean().reset_index()

    return yearmen_df

# Menyiapkan temp_df
def create_temp_df(d_df):
    temp_df = d_df.groupby([
    d_df['temp'].apply(lambda t: 'Very Cold' if t <= 0.3 else 'Cold' if t <= 0.5 else 'Warm' if t <= 0.7 else 'Hot')
    ])[['casual','registered','cnt']].sum().reset_index()

    return temp_df

# Menyiapkan atemp_df
def create_atemp_df(d_df):
    atemp_df = d_df.groupby([
    d_df['atemp'].apply(lambda at: 'Cold' if at <= 0.3 else 'Good' if at <= 0.6 else 'hot')
    ])[['casual','registered','cnt']].sum().reset_index()

    return atemp_df

# Menyiapkan hum_df
def create_hum_df(d_df):
    hum_df = d_df.groupby([
    d_df['hum'].apply(lambda h: 'Low' if h <= 0.3 else 'Moderate' if h <= 0.6 else 'High')
    ])[['casual','registered','cnt']].sum().reset_index()

    return hum_df

# Menyiapkan wind_df
def create_wind_df(d_df):
    wind_df = d_df.groupby([
    d_df['windspeed'].apply(lambda w: 'Low' if w <= 0.2 else 'Moderate' if w <= 0.4 else 'High')
    ])[['casual','registered','cnt']].sum().reset_index()

    return wind_df

# Menghasilkan weather_df
def create_weather_df(h_df):
    weather_df = (h_df.groupby('weathersit')[['casual',
                                            'registered','cnt']].sum().reset_index().assign(weathersit = lambda w: w['weathersit'].map({
                                  1: 'Clear/cloudy',
                                  2: 'Mist',
                                  3: 'Light snow/rain',
                                  4: 'Heavy rain/snow/fog'
                              })).rename(columns = {
                                  'weathersit': 'Cuaca',
                                  'casual': 'Jumlah Pengguna Casual',
                                  'registered': 'Jumlah Pengguna Registered',
                                  'cnt': 'Jumlah Sepeda Total'})).sort_values(by = ['Jumlah Sepeda Total'], ascending=False)

    return weather_df

# Load berkas
day_df = pd.read_csv(r"D:\Delta\Statistika\Semester 6\DBS\Week 3\Proyek Akhir\day.csv")
hour_df = pd.read_csv(r"D:\Delta\Statistika\Semester 6\DBS\Week 3\Proyek Akhir\hour.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Menghasilkan dataframe untuk visualisasi
monthlysum_df = create_monthlysum_df(day_df)
comptype_df = create_comptype_df(day_df)
daily_df = create_daily_df(day_df)
cntsort_df = create_cntsort_df(day_df)
hourmean_df = create_hourmean_df(hour_df)
timecat_df = create_timecat_df(hour_df)
yearmean_df = create_yearmean_df(day_df)
temp_df = create_temp_df(day_df)
atemp_df = create_atemp_df(day_df)
hum_df = create_hum_df(day_df)
wind_df = create_wind_df(day_df)
weather_df = create_weather_df(hour_df)

# Untuk monthly2011_df dan monthly2012_df

monthly2011_df = create_monthly2011_df(monthlysum_df)
monthly2012_df = create_monthly2012_df(monthlysum_df)

# Melengkapi Dashboard dengan Visualisasi Data

st.header('Capital Bike Share Dashboard')
st.text('''Berikut merupakan dashboard dari dataset Bike Share. Dataset tersebut berisi jumlah sepeda sewaan per jam dan per hari antara tahun 2011 dan 2012 di sistem berbagi sepeda Capital dengan informasi cuaca dan musim yang sesuai.''')

tab1, tab2, tab3 = st.tabs(["Total Penyewaan Sepeda", "Penyewaan Sepeda Tertinggi", "Penyewaan Sepeda di Berbagai Kondisi"])

with tab1:
    ## Informasi Total Penyewaan Sepeda
    st.subheader('Total Sepeda yang Disewa Sepanjang Januari 2011 Hingga Desember 2012')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_casual = day_df['casual'].sum()
        st.metric("Total Sewa Casual", value = total_casual)
    
    with col2:
        total_registered = day_df['registered'].sum()
        st.metric('Total Sewa Register', value = total_registered)
    
    with col3:
        total_sewa = day_df['cnt'].sum()
        st.metric('Total Sewa', value = total_sewa)
        
    ### Plot Total Penyewaan Sepeda
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        monthlysum_df["dteday"],
        monthlysum_df["cnt"],
        marker='o', 
        markersize=8,
        linewidth=3,
        color="#458018",
        linestyle="-")
    
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=10, rotation = 30)
    ax.grid(True, linestyle="--", alpha=0.5)
    
    st.pyplot(fig)
    
    with st.expander("See explanation"):
        st.write(
            """Jumlah sepeda yang disewa oleh sistem Bike Central Share mengalami fluktuatif, 
            yakni meningkat pada semester pertama dan menurun di semester kedua, 
            lalu meningkat lagi pada semester pertama di tahun berikutnya dan menurun lagi di semester berikutnya.
            Terlihat bahwa jumlah sepeda yang disewa terendah berada pada akhir tahun 2011 hingga awal tahun 2012.
            """)
    
    ### Menampilkan kenaikan penyewaan sepeda dari 2011 ke 2012
    incyear = (yearmean_df['cnt'].pct_change() * 100).fillna(0).iloc[-1]
    yearmean_df['cnt'] = yearmean_df['cnt'].apply(math.ceil)
    value_inc = yearmean_df['cnt'].iloc[-1]
    st.metric('Kenaikan Jumlah Sepeda Sewa', value = value_inc, delta = f"{incyear:.2f}%")
    
    ### Plot Total Penyewaan Sepeda berdasarkan Tipe
    fig, ax = plt.subplots(figsize=(16, 8))
    
    ax.plot(
        monthlysum_df["dteday"],
        monthlysum_df["casual"],
        marker='o',
        markersize=8,
        linewidth=3,
        color="Green")
    
    ax.plot(
        monthlysum_df["dteday"],
        monthlysum_df["registered"],
        marker='o',
        markersize=8,
        linewidth=3,
        color="Lime")
    
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=10, rotation = 30)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    st.pyplot(fig)
    
    with st.expander("See explanation"):
        st.write(
            """Pola jumlah sepeda sewa berdasarkan tipe pengguna (casual dan registered) tidak jauh berbeda dengan pola total sepeda yang disewa.
            Dapat dilihat bahwa sepanjang waktu, sepeda lebih banyak disewa oleh pengguna yang sudah terdaftar (registered) jika dibandingkan dengan
            pengguna casual.
            """)

    ### Plot Proporsi Jumlah Sepeda Sewa berdasarkan Tipe
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_comp = ['Green', 'Lime']
    ax.pie(comptype_df['Total'], labels = comptype_df['Type'],
           autopct='%1.1f%%', startangle=90,
           colors = colors_comp, wedgeprops={'linewidth': 1, 'edgecolor': 'black'},
           textprops={'fontsize': 14})
        
    st.pyplot(fig)

with tab2:
    ## Informasi Waktu Jumlah Sepeda Sewa Tertinggi
    ### Menampilkan Bulan dengan Jumlah Sepeda Sewa Tertinggi
    st.subheader("Kapan Saja Capital Bike Share Mengalami Jumlah Penyewaan Sepeda Terbanyak?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(16, 8))
        colors_2011 = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3",
                       "Lime", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", 
                       "#D3D3D3", "#D3D3D3"]
        sns.barplot(y = 'cnt',
                    x = 'dteday',
                    data = monthly2011_df,
                    palette = colors_2011,
                    ax = ax)
        ax.set_title("Jumlah Sepeda Sewa Tahun 2011", loc="center", fontsize=30)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=20, rotation = 30)
        ax.tick_params(axis='y', labelsize=20)
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(16, 8))
        colors_2012 = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", 
                       "#D3D3D3", "#D3D3D3", "Lime", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        sns.barplot(y = 'cnt',
                    x = 'dteday',
                    data = monthly2012_df,
                    palette = colors_2012,
                    ax = ax)
        ax.set_title("Jumlah Sepeda Sewa Tahun 2012", loc="center", fontsize=30)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=20, rotation = 30)
        ax.tick_params(axis='y', labelsize=20)
        st.pyplot(fig)
        
        with st.expander("See explanation"):
            st.write(
                """Pada tahun 2011, terlihat bahwa bulan dimana terjadi penyewaan sepeda tertinggi pada Capital Bike Central adalah di bulan Juni.
                Sementara pada tahun 2012, bulan dimana terjadi penyewaan sepeda tertinggi adalah pada bulan September.
                """)
    
    ### Menampilkan Waktu dengan Penyewaan Sepeda Tertinggi
    st.subheader("Sore Hari Merupakan Waktu yang Cocok untuk Bersepeda!")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_timecat = ["#C3F998", "#ACF771", "#D3D3D3", "Lime", "Green"]
    ax.pie(timecat_df['cnt'], labels = timecat_df['hr'],
           autopct=lambda pt: f'{pt:.1f}%' if pt > 3 else '',
           startangle=90, colors = colors_timecat, wedgeprops={'linewidth': 1, 'edgecolor': 'black'}, textprops={'fontsize': 14})
    
    st.pyplot(fig)
    
    with st.expander("See explanation"):
        st.write(
            """Sore hari merupakan waktu yang cocok untuk bersepeda. Dapat dilihat bahwa berdasarkan pie chart di atas, 
            waktu sore hari cenderung lebih banyak dipakai para penyewa sepeda di Capital Bike Share, lalu diikuti oleh waktu siang dan pagi hari.
            Ternyata, ada juga yang menyewa sepeda di pagi buta.
            """)
    
    ### Menampilkan Jumlah Sepeda yang Disewa Selama Hari Libur
    st.subheader("Bagaimana Jumlah Penyewaan Sepeda pada saat Hari Libur?")
    
    fig, ax = plt.subplots(figsize=(16, 8))
    colors_hour = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3",
                   "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3", "#D3D3D3",
                   "#D3D3D3", "#D3D3D3", "#D3D3D3", "Lime", "#D3D3D3",
                   "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3",
                   "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(y = 'cnt',
                x = 'hr',
                data = hourmean_df,
                palette = colors_hour,
                ax = ax)
    ax.set_title("Jumlah Sepeda Sewa pada saat Hari Libur (per jam)", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    st.pyplot(fig)
    
    with st.expander("See explanation"):
        st.write(
            """Pada hari libur, para penyewa sepeda di Capital Bike Share lebih banyak memulai untuk menyewa sepeda
            pada jam 1 siang, dan diikuti pada jam 5 sore. Berdasarkan grafiknya juga, penyewaan sepeda lebih banyak dilakukan di siang hingga sore hari
            pada hari libur.
            """)

with tab3:
    ## Informasi Jumlah Sepeda yang Disewa pada Berbagai Kondisi
    ### Menampilkan Jumlah Sepeda yang Disewa Berdasarkan Humidity dan Windspeed
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text('Proporsi Jumlah Sepeda Sewa Berdasarkan Humidity')
        fig, ax = plt.subplots(figsize=(16, 8))
        colors_hum = ["Lime", "#D3D3D3", "#ACF771"]
        explode = (0.05, 0, 0)
        ax.pie(hum_df['cnt'], labels = hum_df['hum'],
               autopct=lambda pct3: f'{pct3:.1f}%' if pct3 > 2 else '',
               startangle=90, colors = colors_hum, explode = explode,
               wedgeprops={'linewidth': 1, 'edgecolor': 'black'}, textprops={'fontsize': 14})
        st.pyplot(fig)

        with st.expander("See explanation"):
            st.write(
                """Berdasarkan pie chart di atas, banyak sepeda yang justru disewa pada saat tingkat kelembamannya tinggi (high). 
                Artinya, banyak penyewa sepeda yang justru bersepeda pada saat tingkat kelembamannya tersebut.
                Meskipun tidak jauh berbeda proporsinya dengan tingkat kelembaman moderate, hal tersebut perlu diperhatikan mengingat banyak efek
                samping yang dapat timbul akibat beraktivitas di tingkat kelembaman tinggi.
                """)
        
    with col2:
        st.text('Proporsi Jumlah Sepeda Sewa Berdasarkan Windspeed')
        fig, ax = plt.subplots(figsize=(16, 8))
        colors_wind = ["#D3D3D3", "Lime", "#ACF771"]
        explode = (0, 0.05, 0)
        ax.pie(wind_df['cnt'], labels = wind_df['windspeed'],
               autopct=lambda pct2: f'{pct2:.1f}%' if pct2 > 2 else '',
               startangle=90, colors = colors_wind, explode = explode,
               wedgeprops={'linewidth': 1, 'edgecolor': 'black'}, textprops={'fontsize': 14})
        st.pyplot(fig)

        with st.expander("See explanation"):
            st.write(
                """Berdasarkan pie chart di atas, banyak sepeda yang disewa dan digunakan pada tingkat kecepatan angin yang rendah (low), 
                disusul oleh tingkat kecepatan angin moderate, dan sangat sedikit pada saat tingkat kecepatan anginnya tinggi (high).
                """)
    
    ### Menampilkan Jumlah Sepeda yang Disewa Berdasarkan Suhu
    col1, col2 = st.columns(2)
    
    with col1:
        st.text('Proporsi Jumlah Sepeda Sewa Berdasarkan Suhu Aktual')
        fig, ax = plt.subplots(figsize=(16, 8))
        col_temp = ["#A0F55D" ,"#C3F998", "#D3D3D3", "Lime"]
        explode = (0, 0, 0, 0.05)
        ax.pie(temp_df['cnt'], labels = temp_df['temp'],
               autopct=lambda pct4: f'{pct4:.1f}%',
               startangle=90, colors = col_temp, explode = explode,
               wedgeprops={'linewidth': 1, 'edgecolor': 'black'}, textprops={'fontsize': 14})
        st.pyplot(fig)
        
        with st.expander("See explanation"):
            st.write(
                """Berdasarkan pie chart di atas, para penyewa sepeda cenderung bersepeda pada saat 
                suhu aktual atau suhu udara di sekitarnya hangat, diikuti suhu udara dingin dan panas.
                Suhu udara hangat cenderung dapat dirasakan pada saat sore hari, dimana waktu tersebut
                adalah waktu dominan para penyewa sepeda mulai beraktivitas dengan sepedanya.
            """)
        
    with col2:
        st.text('Proporsi Jumlah Sepeda Sewa Berdasarkan Suhu Terasa')
        fig, ax = plt.subplots(figsize=(16, 8))
        col_atemp = ["#D3D3D3", "Lime","#A0F55D"]
        explode = (0, 0.05, 0)
        ax.pie(atemp_df['cnt'], labels = atemp_df['atemp'],
               autopct=lambda pct5: f'{pct5:.1f}%',
               startangle=90, colors = col_atemp, explode = explode,
               wedgeprops={'linewidth': 1, 'edgecolor': 'black'}, textprops={'fontsize': 14})
        st.pyplot(fig)

        with st.expander("See explanation"):
            st.write(
                """Suhu Terasa (Apparent Temperature) mengacu pada bagaimana manusia merasakan suhu udara, dimana 
                hal ini dipengaruhi oleh faktor - faktor seperti kelembapan dan kecepatan angin. Berdasarkan pie chart di atas,
                para penyewa sepeda dominan berada pada suhu yang bagus untuk tubuh mereka saat bersepeda.
            """)
    
    ### Menampilkan Jumlah Sepeda yang Disewa Berdasarkan Cuaca
    st.subheader("Bagaimana Jumlah Sepeda Sewa Berdasarkan Cuaca?")
    lainnya = weather_df.iloc[-2:]
    lainnya_sum = lainnya['Jumlah Sepeda Total'].sum()
    lainnya_df = pd.DataFrame({'Cuaca': ['Lainnya'], 'Jumlah Sepeda Total': [lainnya_sum]})

    utama = weather_df.iloc[:-2].copy()
    utama = pd.concat([utama, lainnya_df], ignore_index=True)

    fig, ax = plt.subplots(figsize=(16, 8))
    colors_weather = ["Lime", "#D3D3D3", "#D3D3D3"]
    sns.barplot(y = 'Jumlah Sepeda Total',
                x = 'Cuaca',
                data = utama,
                palette = colors_weather,
                ax = ax)
    ax.set_title("Jumlah Sepeda Sewa Berdasarkan Cuaca", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    st.pyplot(fig)

    with st.expander("See explanation"):
        st.write(
            """Berdasarkan plot di atas, para penyewa sepeda dominan melakukan aktivitas penyewaan sepeda dan bersepeda
            pada saat cuaca cerah dan berawan, lalu diikuti cuaca berkabut. Lainnya di sini adalah saat cuaca hujan atau hujan salju,
            hingga hujan lebat.
            """)













































         

