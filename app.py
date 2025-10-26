import os
import json
import datetime
import threading 
from flask import Flask, render_template, request, jsonify, send_from_directory

# --- PDF Oluşturma Kütüphaneleri ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- Flask Sunucusunu Başlat ---
app = Flask(__name__, template_folder='Templates')

# --- Dosya Yolları ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'baharatlar.json')
PDF_FILE_NAME = os.path.join(BASE_DIR, "etiket.pdf")
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")
STATIC_PATH = os.path.join(BASE_DIR, "static")

json_lock = threading.Lock()

# --- ÇIKARTMA KAĞIDI ÖLÇÜLERİ ---
TOP_MARGIN = 0.24 * 25.4 * mm
LEFT_MARGIN = 0.18 * 25.4 * mm
ETIKET_GENISLIK = 3.902 * 25.4 * mm
ETIKET_YUKSEKLIK = 2.244 * 25.4 * mm
HORIZONTAL_GUTTER = 0 * mm
VERTICAL_GUTTER = 0 * mm

# --- Türkçe Fontları Kaydet ---
try:
    pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
except:
    print("UYARI: Arial fontları bulunamadı.")


# --- JSON Veri Okuma/Yazma Fonksiyonları (Aynı) ---

def load_json_data():
    with json_lock: 
        if not os.path.exists(JSON_PATH):
            print(f"UYARI: '{JSON_PATH}' bulunamadı, varsayılan dosya oluşturuluyor.")
            default_data = {"baharatlar": ["ÖRNEK BAHARAT"], "gramajlar": ["1 KG"]}
            save_json_data(default_data)
            return default_data
        
        try:
            with open(JSON_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"!!! KRİTİK HATA: JSON okuma hatası: {e}")
            return {"baharatlar": [], "gramajlar": []}

