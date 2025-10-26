import os
import datetime

# --- PDF Oluşturma Kütüphaneleri ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm # Milimetre birimini ekledik
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- ÇIKARTMA KAĞIDI ÖLÇÜLERİ (app.py ile aynı) ---
TOP_MARGIN = 0.24 * 25.4 * mm
LEFT_MARGIN = 0.18 * 25.4 * mm
ETIKET_GENISLIK = 3.902 * 25.4 * mm
ETIKET_YUKSEKLIK = 2.244 * 25.4 * mm
HORIZONTAL_GUTTER = 0 * mm
VERTICAL_GUTTER = 0 * mm

# --- TEST DOSYA ADI ---
# Ana dosyanızın (etiket.pdf) üzerine yazmaması için
PDF_TEST_FILE_NAME = "ETIKET_TEST.pdf" 

# --- Türkçe Fontları Kaydet ---
try:
    pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
except:
    print("UYARI: Arial fontları bulunamadı.")

# --- PDF ETİKET OLUŞTURMA FONKSİYONU ---
def create_labels_pdf(spice_name, page_count):
    # Tarihleri hesapla
    today = datetime.date.today()
    uret_tarihi = today.strftime("%d.%m.%Y")
    stt_tarihi = (today.replace(year=today.year + 2)).strftime("%d.%m.%Y")
    parti_no = uret_tarihi.replace(".", "")

    PAGE_W, PAGE_H = A4
    c = canvas.Canvas(PDF_TEST_FILE_NAME, pagesize=A4)
    
    # --- TEK BİR ETİKETİ ÇİZEN FONKSİYON ---
    # Hizalama sorunları varsa, milimetrik (mm) değerleri burada oynayın
    def draw_single_label(x_base, y_base, genislik, yukseklik, baharat_adi):
        x_center = x_base + genislik / 2
        logo_path = "logo.png" 
        LOGO_GENISLIK = 40 * mm # Test: Logoyu büyütüp küçült
        LOGO_YUKSEKLIK = 25 * mm # Test: Logoyu büyütüp küçült
        
        try:
            logo = ImageReader(logo_path)
            y_logo_start = y_base + yukseklik - 5*mm - LOGO_YUKSEKLIK
            x_logo_start = x_center - (LOGO_GENISLIK / 2)
            c.drawImage(logo, x_logo_start, y_logo_start, width=LOGO_GENISLIK, height=LOGO_YUKSEKLIK, mask='auto')
            y_next_line = y_logo_start - 6*mm # Test: Logo ile yazı arasını aç/kapat
        except:
            y_next_line = y_base + yukseklik - 10*mm
            c.setFont('Arial', 8)
            c.drawCentredString(x_center, y_next_line, "[LOGO YOK - logo.png ekleyin]")
            y_next_line -= 8*mm

        c.setFont('Arial-Bold', 14)
        c.drawCentredString(x_center, y_next_line, baharat_adi)
        y_next_line -= 8*mm # Test: İsim ile tarihler arasını aç/kapat

        c.setFont('Arial', 8)
        c.drawCentredString(x_center, y_next_line, f"ÜRT.TARİHİ: {uret_tarihi}")
        y_next_line -= 4*mm
        
        # !!! DİKKAT !!! Firma bilgilerinizi burada test için güncelleyin
        c.drawCentredString(x_center, y_next_line, "LİDER BAHARAT yücel kaynak petroliş mh refah sk no 16")
        y_next_line -= 4*mm
        c.drawCentredString(x_center, y_next_line, "kartal İŞLETME NO TR-34-K-257496")
        y_next_line -= 6*mm

        x_sol_nokta = x_base + 10*mm
        x_sag_nokta = x_base + genislik - 10*mm
        
        c.drawString(x_sol_nokta, y_next_line, f"S.T.T {stt_tarihi}")
        c.drawRightString(x_sag_nokta, y_next_line, f"PARTİ NO: {parti_no}")
    
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
    
    # -----------------------------------------------------------------
    # --- TEST İÇİN BU DEĞERLERİ DEĞİŞTİRİN ---
    # -----------------------------------------------------------------
    TEST_BAHARAT_ADI = "TEST ÜRÜNÜ ÇOK UZUN İSİM 12345 KG"
    TEST_SAYFA_SAYISI = 1
    # -----------------------------------------------------------------

    try:
        create_labels_pdf(TEST_BAHARAT_ADI, TEST_SAYFA_SAYISI)
        
        print(f"Başarılı! '{PDF_TEST_FILE_NAME}' dosyası bu klasörde oluşturuldu.")
        
        # PDF'i oluşturduktan sonra otomatik olarak aç (Windows için)
        # MacOS veya Linux kullanıyorsanız 'os.startfile' yerine 'os.system' gerekebilir
        print("Test PDF dosyası açılıyor...")
        try:
            os.startfile(PDF_TEST_FILE_NAME)
        except AttributeError:
            # os.startfile Windows'a özgüdür. MacOS/Linux için:
            import subprocess
            if sys.platform == "darwin": # MacOS
                subprocess.call(["open", PDF_TEST_FILE_NAME])
            else: # Linux
                subprocess.call(["xdg-open", PDF_TEST_FILE_NAME])
        
    except Exception as e:
        print(f"PDF oluşturulurken bir hata oluştu: {e}")

    print("Test tamamlandı.")
