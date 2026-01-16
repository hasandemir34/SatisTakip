import requests
import psycopg2
import time

# Veritabanı bağlantı bilgilerini buraya giriyoruz
DB_AYAR = "dbname=stok_takip_db user=postgres password=12345 host=localhost"

def kaydet(satis):
    try:
        conn = psycopg2.connect(DB_AYAR)
        cur = conn.cursor()
        cur.execute("INSERT INTO satislar (islem_id, urun, fiyat, tarih, odeme_tipi) VALUES (%s, %s, %s, %s, %s)",
                    (satis['islem_id'], satis['urun'], satis['fiyat'], satis['tarih'], satis['odeme_tipi']))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Veritabanı Hatası: {e}")
        return False

print("🚀 Veri Avcısı çalışıyor, satışlar toplanıyor...")
while True:
    try:
        r = requests.get("http://127.0.0.1:5000/api/satis-yap")
        if r.status_code == 200:
            veri = r.json()
            if kaydet(veri):
                print(f"✅ Kaydedildi: {veri['urun']} - {veri['fiyat']} TL")
        time.sleep(5) # 5 saniyede bir veri çeker
    except Exception as e:
        print(f"❌ API'ye ulaşılamıyor: {e}")
        time.sleep(10)