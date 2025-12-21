import os
import json
import datetime
import threading 
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# --- PDF Oluşturma Kütüphaneleri ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 # A4 boyutlarını almak için
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
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
PRINT_QUEUE_PATH = os.path.join(BASE_DIR, 'print_queue.json')

# --- Dosya Yükleme Ayarları ---
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Flask ayarları
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

json_lock = threading.Lock()
queue_lock = threading.Lock()

# --- ÇIKARTMA KAĞIDI ÖLÇÜLERİ (GÜNCELLENDİ) ---
# İSTEK 7: Marjları 0'a 0 yap
PAGE_W, PAGE_H = A4 # A4 boyutlarını (genişlik, yükseklik) al
TOP_MARGIN = 0 * mm
LEFT_MARGIN = 0 * mm
HORIZONTAL_GUTTER = 0 * mm
VERTICAL_GUTTER = 0 * mm

# 10 eşit parçaya böl
ETIKET_GENISLIK = PAGE_W / 2  # A4 Genişliği / 2
ETIKET_YUKSEKLIK = PAGE_H / 5 # A4 Yüksekliği / 5


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


# --- DOSYA YÜKLEME YARDIMCI FONKSİYONLARI ---

def allowed_file(filename):
    """Dosya uzantısının izin verilen türlerden olup olmadığını kontrol eder."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_print_queue():
    """Print queue JSON dosyasını yükler."""
    with queue_lock:
        if not os.path.exists(PRINT_QUEUE_PATH):
            return {"queue": []}
        
        try:
            with open(PRINT_QUEUE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Print queue okuma hatası: {e}")
            return {"queue": []}


def save_print_queue(queue_data):
    """Print queue'yu JSON dosyasına kaydeder."""
    with queue_lock:
        try:
            with open(PRINT_QUEUE_PATH, 'w', encoding='utf-8') as f:
                json.dump(queue_data, f, ensure_ascii=False, indent=2)
            print("Print queue güncellendi.")
        except Exception as e:
            print(f"Print queue yazma hatası: {e}")


def add_to_print_queue(filename, original_filename):
    """Dosyayı print queue'ya ekler."""
    queue_data = load_print_queue()
    queue_item = {
        "id": len(queue_data["queue"]) + 1,
        "filename": filename,
        "original_filename": original_filename,
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "pending"
    }
    queue_data["queue"].append(queue_item)
    save_print_queue(queue_data)
    return queue_item


# --- PDF ETİKET OLUŞTURMA FONKSİYONU (GÜNCELLENDİ) ---
# YENİ: Artık 'stt_tarihi_str' (MM / YYYY) alıyor
def create_labels_pdf(cart_items, stt_tarihi_str):
    c = canvas.Canvas(PDF_FILE_NAME, pagesize=A4)
    
    # --- TEK BİR ETİKETİ ÇİZEN FONKSİYON ---
    # (Tüm isteklerinize göre güncellendi)
    def draw_single_label(x_base, y_base, genislik, yukseklik, baharat_adi):
        # x_center artık etiketin tam ortası (marj 0 olduğu için)
        x_center = x_base + genislik / 2
        
        LOGO_GENISLIK = 90 * mm
        LOGO_YUKSEKLIK = 30 * mm
        
        try:
            logo = ImageReader(LOGO_PATH)
            # Y konumu: Etiketin üstünden 2mm boşluk bırak
            y_logo_start = y_base + yukseklik - 2*mm - LOGO_YUKSEKLIK
            # İSTEK 1: x_center kullanarak ortala
            x_logo_start = x_center - (LOGO_GENISLIK / 2) 
            c.drawImage(logo, x_logo_start, y_logo_start, width=LOGO_GENISLIK, height=LOGO_YUKSEKLIK, mask='auto')
            y_next_line = y_logo_start - 5*mm
        except:
            y_next_line = y_base + yukseklik - 10*mm
            c.setFont('Arial', 8)
            c.drawCentredString(x_center, y_next_line, "[LOGO YOK - logo.png ekleyin]")
            y_next_line -= 8*mm

        # Baharat Adı (12pt)
        c.setFont('Arial-Bold', 12) 
        c.drawCentredString(x_center, y_next_line, baharat_adi)
        y_next_line -= 5*mm

        # İSTEK 2: Üretim Tarihi SİLİNDİ

        # İSTEK 3 & 4: STT Eklendi (Ay/Yıl) (9pt)
        c.setFont('Arial', 9) 
        c.drawCentredString(x_center, y_next_line, f"STT : {stt_tarihi_str}")
        y_next_line -= 4*mm

        # İSTEK 5: Parti No metni güncellendi (8pt)
        c.setFont('Arial', 8)
        c.drawCentredString(x_center, y_next_line, "PARTİ NO:SON TÜKETİM TARİHİDİR")
        y_next_line -= 4*mm

        # İşletme No (8pt)
        c.setFont('Arial', 8) 
        c.drawCentredString(x_center, y_next_line, "İŞLETME NO TR-34-K-257496")
        y_next_line -= 4*mm

        # İSTEK 6: Adres güncellendi (8pt, "LİDER BAHARAT" silindi)
        c.setFont('Arial', 8) # 6pt -> 8pt
        c.drawCentredString(x_center, y_next_line, "yücel Kaynak petroliş mh refah sk no 16 kartal")

    # --- ANA DÖNGÜ (Sepet Mantığı) ---
    for item in cart_items:
        label_name = item['label']
        page_count = int(item['pages'])
        
        for _ in range(page_count):
            for row in range(5):
                for col in range(2):
                    # İSTEK 7: Marjlar 0 olduğu için hesaplama basitleşti
                    x = LEFT_MARGIN + col * ETIKET_GENISLIK
                    # ReportLab Y ekseni alttan başlar (0)
                    y = (PAGE_H - TOP_MARGIN - ETIKET_YUKSEKLIK) - row * ETIKET_YUKSEKLIK
                    
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


