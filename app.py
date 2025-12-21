import os
import json
import datetime
import threading
import logging
import subprocess
import sys
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_from_directory

# --- PDF Oluşturma Kütüphaneleri ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 # A4 boyutlarını almak için
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- Flask Sunucusunu Başlat ---
app = Flask(__name__, template_folder='Templates')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# --- Dosya Yolları ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'baharatlar.json')
PDF_FILE_NAME = os.path.join(BASE_DIR, "etiket.pdf")
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")
STATIC_PATH = os.path.join(BASE_DIR, "static")
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'}

json_lock = threading.Lock()
upload_queue_lock = threading.Lock()
upload_queue = []  # Queue for uploaded files

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, 'app.log')),
        logging.StreamHandler()
    ]
)

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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


# --- FILE UPLOAD HELPER FUNCTIONS ---

def allowed_file(filename):
    """Check if file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def print_file_automatically(filepath):
    """
    Automatically print a file without user interaction.
    Works on Windows by using shell print verb.
    """
    try:
        if sys.platform == 'win32':
            # Try using win32api first (best for automation)
            try:
                import win32api
                import win32print
                
                # Get default printer
                printer_name = win32print.GetDefaultPrinter()
                logging.info(f"Printing to: {printer_name}")
                
                # Print using shell execute with 'print' verb
                win32api.ShellExecute(0, "print", filepath, None, ".", 0)
                logging.info(f"Successfully sent print job: {filepath}")
                return True
            except ImportError:
                # Fallback to os.startfile if win32api not available
                logging.warning("win32api not available, using os.startfile")
                os.startfile(filepath, "print")
                logging.info(f"Successfully sent print job via os.startfile: {filepath}")
                return True
        else:
            # For Unix-like systems
            subprocess.run(['lpr', filepath], check=True)
            logging.info(f"Successfully sent print job: {filepath}")
            return True
    except Exception as e:
        logging.error(f"Error printing file {filepath}: {e}")
        return False


def add_to_upload_queue(filename, filepath):
    """Add a file to the upload queue"""
    with upload_queue_lock:
        upload_queue.append({
            'filename': filename,
            'filepath': filepath,
            'timestamp': datetime.datetime.now().isoformat()
        })
        logging.info(f"Added to queue: {filename}")


def get_upload_queue():
    """Get current upload queue"""
    with upload_queue_lock:
        return list(upload_queue)


def clear_upload_queue():
    """Clear the upload queue"""
    with upload_queue_lock:
        upload_queue.clear()
        logging.info("Upload queue cleared")


def remove_from_queue(index):
    """Remove a specific item from the queue"""
    with upload_queue_lock:
        if 0 <= index < len(upload_queue):
            removed = upload_queue.pop(index)
            logging.info(f"Removed from queue: {removed['filename']}")
            return True
    return False


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


# --- 5. FILE UPLOAD ROUTES ---

@app.route('/upload-files', methods=['POST'])
def upload_files():
    """Handle multiple file uploads and add them to the queue"""
    try:
        if 'files[]' not in request.files:
            logging.warning("No files in request")
            return jsonify({"success": False, "message": "Dosya seçilmedi."}), 400
        
        files = request.files.getlist('files[]')
        if not files or files[0].filename == '':
            logging.warning("Empty file list")
            return jsonify({"success": False, "message": "Dosya seçilmedi."}), 400
        
        uploaded_count = 0
        failed_files = []
        
        for file in files:
            if file and file.filename:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to avoid filename conflicts
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    unique_filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
                    
                    try:
                        file.save(filepath)
                        add_to_upload_queue(filename, filepath)
                        uploaded_count += 1
                        logging.info(f"Successfully uploaded: {filename}")
                    except Exception as e:
                        logging.error(f"Failed to save file {filename}: {e}")
                        failed_files.append(filename)
                else:
                    logging.warning(f"File type not allowed: {file.filename}")
                    failed_files.append(file.filename)
        
        if uploaded_count > 0:
            message = f"{uploaded_count} dosya başarıyla yüklendi."
            if failed_files:
                message += f" {len(failed_files)} dosya başarısız: {', '.join(failed_files)}"
            logging.info(f"Upload complete: {uploaded_count} success, {len(failed_files)} failed")
            return jsonify({"success": True, "message": message, "count": uploaded_count})
        else:
            return jsonify({"success": False, "message": "Hiçbir dosya yüklenemedi."}), 400
            
    except Exception as e:
        logging.error(f"Upload error: {e}")
        return jsonify({"success": False, "message": f"Yükleme hatası: {str(e)}"}), 500


@app.route('/get-upload-queue', methods=['GET'])
def get_queue():
    """Get the current upload queue"""
    try:
        queue = get_upload_queue()
        return jsonify({"success": True, "queue": queue})
    except Exception as e:
        logging.error(f"Error getting queue: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/remove-from-queue', methods=['POST'])
def remove_queue_item():
    """Remove an item from the upload queue"""
    try:
        data = request.json
        index = data.get('index')
        
        if index is None:
            return jsonify({"success": False, "message": "Index gerekli."}), 400
        
        if remove_from_queue(index):
            return jsonify({"success": True, "message": "Dosya kuyruktan kaldırıldı."})
        else:
            return jsonify({"success": False, "message": "Geçersiz index."}), 400
            
    except Exception as e:
        logging.error(f"Error removing from queue: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/print-all-uploads', methods=['POST'])
def print_all_uploads():
    """Automatically print all files in the upload queue"""
    try:
        queue = get_upload_queue()
        
        if not queue:
            logging.warning("Print all called with empty queue")
            return jsonify({"success": False, "message": "Yazdırma kuyruğu boş."}), 400
        
        success_count = 0
        failed_files = []
        
        for item in queue:
            filepath = item['filepath']
            filename = item['filename']
            
            if os.path.exists(filepath):
                if print_file_automatically(filepath):
                    success_count += 1
                else:
                    failed_files.append(filename)
            else:
                logging.error(f"File not found: {filepath}")
                failed_files.append(filename)
        
        # Clear the queue after printing
        if success_count > 0:
            clear_upload_queue()
            message = f"{success_count} dosya yazıcıya gönderildi."
            if failed_files:
                message += f" {len(failed_files)} dosya başarısız."
            logging.info(f"Print all complete: {success_count} success, {len(failed_files)} failed")
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "message": "Hiçbir dosya yazdırılamadı."}), 500
            
    except Exception as e:
        logging.error(f"Print all error: {e}")
        return jsonify({"success": False, "message": f"Yazdırma hatası: {str(e)}"}), 500


# --- 6. PWA için Manifest ve Static Dosya Rotaları (Aynı) ---
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
