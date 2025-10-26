import os
import json
import datetime
from flask import Flask, render_template, request, jsonify

# --- PDF Oluşturma Kütüphaneleri ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm # Milimetre birimini ekledik
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- Flask Sunucusunu Başlat ---
app = Flask(__name__)

# --- ÇIKARTMA KAĞIDI ÖLÇÜLERİ (Google Docs'tan gelen) ---
# 1 inç = 25.4 mm
TOP_MARGIN = 0.24 * 25.4 * mm        # A) Üst Boşluk
LEFT_MARGIN = 0.18 * 25.4 * mm       # B) Sol Boşluk
ETIKET_GENISLIK = 3.902 * 25.4 * mm  # C) Etiket Genişliği
ETIKET_YUKSEKLIK = 2.244 * 25.4 * mm # D) Etiket Yüksekliği
HORIZONTAL_GUTTER = 0 * mm           # E) Yatay Boşluk
VERTICAL_GUTTER = 0 * mm             # F) Dikey Boşluk

# --- Türkçe Fontları Kaydet ---
try:
    pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
except:
    print("UYARI: Arial fontları bulunamadı. Yazılar farklı görünebilir.")

# --- PDF ETİKET OLUŞTURMA FONKSİYONU ---

def create_labels_pdf(spice_name, page_count):
    pdf_file_name = "etiket.pdf"
    
    # Tarihleri hesapla
    today = datetime.date.today()
    uret_tarihi = today.strftime("%d.%m.%Y")
    # Son kullanma tarihini 2 yıl sonrası olarak ayarla
    stt_tarihi = (today.replace(year=today.year + 2)).strftime("%d.%m.%Y")
    parti_no = uret_tarihi.replace(".", "") # Parti No: GÜNAYYIL

    PAGE_W, PAGE_H = A4
    c = canvas.Canvas(pdf_file_name, pagesize=A4)
    
    # --- TEK BİR ETİKETİ ÇİZEN FONKSİYON (Güncellendi) ---
    def draw_single_label(x_base, y_base, genislik, yukseklik, baharat_adi):
        # x_base ve y_base, etiketin SOL ALT köşesinin koordinatlarıdır
        # Tüm içerik bu sınırlar içinde ortalanacak
        
        x_center = x_base + genislik / 2
        
        # --- 1. LOGO ---
        # !!! DİKKAT !!! logonuzun adını buraya yazın (logo.png veya logo.jpg)
        logo_path = "logo.png" 
        LOGO_GENISLIK = 40 * mm # Logonuzun enini ayarlayın
        LOGO_YUKSEKLIK = 25 * mm # Logonuzun boyunu ayarlayın
        
        try:
            logo = ImageReader(logo_path)
            # Y konumu: Etiketin üstünden (y_base + yukseklik) başla, 5mm boşluk bırak, logoyu çiz
            y_logo_start = y_base + yukseklik - 5*mm - LOGO_YUKSEKLIK
            x_logo_start = x_center - (LOGO_GENISLIK / 2)
            c.drawImage(logo, x_logo_start, y_logo_start, width=LOGO_GENISLIK, height=LOGO_YUKSEKLIK, mask='auto')
            
            # Bir sonraki metin için Y konumunu ayarla
            y_next_line = y_logo_start - 6*mm # Logonun 6mm altı
        except:
            y_next_line = y_base + yukseklik - 10*mm # En üstten 10mm aşağı
            c.setFont('Arial', 8)
            c.drawCentredString(x_center, y_next_line, "[LOGO YOK - logo.png ekleyin]")
            y_next_line -= 8*mm

        # --- 2. BAHARAT ADI (Dinamik) ---
        c.setFont('Arial-Bold', 14) # Kalın
        c.drawCentredString(x_center, y_next_line, baharat_adi)
        y_next_line -= 8*mm # Adın 8mm altı

        # --- 3. ALT BİLGİLER (Tarihler vs.) ---
        c.setFont('Arial', 8) # Daha küçük font
        
        # 1. Satır: ÜRT.TARİHİ (Ortalı)
        c.drawCentredString(x_center, y_next_line, f"ÜRT.TARİHİ: {uret_tarihi}")
        y_next_line -= 4*mm # 4mm altı

        # 2. Satır: Firma Bilgisi (Ortalı)
        # !!! DİKKAT !!! Resimdeki gibi kendi bilgilerinizi buraya girin
        c.drawCentredString(x_center, y_next_line, "LİDER BAHARAT yücel kaynak petroliş mh refah sk no 16")
        y_next_line -= 4*mm
        c.drawCentredString(x_center, y_next_line, "kartal İŞLETME NO TR-34-K-257496")
        y_next_line -= 6*mm # Biraz daha boşluk

        # 3. Satır: S.T.T ve PARTİ NO (İki Yana Yaslı)
        # Sol ve sağ için hizalama noktaları
        x_sol_nokta = x_base + 10*mm # Etiketin solundan 10mm içeride
        x_sag_nokta = x_base + genislik - 10*mm # Etiketin sağından 10mm içeride
        
        c.drawString(x_sol_nokta, y_next_line, f"S.T.T {stt_tarihi}")
        c.drawRightString(x_sag_nokta, y_next_line, f"PARTİ NO: {parti_no}")

    # --- ANA DÖNGÜ: Sayfaları ve Etiketleri Oluştur (Güncellendi) ---
    for _ in range(page_count):
        
        # 2 Sütun (Sütun 0, Sütun 1)
        for col in range(2):
            # Sütunun sol kenarını HESAPLA
            x = LEFT_MARGIN + col * (ETIKET_GENISLIK + HORIZONTAL_GUTTER)
            
            # 5 Satır (Satır 0, Satır 1, ..., Satır 4)
            for row in range(5):
                # Y koordinatını HESAPLA (ReportLab alttan başlar)
                y = (PAGE_H - TOP_MARGIN - ETIKET_YUKSEKLIK) - row * (ETIKET_YUKSEKLIK + VERTICAL_GUTTER)
                
                # Etiketi tam bu koordinatlara çiz
                draw_single_label(x, y, ETIKET_GENISLIK, ETIKET_YUKSEKLIK, spice_name)
        
        c.showPage() # Yeni sayfaya geç
        
    # PDF dosyasını kaydet
    c.save()
    print(f"'{pdf_file_name}' oluşturuldu.")