# --- DOSYA YÜKLEME VE YAZDIRMA KUYRUĞU ROTALARı ---

@app.route('/upload-file', methods=['POST'])
def upload_file():
    """Dosya yükleme endpoint'i."""
    try:
        # Dosya kontrolü
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "Dosya seçilmedi."}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"success": False, "message": "Dosya seçilmedi."}), 400
        
        # Dosya tipi kontrolü
        if not allowed_file(file.filename):
            return jsonify({
                "success": False, 
                "message": "Geçersiz dosya tipi. Sadece PDF, PNG, JPG dosyaları yükleyebilirsiniz."
            }), 400
        
        # Dosyayı kaydet
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Uploads klasörünü oluştur (yoksa)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        file.save(filepath)
        
        # Print queue'ya ekle
        queue_item = add_to_print_queue(unique_filename, filename)
        
        return jsonify({
            "success": True, 
            "message": f"'{filename}' başarıyla yüklendi ve yazdırma kuyruğuna eklendi.",
            "queue_item": queue_item
        })
        
    except Exception as e:
        print(f"Dosya yükleme hatası: {e}")
        return jsonify({"success": False, "message": f"Dosya yükleme hatası: {str(e)}"}), 500


@app.route('/get-print-queue', methods=['GET'])
def get_print_queue():
    """Print queue'yu döndürür."""
    try:
        queue_data = load_print_queue()
        return jsonify({"success": True, "queue": queue_data["queue"]})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/remove-from-queue/<int:item_id>', methods=['DELETE'])
def remove_from_queue(item_id):
    """Print queue'dan bir öğe siler."""
    try:
        queue_data = load_print_queue()
        queue = queue_data["queue"]
        
        # ID'ye göre öğeyi bul
        item_to_remove = None
        for i, item in enumerate(queue):
            if item["id"] == item_id:
                item_to_remove = queue.pop(i)
                break
        
        if item_to_remove is None:
            return jsonify({"success": False, "message": "Öğe bulunamadı."}), 404
        
        # Dosyayı sil
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], item_to_remove["filename"])
        if os.path.exists(filepath):
            os.remove(filepath)
        
        save_print_queue(queue_data)
        
        return jsonify({"success": True, "message": "Öğe kuyruktan silindi."})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/print-queue-item/<int:item_id>', methods=['POST'])
def print_queue_item(item_id):
    """Kuyruktaki bir öğeyi yazdırır."""
    try:
        queue_data = load_print_queue()
        queue = queue_data["queue"]
        
        # ID'ye göre öğeyi bul
        item_to_print = None
        for item in queue:
            if item["id"] == item_id:
                item_to_print = item
                break
        
        if item_to_print is None:
            return jsonify({"success": False, "message": "Öğe bulunamadı."}), 404
        
        # Dosyayı yazdır
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], item_to_print["filename"])
        
        if not os.path.exists(filepath):
            return jsonify({"success": False, "message": "Dosya bulunamadı."}), 404
        
        # Durumu güncelle
        item_to_print["status"] = "printing"
        save_print_queue(queue_data)
        
        # Dosyayı yazdır
        print(f"Yazdırma komutu: {filepath}")
        os.startfile(filepath, "print")
        
        # Durumu tamamlandı olarak işaretle
        item_to_print["status"] = "completed"
        item_to_print["printed_at"] = datetime.datetime.now().isoformat()
        save_print_queue(queue_data)
        
        return jsonify({
            "success": True, 
            "message": f"'{item_to_print['original_filename']}' yazıcıya gönderildi."
        })
        
    except Exception as e:
        print(f"Yazdırma hatası: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/print-all-queue', methods=['POST'])
def print_all_queue():
    """Kuyruktaki tüm bekleyen öğeleri yazdırır."""
    try:
        queue_data = load_print_queue()
        queue = queue_data["queue"]
        
        printed_count = 0
        for item in queue:
            if item["status"] == "pending":
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], item["filename"])
                
                if os.path.exists(filepath):
                    print(f"Yazdırma komutu: {filepath}")
                    os.startfile(filepath, "print")
                    item["status"] = "completed"
                    item["printed_at"] = datetime.datetime.now().isoformat()
                    printed_count += 1
        
        save_print_queue(queue_data)
        
        return jsonify({
            "success": True, 
            "message": f"{printed_count} dosya yazıcıya gönderildi."
        })
        
    except Exception as e:
        print(f"Toplu yazdırma hatası: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


# --- 2. YAZDIRMA Rotası (GÜNCELLENDİ) ---
@app.route('/print-cart', methods=['POST'])
def handle_print_cart():
    try:
        data = request.json
        cart_data = data.get('cart')
        date_str = data.get('date') # GÜNCELLENDİ: STT (YYYY-MM) al

        if not cart_data:
            return jsonify({"success": False, "message": "Sepet boş."}), 400
        if not date_str:
            return jsonify({"success": False, "message": "STT seçilmedi."}), 400

        # GÜNCELLENDİ: Gelen 'YYYY-MM' tarihini 'MM / YYYY' formatına çevir
        try:
            dt_obj = datetime.datetime.strptime(date_str, '%Y-%m')
            stt_tarihi_formatted = dt_obj.strftime("%m / %Y") # Format: "10 / 2025"
            
        except ValueError:
            stt_tarihi_formatted = "TARIH HATASI"

        print(f"Yazdırma İsteği Alındı: {len(cart_data)} kalem. STT: {stt_tarihi_formatted}")
        
        # 1. Adım: PDF'i STT bilgisiyle oluştur
        create_labels_pdf(cart_data, stt_tarihi_formatted)
        
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
