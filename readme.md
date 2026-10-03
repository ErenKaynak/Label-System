<div align="center">

# 🏷️ Label System

### Profesyonel Baharat Etiket Yazdırma Sistemi

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![PWA](https://img.shields.io/badge/PWA-5A0FC8?style=for-the-badge&logo=pwa&logoColor=white)](https://web.dev/progressive-web-apps/)

**Flask tabanlı modern web uygulaması ile A4 çıkartma kağıdına profesyonel etiket yazdırma çözümü**

[Özellikler](#-özellikler) • [Kurulum](#-kurulum) • [Kullanım](#-kullanım) • [Katkıda Bulun](#-katkıda-bulunma)

<img src="https://img.shields.io/github/stars/ErenKaynak/Label-System?style=social" alt="GitHub stars">
<img src="https://img.shields.io/github/forks/ErenKaynak/Label-System?style=social" alt="GitHub forks">
<img src="https://img.shields.io/github/license/ErenKaynak/Label-System" alt="License">

</div>

---

## 📸 Ekran Görüntüleri

```
┌─────────────────────────────────────┐
│   🏷️  Etiket Sistemi                │
│─────────────────────────────────────│
│   Baharat Seçin: [TOZ BİBER    ▼]   │
│   Gramaj Seçin:  [1 KG         ▼]   │
│   Sayfa Sayısı:  [1            ]    │
│   TETT:          [09.2027     ]    │
│                                     │
│   [      SEPETE EKLE      ]         │
│─────────────────────────────────────│
│   📋 Yazdırma Sepeti                │
│   • TOZ BİBER 1KG (2 sayfa)   [Sil] │
│   • KİMYON 500GR (1 sayfa)    [Sil] │
│                                     │
│    [    TÜMÜNÜ YAZDIR    ]          │
└─────────────────────────────────────┘
```

---

## ✨ Özellikler

<table>
<tr>
<td width="50%">

### 🎯 Kullanıcı Dostu
- ✅ Sezgisel arayüz tasarımı
- 🛒 Akıllı sepet sistemi
- 📱 Mobil uyumlu (PWA)
- ⚡ Hızlı etiket oluşturma

</td>
<td width="50%">

### 🔧 Güçlü Özellikler
- 🖨️ Direkt yazıcı entegrasyonu
- 📅 Ay/yıl TETT; aynı tarih otomatik parti/lot numarası
- 🎨 Özelleştirilebilir tasarım
- 💾 JSON tabanlı veri yönetimi

</td>
</tr>
</table>

---

## 🛠️ Kullanılan Teknolojiler

### Backend
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF-red?style=for-the-badge)

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)

