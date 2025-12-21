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
│   STT:           [10/2027      ]    │
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
- 📁 Çoklu dosya yükleme

</td>
<td width="50%">

### 🔧 Güçlü Özellikler
- 🖨️ Direkt yazıcı entegrasyonu
- 📅 Otomatik STT hesaplama
- 🎨 Özelleştirilebilir tasarım
- 💾 JSON tabanlı veri yönetimi
- 🤖 Otomatik toplu yazdırma

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
Python 3.7+
pip (Python package manager)
```

### ⚡ Kurulum

```bash
# 1. Repoyu klonlayın
git clone https://github.com/ErenKaynak/Label-System.git
cd Label-System

# 2. Gerekli paketleri yükleyin
pip install flask reportlab

# 3. Logo dosyasını ekleyin (isteğe bağlı)
# logo.png dosyasını proje kök dizinine yerleştirin

# 4. Uygulamayı başlatın
python app.py
```

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

```plaintext
1. Baharat türünü seçin (örn: TOZ BİBER)
2. Gramajı seçin (örn: 1 KG)
3. Sayfa sayısını girin (her sayfa = 10 etiket)
4. Son tüketim tarihini seçin
5. "SEPETE EKLE" butonuna tıklayın
```

### 2️⃣ Toplu Yazdırma

```plaintext
1. Sepete birden fazla ürün ekleyin
2. "TÜMÜNÜ YAZDIR" butonuna tıklayın
3. PDF otomatik olarak yazıcıya gönderilir
```

### 3️⃣ Yeni Ürün Ekleme

```plaintext
1. Sayfanın altındaki "Listeyi Düzenle" bölümünü açın
2. Yeni baharat adını veya gramajı girin
3. "Ekle" butonuna tıklayın
4. Sayfa otomatik yenilenir
```

### 4️⃣ Resim/PDF Yükleme ve Otomatik Yazdırma

```plaintext
1. "📁 Resim/PDF Yükle ve Yazdır" bölümünden dosya seçin
2. Galeri veya dosya seçicide birden fazla dosya seçebilirsiniz
3. "YÜKLE" butonuna tıklayın
4. Dosyalar yazdırma kuyruğuna eklenir
5. "TÜMÜNÜ OTOMATIK YAZDIR" ile hepsi otomatik yazdırılır
6. Desteklenen formatlar: PDF, PNG, JPG, JPEG, GIF, BMP
7. Maksimum dosya boyutu: 16MB
```

> 💡 **Detaylı bilgi için**: [UPLOAD_FEATURE.md](UPLOAD_FEATURE.md) dosyasına bakın.

---

## 📦 Etiket Tasarımı

### 🎨 Etiket İçeriği

<table>
<tr>
<td width="30%"><b>Bölüm</b></td>
<td width="40%"><b>İçerik</b></td>
<td width="30%"><b>Font</b></td>
</tr>
<tr>
<td>🖼️ Logo</td>
<td>Firma logosu (90x30mm)</td>
<td>-</td>
</tr>
<tr>
<td>📝 Ürün Adı</td>
<td>Baharat + Gramaj</td>
<td>Arial Bold 12pt</td>
</tr>
<tr>
<td>📅 STT</td>
<td>MM / YYYY</td>
<td>Arial 9pt</td>
</tr>
<tr>
<td>🏷️ Parti No</td>
<td>Sabit metin</td>
<td>Arial 8pt</td>
</tr>
<tr>
<td>🏢 İşletme No</td>
<td>TR-XX-X-XXXXXX</td>
<td>Arial 8pt</td>
</tr>
<tr>
<td>📍 Adres</td>
<td>Firma adresi</td>
<td>Arial 8pt</td>
</tr>
</table>

### 📐 Teknik Özellikler

```plaintext
├─ Sayfa Formatı: A4 (210 x 297 mm)
├─ Etiket Düzeni: 2 sütun × 5 satır
├─ Toplam Etiket: 10 etiket/sayfa
├─ Etiket Boyutu: 105 × 59.4 mm
├─ Marj: 0 mm
└─ Logo Boyutu: 90 × 30 mm
```

---

## 🗂️ Proje Yapısı

```
Label-System/
│
├── 📄 app.py                    # Ana Flask uygulaması
├── 📊 baharatlar.json          # Ürün veritabanı
├── 🖼️ logo.png                 # Firma logosu
├── 📄 etiket.pdf               # Oluşturulan PDF (otomatik)
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
| `/print-cart` | POST | Sepeti yazdır | `cart`, `date` |
| `/add-spice` | POST | Yeni baharat ekle | `spice_name` |
| `/add-weight` | POST | Yeni gramaj ekle | `weight_name` |
| `/upload-files` | POST | Dosya yükle (çoklu) | `files[]` |
| `/get-upload-queue` | GET | Yükleme kuyruğunu getir | - |
| `/remove-from-queue` | POST | Kuyruktan dosya sil | `index` |
| `/print-all-uploads` | POST | Tüm yüklemeleri yazdır | - |
| `/manifest.json` | GET | PWA manifest | - |
| `/static/<path>` | GET | Statik dosyalar | - |

### 📤 Örnek POST Request

```javascript
// Sepeti yazdır
fetch('/print-cart', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    cart: [
      { label: "TOZ BİBER    1 KG", pages: 2 }
    ],
    date: "2027-10"
  })
});

// Yeni baharat ekle
fetch('/add-spice', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    spice_name: "ZERDEÇAL"
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

`app.py` dosyasında aşağıdaki değişkenleri düzenleyerek etiket tasarımını özelleştirebilirsiniz:

```python
# Sayfa ayarları
PAGE_W, PAGE_H = A4
TOP_MARGIN = 0 * mm
LEFT_MARGIN = 0 * mm

# Etiket boyutları
ETIKET_GENISLIK = PAGE_W / 2
ETIKET_YUKSEKLIK = PAGE_H / 5

# Logo boyutları
LOGO_GENISLIK = 90 * mm
LOGO_YUKSEKLIK = 30 * mm
```

---

## 🐛 Sorun Giderme

<details>
<summary><b>❌ "Arial fontları bulunamadı" hatası</b></summary>

**Çözüm (Windows):**
```python
# app.py içinde zaten doğru yol tanımlı
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
```

**Çözüm (Linux/Mac):**
```python
# Font yolunu sistem fontlarınıza göre güncelleyin
pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'))
```
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
- ✅ Varsayılan PDF görüntüleyici tanımlı mı?
- ✅ Yazıcı bağlantısı aktif mi?
- ✅ Windows kullanıyorsunuz? (`os.startfile` sadece Windows'ta çalışır)

**Alternatif (Linux/Mac):**
```python
# app.py içinde os.startfile yerine:
import subprocess
subprocess.run(['lpr', PDF_FILE_NAME])  # Linux
subprocess.run(['open', '-a', 'Preview', PDF_FILE_NAME])  # Mac
```
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
