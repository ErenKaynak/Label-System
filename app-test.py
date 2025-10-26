import os
import datetime

# --- PDF Oluşturma Kütüphaneleri ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm 
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- ÇIKARTMA KAĞIDI ÖLÇÜLERİ (Aynı kaldı) ---
TOP_MARGIN = 0.24 * 25.4 * mm
LEFT_MARGIN = 0.18 * 25.4 * mm
ETIKET_GENISLIK = 3.902 * 25.4 * mm
ETIKET_YUKSEKLIK = 2.244 * 25.4 * mm
HORIZONTAL_GUTTER = 0 * mm
VERTICAL_GUTTER = 0 * mm

PDF_TEST_FILE_NAME = "ETIKET_TEST.pdf" 

# --- Türkçe Fontları Kaydet ---
try:
    pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
except:
    print("UYARI: Arial fontları bulunamadı.")

# --- PDF ETİKET OLUŞTURMA FONKSİYONU ---
def create_labels_pdf(spice_name, page_count, uretim_tarihi_str):
    PAGE_W, PAGE_H = A4
    c = canvas.Canvas(PDF_TEST_FILE_NAME, pagesize=A4)
    
    # --- TEK BİR ETİKETİ ÇİZEN FONKSİYON (GÜNCELLENDİ) ---
    def draw_single_label(x_base, y_base, genislik, yukseklik, baharat_adi):
        x_center = x_base + genislik / 2
        
        # 1. LOGO (İSTEK: 45mm genişlik)
        logo_path = "logo.png" 
        LOGO_GENISLIK = 45 * mm  # 45mm olarak büyütüldü
        LOGO_YUKSEKLIK = 20 * mm 
        
        try:
            logo = ImageReader(logo_path)
            y_logo_start = y_base + yukseklik - 2*mm - LOGO_YUKSEKLIK
            x_logo_start = x_center - (LOGO_GENISLIK / 2)
            c.drawImage(logo, x_logo_start, y_logo_start, width=LOGO_GENISLIK, height=LOGO_YUKSEKLIK, mask='auto')
            y_next_line = y_logo_start - 5*mm # Boşluk azaltıldı
        except:
            y_next_line = y_base + yukseklik - 10*mm
            c.setFont('Arial', 8)
            c.drawCentredString(x_center, y_next_line, "[LOGO YOK - logo.png ekleyin]")
            y_next_line -= 8*mm

        # 2. BAHARAT ADI (12pt)
        c.setFont('Arial-Bold', 12) 
        c.drawCentredString(x_center, y_next_line, baharat_adi)
        y_next_line -= 5*mm # Boşluk azaltıldı (6'dan 5'e)

        # 3. ÜRETİM TARİHİ (9pt)
        c.setFont('Arial', 9) 
        c.drawCentredString(x_center, y_next_line, f"Ürt Tarihi : {uretim_tarihi_str}")
        y_next_line -= 4*mm

        # 4. PARTİ NO (8pt)
        c.setFont('Arial', 8)
        c.drawCentredString(x_center, y_next_line, "PARTİ NO:ÜRETİM TARİHİDİR")
        y_next_line -= 4*mm # Bir satır aşağı in

        # 5. İŞLETME NO (İSTEK: Yeri değişti, 8pt)
        c.setFont('Arial', 8) 
        c.drawCentredString(x_center, y_next_line, "İŞLETME NO TR-34-K-257496")
        y_next_line -= 4*mm # Bir satır aşağı in

        # 6. ADRES (İSTEK: 6pt, Tek Satır)
        c.setFont('Arial', 6) 
        c.drawCentredString(x_center, y_next_line, "LİDER BAHARAT yücel Kaynak petroliş mh refah sk no 16 kartal")
        # Bu son satır, altına boşluk gerekmiyor.

    # --- ANA DÖNGÜ ---
    for _ in range(page_count):
        for col in range(2):
            x = LEFT_MARGIN + col * (ETIKET_GENISLIK + HORIZONTAL_GUTTER)
            for row in range(5):
                y = (PAGE_H - TOP_MARGIN - ETIKET_YUKSEKLIK) - row * (ETIKET_YUKSEKLIK + VERTICAL_GUTTER)
                draw_single_label(x, y, ETIKET_GENISLIK, ETIKET_YUKSEKLIK, spice_name)
        c.showPage()
        
    c.save()
    print(f"'{PDF_TEST_FILE_NAME}' oluşturuldu.")

# --- ANA TEST ÇALIŞTIRMA BÖLÜMÜ ---
if __name__ == '__main__':
    print("Test PDF oluşturucu başlatıldı...")
    
    TEST_BAHARAT_ADI = "TEST ÜRÜNÜ (12 PUNTO)"
    TEST_SAYFA_SAYISI = 1
    TEST_URETIM_TARIHI = "25.10.2025"
    
    try:
        create_labels_pdf(TEST_BAHARAT_ADI, TEST_SAYFA_SAYISI, TEST_URETIM_TARIHI)
        print(f"Başarılı! '{PDF_TEST_FILE_NAME}' dosyası bu klasörde oluşturuldu.")
        
        print("Test PDF dosyası açılıyor...")
        try:
            os.startfile(PDF_TEST_FILE_NAME)
        except AttributeError:
            import subprocess
            if sys.platform == "darwin": subprocess.call(["open", PDF_TEST_FILE_NAME])
            else: subprocess.call(["xdg-open", PDF_TEST_FILE_NAME])
        
    except Exception as e:
        print(f"PDF oluşturulurken bir hata oluştu: {e}")

    print("Test tamamlandı.")