### Araçlar
![JSON](https://img.shields.io/badge/JSON-5E5C5C?style=for-the-badge&logo=json&logoColor=white)
![Git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

---

## 🚀 Hızlı Başlangıç

### 📋 Gereksinimler

```bash
Python 3.9+
pip (Python package manager)
```

### ⚡ Windows kurulumu

Proje klasörünün tamamını Windows bilgisayara kopyalayın. Python 3.9 veya üstünü yükleyin. İlk kullanımda `kurulum.bat` dosyasına çift tıklayın; bu dosya `.venv` klasörünü oluşturup `requirements.txt` içindeki paketleri kurar. Daha sonra `baslat.bat` dosyasına çift tıklayın ve tarayıcıda `http://127.0.0.1:5000/` adresini açın. Başlatma dosyası kurulum eksikse kurulumu kendisi de başlatır. Sunucu çalışırken açılan komut penceresini kapatmayın.

Kurulum için internet bağlantısı gerekir. `.venv` klasörünü bir bilgisayardan diğerine taşımayın; her Windows bilgisayarda yeniden oluşturun. Daha önce kaydedilmiş işletme bilgilerini de taşımak istiyorsanız `isletme.json` dosyasını proje klasörüyle birlikte kopyalayın.

### ⚡ macOS / Linux kurulumu

```bash
# 1. Repoyu klonlayın
git clone https://github.com/ErenKaynak/Label-System.git
cd Label-System

# 2. Gerekli paketleri yükleyin
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# 3. Uygulamayı başlatın
.venv/bin/python app.py
```

macOS'te 5000 portu doluysa `PORT=5001 .venv/bin/python app.py` komutunu kullanın ve `http://localhost:5001` adresini açın.

### 🌐 Erişim

**Bilgisayardan:**
```
http://localhost:5000
```

**Mobil Cihazlardan:**
```
http://[BİLGİSAYAR-ADI].local:5000
```

> 💡 **İpucu:** Bilgisayar adınızı öğrenmek için terminalde `hostname` komutunu çalıştırın.

---

## 📱 Kullanım Kılavuzu

### 1️⃣ Etiket Oluşturma

1. Etiket düzenini seçin: yatay 148,5 × 42 mm, dikey 59,4 × 105 mm veya önceki 105 × 59,4 mm düzen.
2. Baharat, net miktar ve sayfa sayısını seçin.
3. İçindekiler, alerjen ve menşe bilgilerini gerçek ürüne göre doldurup doğrulayın. Muhafaza koşulu otomatik gelir; ürüne uymuyorsa düzeltin.
4. Her ürünün TETT ayını ve yılını seçin. Aynı tarih etikette parti/lot numarası olarak kullanılır.
5. İşletmeci adı, tam adresi ve kayıt numarasını bir kez girip **İşletme bilgilerini kaydet** düğmesine basın. Sonraki açılışlarda alanlar otomatik dolar.
6. Sepete ekleyin; PDF önizlemesini kontrol ettikten sonra yazdırın.

### 2️⃣ Toplu Yazdırma

```plaintext
1. Sepete birden fazla ürün ekleyin
2. "PDF ÖNİZLEME İNDİR" ile sayfayı kontrol edin
3. "TÜMÜNÜ YAZDIR" butonuna tıklayın
4. PDF varsayılan yazıcıya gönderilir
```

### 3️⃣ Yeni Ürün Ekleme

```plaintext
1. Sayfanın altındaki "Listeyi Düzenle" bölümünü açın
2. Yeni baharat adını veya gramajı girin
3. "Ekle" butonuna tıklayın
4. Sayfa otomatik yenilenir
```

---

## 📦 Etiket Tasarımı ve mevzuat

A4 üzerinde 2 sütun × 5 satır vardır. Yatay etiket **148,5 × 42 mm** ölçüsündedir. Dikey etiket, A4 dikey sayfadaki 105 × 59,4 mm hücrenin içeriği 90° döndürülerek **59,4 × 105 mm** yönünde okunur. Önceki yatay içerikli A4 dikey düzen de korunur. `logo.png` dikey etikette yazıların üstüne, yatay etikette geniş bir sol alana otomatik yerleştirilir. İçerikte 9 pt, başlıkta 10–13 pt gömülü Türkçe TrueType font kullanılır. Baskıyı **gerçek boyut / %100 ölçek** ile alın ve fiziksel boyutu ölçün. Zorunlu bilgilerin okunurluğu ve x-yüksekliği, gerçek baskıda da kontrol edilmelidir.

Etiket; ürün adı, net miktar, içindekiler, varsa alerjenler, menşe, muhafaza koşulu, TETT, parti/lot açıklaması, işletmeci adı ve adresi ile işletme kayıt numarasını içerir. TETT ay/yıl biçiminde basılır ve aynı tarih parti/lot işareti sayılır; etikette “Parti/lot numarası, tavsiye edilen tüketim tarihidir.” açıklaması yer alır. **Aynı TETT tarihini taşıyan farklı üretim partileri varsa yalnızca tarih bunları ayırt etmez.** Bu durumda gerçek üretim kayıtlarına uygun ayrı bir parti kodu ve etiket düzeni gerekir. İşletme bilgileri yalnızca bu bilgisayardaki `isletme.json` dosyasına kaydedilir; dosya sürüm kontrolü dışında tutulur. Tek baharat ve baharat karışımlarında beslenme bildirimi istisnası olabilir; yağ/tuz gibi ekler bu durumu değiştirebilir. Kekikte gerçek cins adı ürün adı veya bileşen listesinde belirtilmelidir. Ürün reçeteleri ve raf ömrü internetten güvenilir biçimde belirlenemeyeceği için program yalnızca örnek içerik önerir ve doğrulama ister. Alerjen alanına yazılan ve içindekiler metninde geçen maddeler listede kalın gösterilir; özel ürün kuralları ve baskıdaki okunurluk ayrıca kontrol edilmelidir.

Başvurulan resmi kaynaklar:

- [TGK Gıda Etiketleme ve Tüketicileri Bilgilendirme Yönetmeliği](https://istanbul.tarimorman.gov.tr/Belgeler/SolMenu/RESM%C4%B0%20GAZETE/GidaEtiketlemeYonetmeligi.pdf)
- [TGK Baharat Tebliği 2022/7](https://sanliurfa.tarimorman.gov.tr/Duyuru/339/Turk-Gida-Kodeksi-Baharat-Tebligi-_teblig-No-2022_7_)
- [2026/11 parti/lot tebliği duyurusu](https://www.tarimorman.gov.tr/HHGM/Haber/221/Turk-Gida-Kodeksi-Gidalarin-Ait-Oldugu-Partiyi-Tanimlayan-Isaretler-Veya-Numaralar-Hakkinda-Teblig-_teblig-No2026_11_-Yayimlanmistir)
- [Bakanlık etiketleme açıklamaları](https://istanbul.tarimorman.gov.tr/Duyuru/465/Tgk-Etiketleme-Ve-Tuketicileri-Bilgilendirme-Yonetmeligi-Ve-Tgk-Etiketleme-Ve-Tuketicileri-Bilgilendirme-Yonetmeligi-Kilavuzunda-Yapilan-Degisikliklere-Iliskin-Aciklamalar)

### 🖨️ Baskı kontrolü

Önce PDF önizlemesini normal A4 kâğıda **gerçek boyut / %100 ölçek** ile yazdırın; "sayfaya sığdır" seçeneğini kapatın. Çıktıyı etiket kâğıdının üzerine koyup 2 × 5 kesim çizgileriyle hizayı ışığa tutarak kontrol edin. Fiziksel yazıcı payı ve etiket kâğıdının gerçek kesimi yazılım tarafından ölçülemez; seri baskıdan önce tek sayfalık deneme yapın.

macOS ve Linux'ta doğrudan yazdırma için sistemde varsayılan yazıcı tanımlı ve `lp` komutu kullanılabilir olmalıdır. Yazıcı tanımlı değilse uygulama hata gösterir; PDF önizlemesi yine indirilebilir.
Windows'ta doğrudan yazdırma, varsayılan PDF uygulamasının **Yazdır** komutunu desteklemesine bağlıdır. Bu komut çalışmazsa PDF önizlemesini indirip PDF uygulamasından A4 ve %100 ölçekte yazdırın.

---

## 🗂️ Proje Yapısı

```
Label-System/
│
├── 📄 app.py                    # Ana Flask uygulaması
├── 📄 requirements.txt          # Python paketleri
├── 📄 kurulum.bat               # Windows ilk kurulum
├── 📄 baslat.bat                # Windows başlatma
├── 📊 baharatlar.json          # Ürün veritabanı
├── 🖼️ logo.png                 # Etiketlerde kullanılan firma logosu
├── 📄 etiket.pdf               # Doğrudan yazdırmada oluşturulan PDF
│
├── 📁 Templates/
│   └── 🌐 index.html           # Ana web arayüzü
│
└── 📁 static/
    ├── 📋 manifest.json        # PWA manifest
    └── 📁 icons/               # PWA ikonları
        ├── icon-192.png
        └── icon-512.png
```

---

## 🔌 API Endpoints

| Endpoint | Method | Açıklama | Parametreler |
|----------|--------|----------|--------------|
| `/` | GET | Ana sayfa | - |
| `/save-business` | POST | Tek işletmenin bilgilerini yerel dosyaya kaydet | `operator`, `address`, `registration` |
| `/preview-cart` | POST | PDF indir | `cart`, `common`, `orientation` |
| `/print-cart` | POST | Sepeti yazdır | `cart`, `common`, `orientation` |
| `/add-spice` | POST | Yeni baharat ekle | `spice_name` |
| `/add-weight` | POST | Yeni gramaj ekle | `weight_name` |
| `/manifest.json` | GET | PWA manifest | - |
| `/static/<path>` | GET | Statik dosyalar | - |

### 📤 Örnek PDF isteği

```javascript
fetch('/preview-cart', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    orientation: 'landscape',
    common: {
      operator: 'İşletmeci adı', address: 'Tam adres',
      registration: 'TR-...'
    },
    cart: [{
      spice: 'KİMYON', weight: '500 GR', ingredients: 'Kimyon',
      allergens: '', origin: 'Türkiye',
      date: '2027-09', verified: true, pages: 1
    }]
  })
});
```

---

## ⚙️ Yapılandırma

### 📝 baharatlar.json

```json
{
  "baharatlar": [
    "TOZ BİBER",
    "KİMYON",
    "KARABİBER TANE",
    "NANE",
    "KEKİK",
    "PUL BİBER"
  ],
  "gramajlar": [
    "1 KG",
    "500 GR",
    "250 GR"
  ]
}
```

### 🎨 Etiket Özelleştirme

Sayfa yönü arayüzden seçilir. Ürün verileri baskı öncesinde arayüzden girilir. `baharatlar.json` yalnızca baharat ve gramaj seçeneklerini tutar.

---

## 🐛 Sorun Giderme

<details>
<summary><b>❌ "Font bulunamadı" hatası</b></summary>

Uygulama Windows ve macOS Arial fontlarını, Linux'ta Liberation Sans veya DejaVu Sans fontlarını otomatik arar. Bu font ailelerinden birini normal ve kalın dosyalarıyla kurup uygulamayı yeniden başlatın.
</details>

<details>
<summary><b>📱 Mobil cihazdan bağlanamıyorum</b></summary>

**Kontrol listesi:**
- ✅ Bilgisayar ve mobil cihaz aynı WiFi ağında mı?
- ✅ Windows Firewall 5000 portuna izin veriyor mu?
- ✅ Bilgisayar adını doğru yazdınız mı? (`hostname` komutu ile kontrol edin)

**Windows Firewall ayarı:**
```powershell
# PowerShell'i yönetici olarak açın
New-NetFirewallRule -DisplayName "Flask App" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```
</details>

<details>
<summary><b>🖨️ PDF yazdırma çalışmıyor</b></summary>

**Çözüm:**
- ✅ Yazıcı bağlantısı aktif mi?
- ✅ Yazıcı sistemde varsayılan olarak tanımlı mı?
- ✅ Baskı ayarında A4 ve %100 ölçek seçili mi?

**Linux/Mac:** `lpstat -p -d` komutuyla varsayılan yazıcıyı kontrol edin.
</details>

---

## 🔒 Güvenlik

- 🔐 **Thread-Safe:** JSON işlemleri `threading.Lock()` ile korunur
- 🛡️ **Input Validation:** Tüm kullanıcı girdileri doğrulanır
- 🚫 **SQL Injection:** JSON kullanıldığı için risk yoktur
- 🌐 **CORS:** Sadece aynı ağdan erişim

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! İşte nasıl katkıda bulunabilirsiniz:

1. 🍴 Bu repoyu **fork** edin
2. 🌿 Yeni bir **branch** oluşturun
   ```bash
   git checkout -b feature/harika-ozellik
   ```
3. 💾 Değişikliklerinizi **commit** edin
   ```bash
   git commit -m '✨ Harika özellik eklendi'
   ```
4. 📤 Branch'inizi **push** edin
   ```bash
   git push origin feature/harika-ozellik
   ```
5. 🎉 Bir **Pull Request** oluşturun

### 📝 Commit Mesajı Kuralları

```
✨ feat: Yeni özellik
🐛 fix: Hata düzeltme
📚 docs: Dokümantasyon
💄 style: Tasarım değişikliği
♻️ refactor: Kod iyileştirme
⚡ perf: Performans
✅ test: Test ekleme
🔧 chore: Yapılandırma
```

---

## 📊 Özellik Roadmap

- [x] Temel etiket yazdırma
- [x] PWA desteği
- [x] Sepet sistemi
- [x] Dinamik liste yönetimi
- [ ] 🚧 Çoklu dil desteği
- [ ] 🚧 Tema özelleştirme
- [ ] 🚧 Barkod entegrasyonu
- [ ] 🚧 Excel import/export
- [ ] 🚧 Kullanıcı giriş sistemi

---

## 👨‍💻 Geliştirici

<div align="center">

**Eren Kaynak**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ErenKaynak)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/erenkaynak)

</div>

---

## 💖 Teşekkürler

Bu projeyi kullandığınız için teşekkürler! Eğer beğendiyseniz ⭐ vermeyi unutmayın!

---

<div align="center">

**[⬆ Başa Dön](#-label-system)**

Made with ❤️ by [Eren Kaynak](https://github.com/ErenKaynak)

![Visitor Count](https://visitor-badge.laobi.icu/badge?page_id=ErenKaynak.Label-System)

</div>
