import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import time
from sklearn.linear_model import LinearRegression # Tahminleme için
import numpy as np

# 1. Sayfa Ayarları
st.set_page_config(page_title="Yapay Zeka Destekli Stok Paneli", layout="wide")

# 2. Veri Çekme (Şifre: 12345)
def veri_getir():
    try:
        conn = psycopg2.connect(dbname="stok_takip_db", user="postgres", password="12345", host="localhost")
        df = pd.read_sql_query("SELECT * FROM satislar", conn)
        conn.close()
        # Tarih sütununu Python'ın anlayacağı gerçek zaman formatına çevirelim
        df['tarih'] = pd.to_datetime(df['tarih'])
        return df
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return None

# --- ML TAHMİN MOTORU ---
def satis_tahmini_yap(df):
    """Basit bir Doğrusal Regresyon ile trend tahmini yapar."""
    # Verileri dakikalık bazda gruplayıp satış sayılarını alalım
    df['dakika'] = df['tarih'].dt.floor('min')
    satis_trend = df.groupby('dakika').size().reset_index(name='satis_sayisi')
    
    # Zamanı sayısal bir değere çevirelim (Modelin anlayabilmesi için)
    satis_trend['zaman_indeksi'] = np.arange(len(satis_trend))
    
    X = satis_trend[['zaman_indeksi']] # Girdi (Zaman)
    y = satis_trend['satis_sayisi']     # Çıktı (Satış Miktarı)
    
    # Modeli Eğitme
    model = LinearRegression()
    model.fit(X, y)
    
    # Gelecekteki bir sonraki dakika için tahmin yap
    gelecek_zaman = np.array([[len(satis_trend)]])
    tahmin = model.predict(gelecek_zaman)[0]
    
    return round(max(0, tahmin), 2)

# --- ARAYÜZ ---
st.title("🤖 Yapay Zeka Destekli Stok Paneli")

df = veri_getir()

if df is not None and not df.empty:
    # Tahmin Hesapla
    gelecek_tahmini = satis_tahmini_yap(df)
    
    # Üst Metrikler
    m1, m2, m3 = st.columns(3)
    m1.metric("💰 Toplam Ciro", f"{df['fiyat'].sum():,.2f} TL")
    m2.metric("📦 Toplam İşlem", len(df))
    # ML Tahminini Gösterelim
    m3.metric("🔮 Gelecek Tahmini", f"~ {gelecek_tahmini} Satış/Dk", delta="Yapay Zeka Analizi")

    st.info(f"💡 **AI Notu:** Şu anki satış hızına göre, önümüzdeki 1 dakika içinde yaklaşık {gelecek_tahmini} adet yeni işlem bekleniyor.")

    # Grafik: Satış Trendi (Zaman Serisi)
    st.subheader("📈 Gerçek Zamanlı Satış Trendi ve Tahminleme")
    df['dakika'] = df['tarih'].dt.floor('min')
    trend_data = df.groupby('dakika').size().reset_index(name='Satis')
    fig = px.line(trend_data, x='dakika', y='Satis', title="Dakikalık Satış Hızı", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Önceki grafiklerini buraya eklemeye devam edebilirsin...
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏆 Ürün Bazlı Durum")
        st.bar_chart(df['urun'].value_counts())

# Yenileme
time.sleep(5)
st.rerun()