def save_json_data(data):
    with json_lock:
        try:
            with open(JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("Başarılı: baharatlar.json dosyası güncellendi.")
        except Exception as e:
            print(f"!!! KRİTİK HATA: JSON yazma hatası: {e}")


# --- PDF ETİKET OLUŞTURMA FONKSİYONU (GÜNCELLENDİ) ---
# YENİ: Artık 'uretim_tarihi_str' parametresini alıyor
def create_labels_pdf(cart_items, uretim_tarihi_str):
    PAGE_W, PAGE_H = A4
    c = canvas.Canvas(PDF_FILE_NAME, pagesize=A4)
    
    # --- TEK BİR ETİKETİ ÇİZEN FONKSİYON ---
    # (app-test.py dosyanızdaki son hizalama)
    def draw_single_label(x_base, y_base, genislik, yukseklik, baharat_adi):
        x_center = x_base + genislik / 2
        
        LOGO_GENISLIK = 90 * mm
        LOGO_YUKSEKLIK = 30 * mm
        
        try:
            logo = ImageReader(LOGO_PATH)
            y_logo_start = y_base + yukseklik - 2*mm - LOGO_YUKSEKLIK
            x_logo_start = x_center - (LOGO_GENISLIK / 2)
            c.drawImage(logo, x_logo_start, y_logo_start, width=LOGO_GENISLIK, height=LOGO_YUKSEKLIK, mask='auto')
            y_next_line = y_logo_start - 5*mm
        except:
            y_next_line = y_base + yukseklik - 10*mm
            c.setFont('Arial', 8)
            c.drawCentredString(x_center, y_next_line, "[LOGO YOK - logo.png ekleyin]")
            y_next_line -= 8*mm

        c.setFont('Arial-Bold', 12) 
        c.drawCentredString(x_center, y_next_line, baharat_adi)
        y_next_line -= 5*mm

        # YENİ: 'uretim_tarihi_str' değişkeni artık burada mevcut
        c.setFont('Arial', 9) 
        c.drawCentredString(x_center, y_next_line, f"Ürt Tarihi : {uretim_tarihi_str}")
        y_next_line -= 4*mm

        c.setFont('Arial', 8)
        c.drawCentredString(x_center, y_next_line, "PARTİ NO:ÜRETİM TARİHİDİR")
        y_next_line -= 4*mm

        c.setFont('Arial', 8) 
        c.drawCentredString(x_center, y_next_line, "İŞLETME NO TR-34-K-257496")
        y_next_line -= 4*mm

        c.setFont('Arial', 6) 
        c.drawCentredString(x_center, y_next_line, "LİDER BAHARAT yücel Kaynak petroliş mh refah sk no 16 kartal")

    # --- ANA DÖNGÜ (Sepet Mantığı) ---
    for item in cart_items:
        label_name = item['label']
        page_count = int(item['pages'])
        
        for _ in range(page_count):
            for row in range(5):
                for col in range(2):
                    x = LEFT_MARGIN + col * (ETIKET_GENISLIK + HORIZONTAL_GUTTER)
                    y = (PAGE_H - TOP_MARGIN - ETIKET_YUKSEKLIK) - row * (ETIKET_YUKSEKLIK + VERTICAL_GUTTER)
                    
                    # Etiketi çiz
                    draw_single_label(x, y, ETIKET_GENISLIK, ETIKET_YUKSEKLIK, label_name)
            
            c.showPage()
        
    c.save()
    print(f"'{PDF_FILE_NAME}' oluşturuldu/güncellendi. Toplam {len(cart_items)} kalem ürün.")


# --- 1. Ana web sayfasını sun (Aynı) ---
@app.route('/')
def index():
    data = load_json_data() 
    baharat_listesi = data.get("baharatlar", [])
    gramaj_listesi = data.get("gramajlar", [])
    return render_template('index.html', baharat_listesi=baharat_listesi, gramaj_listesi=gramaj_listesi)

# --- 2. YAZDIRMA Rotası (GÜNCELLENDİ) ---
@app.route('/print-cart', methods=['POST'])
def handle_print_cart():
    try:
        data = request.json
        cart_data = data.get('cart')
        date_str = data.get('date') # YENİ: Tarihi al

        if not cart_data:
            return jsonify({"success": False, "message": "Sepet boş."}), 400
        if not date_str:
            return jsonify({"success": False, "message": "Tarih seçilmedi."}), 400

        # YENİ: Gelen 'YYYY-MM-DD' tarihini 'DD.MM.YYYY' formatına çevir
        try:
            dt_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            uret_tarihi_formatted = dt_obj.strftime("%d.%m.%Y")
        except ValueError:
            uret_tarihi_formatted = "TARIH HATASI" # Geçersiz tarih gelirse

        print(f"Yazdırma İsteği Alındı: {len(cart_data)} kalem. Tarih: {uret_tarihi_formatted}")
        
        # 1. Adım: PDF'i tarih bilgisiyle oluştur
        create_labels_pdf(cart_data, uret_tarihi_formatted)
        
        # 2. Adım: PDF'i yazdır
        print(f"YAZDIRMA komutu: {PDF_FILE_NAME}")
        os.startfile(PDF_FILE_NAME, "print")
        
        return jsonify({"success": True, "message": "Tüm sepet yazıcıya gönderildi."})
    
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

# --- 3. Yeni Baharat Ekleme Rotası (Aynı) ---
@app.route('/add-spice', methods=['POST'])
def add_spice():
    try:
        data = request.json
        new_spice = data.get('spice_name', '').strip().upper()
        if not new_spice:
            return jsonify({"success": False, "message": "Baharat adı boş olamaz."}), 400

        current_data = load_json_data()
        baharat_listesi = current_data.get("baharatlar", [])
        
        if new_spice in baharat_listesi:
            return jsonify({"success": False, "message": "Bu baharat zaten listede var."}), 400
        
        baharat_listesi.append(new_spice)
        baharat_listesi.sort() 
        current_data["baharatlar"] = baharat_listesi
        save_json_data(current_data)
        
        return jsonify({"success": True, "message": f"Başarılı: '{new_spice}' eklendi."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Sunucu hatası: {e}"}), 500

# --- 4. Yeni Gramaj Ekleme Rotası (Aynı) ---
@app.route('/add-weight', methods=['POST'])
def add_weight():
    try:
        data = request.json
        new_weight = data.get('weight_name', '').strip().upper()
        if not new_weight:
            return jsonify({"success": False, "message": "Gramaj boş olamaz."}), 400

        current_data = load_json_data()
        gramaj_listesi = current_data.get("gramajlar", [])
        
        if new_weight in gramaj_listesi:
            return jsonify({"success": False, "message": "Bu gramaj zaten listede var."}), 400
        
        gramaj_listesi.append(new_weight)
        current_data["gramajlar"] = gramaj_listesi
        save_json_data(current_data)
        
        return jsonify({"success": True, "message": f"Başarılı: '{new_weight}' eklendi."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Sunucu hatası: {e}"}), 500


# --- 5. PWA için Manifest ve Static Dosya Rotaları (Aynı) ---
@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory(STATIC_PATH, 'manifest.json')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_PATH, filename)

# --- Sunucuyu Başlat ---
if __name__ == '__main__':
    print("Sunucu başlatılıyor...")
    print("Telefondan erişim için: http://[BILGISAYAR-ADI].local:5000")
    app.run(host='0.0.0.0', port=5000)
