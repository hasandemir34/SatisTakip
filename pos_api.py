from flask import Flask, jsonify
import random
from datetime import datetime

app = Flask(__name__)

@app.route('/api/satis-yap', methods=['GET'])
def satis():
    urunler = ["Filtre Kahve", "Latte", "Cay", "Simit", "Kek"]
    secilen = random.choice(urunler)
    
    veri = {
        "islem_id": random.randint(1000, 9999),
        "urun": secilen,
        "fiyat": random.randint(20, 80),
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "odeme_tipi": random.choice(["Nakit", "Kredi Karti"])
    }
    return jsonify(veri)

if __name__ == '__main__':
    print("📢 Yazar Kasa (API) 5000 portunda çalışıyor...")
    app.run(port=5000)