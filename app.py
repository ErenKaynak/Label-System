import os
import json
import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory

# --- PDF Oluşturma Kütüphaneleri ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- Flask Sunucusunu Başlat ---
app = Flask(__name__)

# --- ÇIKARTMA KAĞIDI ÖLÇÜLERİ (Tanex şablonuyla aynı) ---
TOP_MARGIN = 0.24 * 25.4 * mm
LEFT_MARGIN = 0.18 * 25.4 * mm
ETIKET_GENISLIK = 3.902 * 25.4 * mm
ETIKET_YUKSEKLIK = 2.244 * 25.4 * mm
HORIZONTAL_GUTTER = 0 * mm
VERTICAL_GUTTER = 0 * mm
PDF_FILE_NAME = "etiket.pdf" # Sabit dosya adı

# --- Türkçe Fontları Kaydet ---
try:
    pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
except:
    print("UYARI: Arial fontları bulunamadı.")

# --- PDF ETİKET OLUŞTURMA FONKSİYONU ---
# (Hizalama mantığı app-test.py'den kopyalandı)
def create_labels_pdf(spice_name, page_count, uretim_tarihi_str):
    PAGE_W, PAGE_H = A4
    c = canvas.Canvas(PDF_FILE_NAME, pagesize=A4)
    
    # --- TEK BİR ETİKETİ ÇİZEN FONKSİYON (app-test.py'deki son haliniz) ---
    def draw_single_label(x_base, y_base, genislik, yukseklik, baharat_adi):
        x_center = x_base + genislik / 2
        
        # 1. LOGO (90x30mm)
        logo_path = "logo.png" 
        LOGO_GENISLIK = 90 * mm  # Test dosyanızdaki son boyut
        LOGO_YUKSEKLIK = 30 * mm # Test dosyanızdaki son boyut
        
        try:
            logo = ImageReader(logo_path)
            y_logo_start = y_base + yukseklik - 2*mm - LOGO_YUKSEKLIK
            x_logo_start = x_center - (LOGO_GENISLIK / 2)
            c.drawImage(logo, x_logo_start, y_logo_start, width=LOGO_GENISLIK, height=LOGO_YUKSEKLIK, mask='auto')
            y_next_line = y_logo_start - 5*mm # Test dosyanızdaki son ayar
        except:
            y_next_line = y_base + yukseklik - 10*mm
            c.setFont('Arial', 8)
            c.drawCentredString(x_center, y_next_line, "[LOGO YOK - logo.png ekleyin]")
            y_next_line -= 8*mm

        # 2. BAHARAT ADI (12pt)
        c.setFont('Arial-Bold', 12) 
        c.drawCentredString(x_center, y_next_line, baharat_adi)
        y_next_line -= 5*mm # Test dosyanızdaki son ayar

        # 3. ÜRETİM TARİHİ (9pt)
        c.setFont('Arial', 9) 
        c.drawCentredString(x_center, y_next_line, f"Ürt Tarihi : {uretim_tarihi_str}")
        y_next_line -= 4*mm

        # 4. PARTİ NO (8pt)
        c.setFont('Arial', 8)
        c.drawCentredString(x_center, y_next_line, "PARTİ NO:ÜRETİM TARİHİDİR")
        y_next_line -= 4*mm

        # 5. İŞLETME NO (8pt)
        c.setFont('Arial', 8) 
        c.drawCentredString(x_center, y_next_line, "İŞLETME NO TR-34-K-257496")
        y_next_line -= 4*mm

        # 6. ADRES (6pt, Tek Satır)
        c.setFont('Arial', 6) 
        c.drawCentredString(x_center, y_next_line, "LİDER BAHARAT yücel Kaynak petroliş mh refah sk no 16 kartal")

    # --- ANA DÖNGÜ ---
    for _ in range(page_count):
        for col in range(2):
            x = LEFT_MARGIN + col * (ETIKET_GENISLIK + HORIZONTAL_GUTTER)
            for row in range(5):
                y = (PAGE_H - TOP_MARGIN - ETIKET_YUKSEKLIK) - row * (ETIKET_YUKSEKLIK + VERTICAL_GUTTER)
                draw_single_label(x, y, ETIKET_GENISLIK, ETIKET_YUKSEKLIK, spice_name)
        c.showPage()
        
    c.save()
    print(f"'{PDF_FILE_NAME}' oluşturuldu/güncellendi.")

# --- 1. Baharat verisini yükle ---
try:
    with open('baharatlar.json', 'r', encoding='utf-8') as f:
        baharat_listesi = json.load(f)
except:
    baharat_listesi = [{"ad": "HATA: baharatlar.json dosyası bulunamadı"}]

# --- 2. Ana web sayfasını sun ---
@app.route('/')
def index():
    return render_template('index.html', baharatlar=baharat_listesi)

# --- 3. PDF OLUŞTURMA Rotası (Önizleme için) ---
@app.route('/generate', methods=['POST'])
def handle_generate():
    try:
        data = request.json
        spice_name = data.get('spice')
        page_count = int(data.get('pages', 1))
        date_str = data.get('date') # Dinamik tarihi al

        if not spice_name:
            return jsonify({"success": False, "message": "Baharat adı seçilmedi."}), 400

        # Gelen 'YYYY-MM-DD' tarihini 'DD.MM.YYYY' formatına çevir
        if date_str:
            try:
                dt_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                uret_tarihi_formatted = dt_obj.strftime("%d.%m.%Y")
            except ValueError:
                uret_tarihi_formatted = datetime.date.today().strftime("%d.%m.%Y")
        else:
            uret_tarihi_formatted = datetime.date.today().strftime("%d.%m.%Y")
        
        print(f"PDF İsteği: {spice_name}, {page_count} sayfa, Tarih: {uret_tarihi_formatted}")
        
        # Testteki hizalama ile PDF'i oluştur
        create_labels_pdf(spice_name, page_count, uret_tarihi_formatted)
        
        return jsonify({
            "success": True, 
            "message": "PDF önizleme için hazır.",
            "pdf_url": f"/download/{PDF_FILE_NAME}"
        })
    
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

# --- 4. PDF YAZDIRMA Rotası ---
@app.route('/print-now', methods=['GET'])
def handle_print_now():
    try:
        if not os.path.exists(PDF_FILE_NAME):
            return jsonify({"success": False, "message": "Önce PDF oluşturulmalı."}), 404
            
        print(f"YAZDIRMA komutu: {PDF_FILE_NAME}")
        # Windows'ta varsayılan yazıcıya gönder
        os.startfile(PDF_FILE_NAME, "print")
        return jsonify({"success": True, "message": "Yazıcıya gönderildi."})
        
    except Exception as e:
        print(f"Yazdırma hatası: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

# --- 5. PDF GÖRÜNTÜLEME Rotası ---
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(directory='.', path=filename, as_attachment=False)

# --- 6. PWA için Manifest ve Static Dosya Rotaları ---
@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# --- Sunucuyu Başlat ---
if __name__ == '__main__':
    print("Sunucu başlatılıyor...")
    print("Babanızın telefonundan erişim için:")
    print("1. Bonjour'un (Apple Yazdırma Hizmetleri) kurulu olduğundan emin olun.")
    print("2. Bilgisayarınızın adını öğrenin (örn: 'BABAMIN-PC').")
    print("3. Adresi http://BABAMIN-PC.local:5000 olarak girin.")
    app.run(host='0.0.0.0', port=5000)
