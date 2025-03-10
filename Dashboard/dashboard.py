import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

sns.set(style='dark')

# Menyiapkan monthlys_df
def create_monthly_df(ds_df):
    monthly_df = ds_df.resample(rule = 'ME', on = 'dteday').agg({
        'casual': ['min', 'max', 'sum', 'mean'],
        'registered': ['min', 'max', 'sum', 'mean'],
        'cnt': ['min', 'max', 'sum', 'mean']}).reset_index()

    monthly_df['dteday'] = monthly_df['dteday'].dt.to_period('M').astype(str)

    return monthly_df

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
    
    daily_df['dteday'] = pd.to_datetime(daily_df['dteday'])

    return daily_df

# Menyiapkan monthly2011_df
def create_monthly2011_df(m_df):
    monthly2011_df = m_df[m_df['dteday'].str.startswith('2011')]

    return monthly2011_df

# Menyiapkan monthly2012_df
def create_monthly2012_df(m_df):
    monthly2012_df = m_df[m_df['dteday'].str.startswith('2012')]

    return monthly2012_df

# Menyiapkan timecat_df
def create_timecat_df(h_df):
    timecat_df = h_df.groupby([
    h_df['hr'].apply(lambda j: 'Pagi Buta' if j <= 5 else 'Pagi' if j <= 10 else 'Siang' if j <= 15 else 'Sore' if j <= 19 else 'Malam')
    ])[['casual','registered','cnt']].mean().reset_index()

    return timecat_df

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
def create_weather_df(d_df):
    weather_df = (d_df.groupby('weathersit')[['casual',
                                            'registered','cnt']].sum().reset_index().assign(weathersit = lambda w: w['weathersit'].map({
                                  1: 'Clear/cloudy',
                                  2: 'Mist',
                                  3: 'Light snow/rain'
                              })).rename(columns = {
                                  'weathersit': 'Cuaca',
                                  'casual': 'Jumlah Pengguna Casual',
                                  'registered': 'Jumlah Pengguna Registered',
                                  'cnt': 'Jumlah Sepeda Total'})).sort_values(by = ['Jumlah Sepeda Total'], ascending=False)

    return weather_df

# Load berkas
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Untuk melihat jumlah sepeda sewa tertinggi setiap tahunnya (tidak menggunakan filtering)
daystack_df = day_df
monthly_df = create_monthly_df(daystack_df)
monthly2011_df = create_monthly2011_df(monthly_df)
monthly2012_df = create_monthly2012_df(monthly_df)

# Membuat Komponen Filter
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar:
    st.subheader("Informasi Detail Menurut Rentang Waktu")

    start_date, end_date = st.date_input(
        label = 'Rentang Waktu', min_value = min_date,
        max_value = max_date, value = [min_date, max_date])

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

day_df = day_df[(day_df['dteday'] >= start_date) &
                (day_df['dteday'] <= end_date)]