# --- 1. Baharat verisini yükle (Aynı kaldı) ---
try:
    with open('baharatlar.json', 'r', encoding='utf-8') as f:
        baharat_listesi = json.load(f)
except:
    baharat_listesi = [{"ad": "HATA: baharatlar.json dosyası bulunamadı"}]

# --- 2. Ana web sayfasını sun (Aynı kaldı) ---
@app.route('/')
def index():
    return render_template('index.html', baharatlar=baharat_listesi)

# --- 3. Yazdırma isteğini karşıla (Aynı kaldı) ---
@app.route('/print', methods=['POST'])
def handle_print():
    try:
        data = request.json
        spice_name = data.get('spice')
        page_count = int(data.get('pages', 1))

        if not spice_name:
            return jsonify({"success": False, "message": "Baharat adı seçilmedi."}), 400

        print(f"İstek alındı: {spice_name}, {page_count} sayfa")

        # 4. Etiket PDF'ini oluştur
        create_labels_pdf(spice_name, page_count)
        
        # 5. Oluşturulan PDF'i YAZDIR
        os.startfile("etiket.pdf", "print")

        return jsonify({"success": True, "message": "Yazdırılıyor..."})
    
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

# --- Sunucuyu Başlat (Aynı kaldı) ---
if __name__ == '__main__':
    print("Sunucu başlatılıyor... http://127.0.0.1:5000")
    print("Telefondan erişim için bilgisayarınızın IP adresini kullanın.")
    app.run(host='0.0.0.0', port=5000)