# Menghasilkan dataframe untuk visualisasi
comptype_df = create_comptype_df(day_df)
daily_df = create_daily_df(day_df)
timecat_df = create_timecat_df(hour_df)
temp_df = create_temp_df(day_df)
atemp_df = create_atemp_df(day_df)
hum_df = create_hum_df(day_df)
wind_df = create_wind_df(day_df)
weather_df = create_weather_df(day_df)

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
        daily_df["dteday"],
        daily_df["cnt"],
        marker='o', 
        markersize=3,
        linewidth=2,
        color="Green",
        linestyle="-")
    
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    
    st.pyplot(fig)
    
    with st.expander("See explanation"):
        st.write(
            """Jumlah sepeda yang disewa oleh sistem Bike Central Share mengalami fluktuatif, 
            yakni meningkat pada semester pertama dan menurun di semester kedua, 
            lalu meningkat lagi pada semester pertama di tahun berikutnya dan menurun lagi di semester berikutnya.
            Terlihat bahwa jumlah sepeda yang disewa terendah berada pada akhir tahun 2011 hingga awal tahun 2012.
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
        sns.barplot(y = monthly2011_df['cnt']['sum'],
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
        sns.barplot(y = monthly2012_df['cnt']['sum'],
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


with tab3:
    ## Informasi Jumlah Sepeda yang Disewa pada Berbagai Kondisi
    ### Menampilkan Jumlah Sepeda yang Disewa Berdasarkan Humidity dan Windspeed
    
    st.subheader('Jumlah Sepeda Sewa Berdasarkan Tingkat Kelembaman dan Kecepatan Angin')

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

    col_hum = ["Lime", "#ACF771", "#D3D3D3"]
    col_wind = ["Lime", "#ACF771", "#D3D3D3"]

    sns.barplot(
        y = 'cnt',
        x = 'hum',
        data = hum_df.sort_values(by = 'cnt', ascending = False),
        palette = col_hum,
        ax = ax[0]
    )
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Jumlah Sepeda Sewa Berdasarkan Tingkat Kelembaman", loc="center", fontsize=25)
    ax[0].tick_params(axis='y', labelsize=25)
    ax[0].tick_params(axis='x', labelsize=25)
    ax[0].yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
        
    sns.barplot(
        y = 'cnt',
        x = 'windspeed',
        data = wind_df.sort_values(by = 'cnt', ascending = False),
        palette = col_wind,
        ax = ax[1]
    )
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("Jumlah Sepeda Sewa Berdasarkan Kecepatan Angin", loc="center", fontsize=25)
    ax[1].tick_params(axis='y', labelsize=25)
    ax[1].tick_params(axis='x', labelsize=25)
    ax[1].yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

    st.pyplot(fig)
    
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("See explanation"):
            st.write(
                """Berdasarkan pie chart di atas, banyak sepeda yang justru disewa pada saat tingkat kelembamannya tinggi (high). 
                Artinya, banyak penyewa sepeda yang justru bersepeda pada saat tingkat kelembamannya tersebut.
                Meskipun tidak jauh berbeda proporsinya dengan tingkat kelembaman moderate, hal tersebut perlu diperhatikan mengingat banyak efek
                samping yang dapat timbul akibat beraktivitas di tingkat kelembaman tinggi.
                """)

    with col2:
        with st.expander("See explanation"):
            st.write(
                """Berdasarkan pie chart di atas, banyak sepeda yang disewa dan digunakan pada tingkat kecepatan angin yang rendah (low), 
                disusul oleh tingkat kecepatan angin moderate, dan sangat sedikit pada saat tingkat kecepatan anginnya tinggi (high).
                """)
    
    ### Menampilkan Jumlah Sepeda yang Disewa Berdasarkan Suhu

    st.subheader('Jumlah Sepeda Sewa Berdasarkan Suhu')

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

    col_temp = ["Lime", "#ACF771" ,"#ACF771", "#D3D3D3"]
    col_atemp = ["Lime", "#ACF771", "#D3D3D3"]

    sns.barplot(
        y = 'cnt',
        x = 'temp',
        data = temp_df.sort_values(by = 'cnt', ascending = False),
        palette = col_temp,
        ax = ax[0]
    )
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Jumlah Sepeda Sewa Berdasarkan Suhu Aktual", loc="center", fontsize=25)
    ax[0].tick_params(axis='y', labelsize=25)
    ax[0].tick_params(axis='x', labelsize=25)
    ax[0].yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
        
    sns.barplot(
        y = 'cnt',
        x = 'atemp',
        data = atemp_df.sort_values(by = 'cnt', ascending = False),
        palette = col_atemp,
        ax = ax[1]
    )
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("Jumlah Sepeda Sewa Berdasarkan Suhu Terasa", loc="center", fontsize=25)
    ax[1].tick_params(axis='y', labelsize=25)
    ax[1].tick_params(axis='x', labelsize=25)
    ax[1].yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

    st.pyplot(fig)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("See explanation"):
            st.write(
                """Para penyewa sepeda cenderung bersepeda pada saat suhu aktual atau suhu udara di sekitarnya hangat, 
                diikuti suhu udara dingin dan panas. Suhu udara hangat cenderung dapat dirasakan pada saat sore hari, 
                dimana waktu tersebut adalah waktu dominan para penyewa sepeda mulai beraktivitas dengan sepedanya.
            """)
        
    with col2:
        with st.expander("See explanation"):
            st.write(
                """Suhu Terasa (Apparent Temperature) mengacu pada bagaimana manusia merasakan suhu udara, dimana 
                hal ini dipengaruhi oleh faktor - faktor seperti kelembapan dan kecepatan angin. Berdasarkan info yang tertera,
                para penyewa sepeda dominan berada pada suhu yang bagus untuk tubuh mereka saat bersepeda.
            """)
    
    ### Menampilkan Jumlah Sepeda yang Disewa Berdasarkan Cuaca
    st.subheader("Bagaimana Jumlah Sepeda Sewa Berdasarkan Cuaca?")
    fig, ax = plt.subplots(figsize=(16, 8))
    colors_weather = ["Lime", "#D3D3D3", "#D3D3D3"]
    sns.barplot(y = 'Jumlah Sepeda Total',
                x = 'Cuaca',
                data = weather_df,
                palette = colors_weather,
                ax = ax)
    ax.set_title("Jumlah Sepeda Sewa Berdasarkan Cuaca", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=25)
    ax.tick_params(axis='y', labelsize=25)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    st.pyplot(fig)

    with st.expander("See explanation"):
        st.write(
            """Berdasarkan plot di atas, para penyewa sepeda dominan melakukan aktivitas penyewaan sepeda dan bersepeda
            pada saat cuaca cerah dan berawan, lalu diikuti cuaca berkabut.
            """)













































         

