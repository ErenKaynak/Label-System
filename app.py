import io
from html import escape
import json
import os
import re
import subprocess
import sys
import threading
from datetime import datetime

from flask import Flask, jsonify, render_template, request, send_file, send_from_directory
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

from product_profiles import SPICE_PROFILES

app = Flask(__name__, template_folder='Templates')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'baharatlar.json')
BUSINESS_PATH = os.path.join(BASE_DIR, 'isletme.json')
STATIC_PATH = os.path.join(BASE_DIR, 'static')
LOGO_PATH = os.path.join(BASE_DIR, 'logo.png')
json_lock = threading.RLock()
DEFAULT_STORAGE = 'Serin, kuru ve güneşten uzak tutunuz.'
LOT_STATEMENT = 'Parti/lot numarası, tavsiye edilen tüketim tarihidir.'
logo = ImageReader(LOGO_PATH)
logo_source_width, logo_source_height = logo.getSize()
# logo.png içindeki görünür çizimin yatay merkezi (beyaz kenarlar hariç).
LOGO_ARTWORK_CENTER_X = 200


def draw_logo(c, x, y, height, width=None):
    if width is None:
        width = height * logo_source_width / logo_source_height
    c.drawImage(logo, x, y, width=width, height=height)
    return width

FONT_PAIRS = [
    ('C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/arialbd.ttf'),
    ('/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'),
    ('/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf', '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf'),
    ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
    ('/usr/share/fonts/TTF/DejaVuSans.ttf', '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf'),
]
for regular_path, bold_path in FONT_PAIRS:
    if os.path.isfile(regular_path) and os.path.isfile(bold_path):
        pdfmetrics.registerFont(TTFont('Label-Regular', regular_path))
        pdfmetrics.registerFont(TTFont('Label-Bold', bold_path))
        pdfmetrics.registerFontFamily('Label-Regular', normal='Label-Regular', bold='Label-Bold')
        break
else:
    raise RuntimeError('Türkçe karakterleri destekleyen bir TrueType font bulunamadı.')

# 8 pt Arial/Liberation/DejaVu için küçük harf yüksekliği 1,2 mm'nin üstündedir.
# PDF her zaman gerçek ölçekte basılmalıdır; baskıdaki fiziksel ölçü kontrol edilmelidir.
BODY_SIZE = 8
LINE_HEIGHT = 10
NUTRITION_FIELDS = (
    ('calories', 'Kalori'),
    ('fat', 'Toplam yağ'),
    ('carbohydrate', 'Karbonhidrat'),
    ('sugar', 'Şeker'),
    ('protein', 'Protein'),
    ('fiber', 'Lif'),
    ('sodium', 'Sodyum'),
)
def load_json_data():
    with json_lock:
        if not os.path.exists(JSON_PATH):
            return {'baharatlar': [], 'gramajlar': []}
        with open(JSON_PATH, encoding='utf-8') as file:
            return json.load(file)


def save_json_data(data):
    with json_lock:
        with open(JSON_PATH, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


def load_business_settings():
    with json_lock:
        if not os.path.exists(BUSINESS_PATH):
            return {'operator': '', 'address': '', 'registration': ''}
        with open(BUSINESS_PATH, encoding='utf-8') as file:
            saved = json.load(file)
        return {key: str(saved.get(key, '')) for key in ('operator', 'address', 'registration')}


def save_business_settings(data):
    business = {key: required_text(data.get(key), label) for key, label in (
        ('operator', 'İşletmeci adı'), ('address', 'İşletmeci adresi'),
        ('registration', 'İşletme kayıt numarası'))}
    with json_lock:
        temporary_path = BUSINESS_PATH + '.tmp'
        with open(temporary_path, 'w', encoding='utf-8') as file:
            json.dump(business, file, ensure_ascii=False, indent=2)
        os.replace(temporary_path, BUSINESS_PATH)
    return business


def required_text(value, label, max_length=180):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} boş olamaz.')
    value = ' '.join(value.split())
    if len(value) > max_length:
        raise ValueError(f'{label} en fazla {max_length} karakter olabilir.')
    return value


def optional_text(value, label, max_length=180):
    if value is None:
        return ''
    if not isinstance(value, str):
        raise ValueError(f'{label} metin olmalıdır.')
    value = ' '.join(value.split())
    if len(value) > max_length:
        raise ValueError(f'{label} en fazla {max_length} karakter olabilir.')
    return value


def wrap_text(text, font, size, width):
    words = text.split()
    lines = []
    line = ''
    for word in words:
        candidate = f'{line} {word}'.strip()
        if pdfmetrics.stringWidth(candidate, font, size) <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            if pdfmetrics.stringWidth(word, font, size) > width:
                raise ValueError(f'Etikete sığmayan uzun sözcük: {word[:35]}')
            line = word
    if line:
        lines.append(line)
    return lines


def draw_lines(c, text, x, y, width, font='Label-Regular', size=BODY_SIZE,
               max_lines=2, line_height=LINE_HEIGHT, center=False):
    lines = wrap_text(text, font, size, width)
    if len(lines) > max_lines:
        raise ValueError(f'Etiket alanına sığmıyor: {text[:45]}... Metni kısaltın.')
    c.setFont(font, size)
    for line in lines:
        if center:
            c.drawCentredString(x + width / 2, y, line)
        else:
            c.drawString(x, y, line)
        y -= line_height
    return y


def draw_ingredients(c, ingredients, allergens, x, y, width):
    if not ingredients:
        return y

    terms = [term.strip() for term in allergens.split(',') if term.strip()]
    if terms:
        pattern = re.compile('(' + '|'.join(re.escape(term) for term in sorted(terms, key=len, reverse=True)) + ')', re.IGNORECASE)
        chunks = pattern.split(ingredients)
        marked = ''.join('<b>' + escape(chunk) + '</b>' if pattern.fullmatch(chunk) else escape(chunk)
                         for chunk in chunks)
    else:
        marked = escape(ingredients)
    paragraph = Paragraph('İçindekiler: ' + marked,
                          ParagraphStyle('ingredients', fontName='Label-Regular',
                                         fontSize=BODY_SIZE, leading=LINE_HEIGHT))
    _, height = paragraph.wrap(width, 1000)
    if height > 3 * LINE_HEIGHT:
        raise ValueError('İçindekiler etikete sığmıyor. Metni kısaltın.')
    paragraph.drawOn(c, x, y - height + LINE_HEIGHT - 2)
    return y - height


def draw_tett(c, date, x, y, width, line_height=LINE_HEIGHT):
    text = 'TETT: ' + date
    if pdfmetrics.stringWidth(text, 'Label-Bold', BODY_SIZE) > width:
        raise ValueError(f'Etiket alanına sığmıyor: {text}')
    c.setFont('Label-Bold', BODY_SIZE)
    c.drawString(x, y, text)
    c.setLineWidth(0.5)
    c.line(x, y - 2.5, x + width, y - 2.5)
    return y - line_height


def draw_nutrition_table(c, nutrition, x, y, width, columns=2):
    compact_labels = {
        'calories': 'Enerji',
        'fat': 'Yağ',
        'carbohydrate': 'Karb.',
        'sugar': 'Şeker',
        'protein': 'Protein',
        'fiber': 'Lif',
        'sodium': 'Sodyum',
    }
    entries = [(compact_labels[key], nutrition[key]) for key, _ in NUTRITION_FIELDS
               if nutrition.get(key)]
    if not entries:
        return y

    heading_size = 8.2
    value_size = 7.2
    row_height = 7.5
    gap = 2 * mm
    column_width = (width - gap * (columns - 1)) / columns
    c.setFont('Label-Bold', heading_size)
    c.drawString(x, y, 'Besin Değerleri')
    c.setLineWidth(0.3)
    c.line(x, y - 2.5, x + width, y - 2.5)
    y -= 9.5

    c.setFont('Label-Regular', value_size)
    for index, (label, value) in enumerate(entries):
        column = index % columns
        text = f'{label}: {value}'
        if pdfmetrics.stringWidth(text, 'Label-Regular', value_size) > column_width:
            raise ValueError(f'Besin değeri etikete sığmıyor: {text}')
        c.drawString(x + column * (column_width + gap), y, text)
        if column == columns - 1 or index == len(entries) - 1:
            y -= row_height
    return y


def draw_label(c, x, y, width, height, item, common):
    pad = 3 * mm
    wide_label = width > 120 * mm
    logo_zone_width = (26 if wide_label else 18) * mm
    logo_height = (20 if wide_label else 15) * mm
    logo_draw_width = logo_height * logo_source_width / logo_source_height
    logo_x = x + pad + (logo_zone_width - logo_draw_width) / 2
    draw_logo(c, logo_x, y + height - pad - logo_height, logo_height)

    gap = 4 * mm
    lx = x + pad + logo_zone_width + 2 * mm
    inner = x + width - pad - lx
    left_w = (45 if wide_label else 35) * mm
    right_w = inner - left_w - gap
    rx = lx + left_w + gap
    top = y + height - pad - (5 if wide_label else 10)
    bottom = y + pad + (1 if wide_label else 2)
    detail_line_height = 9 if item.get('nutrition') else (10 if wide_label else LINE_HEIGHT)

    name = item['spice']
    weight = item['weight']
    title = f'{name}   {weight}'
    title_size = 12
    if pdfmetrics.stringWidth(title, 'Label-Bold', title_size) > inner:
        title_size = 10
    if pdfmetrics.stringWidth(title, 'Label-Bold', title_size) > inner:
        raise ValueError(f'Ürün adı ve gramaj etikete sığmıyor: {name}')
    c.setFont('Label-Bold', title_size)
    c.drawCentredString(lx + inner / 2, top, title)
    c.setLineWidth(0.35)
    c.line(lx, top - 4, x + width - pad, top - 4)

    left_y = top - (13 if wide_label else 17)
    left_y = draw_ingredients(c, item['ingredients'], item['allergens'], lx, left_y, left_w)
    if item['allergens']:
        left_y = draw_lines(c, 'Alerjen: ' + item['allergens'], lx, left_y, left_w,
                            font='Label-Bold', max_lines=2, line_height=detail_line_height)
    left_y = draw_lines(c, 'Menşei: ' + item['origin'], lx, left_y, left_w,
                        max_lines=1 if wide_label else 2, line_height=detail_line_height)
    left_y = draw_lines(c, 'Muhafaza: ' + item['storage'], lx, left_y, left_w,
                        max_lines=3, line_height=detail_line_height)

    right_y = top - (13 if wide_label else 17)
    right_y = draw_tett(c, item['date'], rx, right_y, right_w,
                        line_height=detail_line_height)
    right_y = draw_lines(c, LOT_STATEMENT, rx, right_y, right_w,
                         max_lines=2 if wide_label else 3, line_height=detail_line_height)
    right_y = draw_lines(c, 'İşletmeci: ' + common['operator'],
                         rx, right_y, right_w, max_lines=2 if wide_label else 3,
                         line_height=detail_line_height)
    right_y = draw_lines(c, 'Adres: ' + common['address'], rx, right_y, right_w,
                         max_lines=3 if wide_label else 4, line_height=detail_line_height)
    right_y = draw_lines(c, ('Kayıt no: ' if wide_label else 'İşletme kayıt no: ') + common['registration'],
                         rx, right_y, right_w, max_lines=2, line_height=detail_line_height)
    nutrition_y = min(left_y, right_y)
    if item.get('nutrition'):
        nutrition_y = draw_nutrition_table(
            c, item['nutrition'], lx, nutrition_y - 2, inner,
            columns=4 if wide_label else 3)
    if min(left_y, right_y, nutrition_y) < bottom:
        raise ValueError(f'{name} için bilgiler yatay etikete sığmıyor. Metinleri kısaltın.')


def draw_vertical_label(c, width, height, item, common):
    pad = 4 * mm
    x = pad
    text_width = width - 2 * pad
    vertical_logo_height = 34 * mm * logo_source_height / logo_source_width
    vertical_logo_width = 75 * mm
    vertical_logo_x = width / 2 - vertical_logo_width * LOGO_ARTWORK_CENTER_X / logo_source_width
    detail_line_height = 9 if item.get('nutrition') else 10
    draw_logo(c, vertical_logo_x,
              height - pad - vertical_logo_height, vertical_logo_height,
              width=vertical_logo_width)
    y = height - pad - vertical_logo_height - 3 * mm
    bottom = pad + 5

    y = draw_lines(c, f"{item['spice']}   {item['weight']}", x, y, text_width,
                   font='Label-Bold', size=13, max_lines=2, center=True)
    c.setLineWidth(0.4)
    c.line(x, y + 2, width - pad, y + 2)
    y -= 6

    y = draw_ingredients(c, item['ingredients'], item['allergens'], x, y, text_width)
    if item['allergens']:
        y = draw_lines(c, 'Alerjen: ' + item['allergens'], x, y, text_width,
                       font='Label-Bold', max_lines=2, line_height=detail_line_height)
    y = draw_lines(c, 'Menşei: ' + item['origin'], x, y, text_width,
                   max_lines=2, line_height=detail_line_height)
    y = draw_lines(c, 'Muhafaza: ' + item['storage'], x, y, text_width,
                   max_lines=3, line_height=detail_line_height)

    c.line(x, y + 6, width - pad, y + 6)
    y -= 4
    y = draw_tett(c, item['date'], x, y, text_width,
                  line_height=detail_line_height)
    y = draw_lines(c, LOT_STATEMENT, x, y, text_width,
                   max_lines=3, line_height=detail_line_height)
    y = draw_lines(c, 'İşletmeci: ' + common['operator'], x, y, text_width,
                   max_lines=3, line_height=detail_line_height)
    y = draw_lines(c, 'Adres: ' + common['address'], x, y, text_width,
                   max_lines=4, line_height=detail_line_height)
    y = draw_lines(c, 'İşletme kayıt no: ' + common['registration'],
                   x, y, text_width, max_lines=2, line_height=detail_line_height)
    if item.get('nutrition'):
        y = draw_nutrition_table(c, item['nutrition'], x, y - 2, text_width, columns=2)
    if y < bottom:
        raise ValueError(f"{item['spice']} için bilgiler dikey etikete sığmıyor. Metinleri kısaltın.")


def create_labels_pdf(cart, common, orientation):
    page_size = landscape(A4) if orientation == 'landscape' else A4
    width, height = page_size
    label_w, label_h = width / 2, height / 5
    output = io.BytesIO()
    pdf = canvas.Canvas(output, pagesize=page_size)
    for item in cart:
        for _ in range(item['pages']):
            for row in range(5):
                for col in range(2):
                    cell_x = col * label_w
                    cell_y = height - (row + 1) * label_h
                    if orientation == 'vertical_label':
                        pdf.saveState()
                        pdf.translate(cell_x + label_w, cell_y)
                        pdf.rotate(90)
                        label_clip = pdf.beginPath()
                        label_clip.rect(0, 0, label_h, label_w)
                        pdf.clipPath(label_clip, stroke=0, fill=0)
                        draw_vertical_label(pdf, label_h, label_w, item, common)
                        pdf.restoreState()
                    else:
                        draw_label(pdf, cell_x, cell_y, label_w, label_h, item, common)
            pdf.showPage()
    pdf.save()
    output.seek(0)
    return output


def prepare_pdf_from_request():
    data = request.get_json(silent=True) or {}
    orientation = data.get('orientation', 'landscape')
    if orientation not in ('landscape', 'portrait', 'vertical_label'):
        raise ValueError('Geçersiz baskı yönü.')
    raw_cart = data.get('cart')
    if not isinstance(raw_cart, list) or not raw_cart or len(raw_cart) > 100:
        raise ValueError('Sepet 1-100 kalem içermelidir.')
    raw_common = data.get('common') or load_business_settings()
    if not isinstance(raw_common, dict):
        raise ValueError('Ortak etiket bilgileri geçersiz.')
    common = {key: required_text(raw_common.get(key), label) for key, label in (
        ('operator', 'İşletmeci adı'), ('address', 'İşletmeci adresi'),
        ('registration', 'İşletme kayıt numarası'))}
    cart = []
    total_pages = 0
    for raw in raw_cart:
        if not isinstance(raw, dict):
            raise ValueError('Sepet öğesi geçersiz.')
        pages = raw.get('pages')
        if isinstance(pages, bool) or not isinstance(pages, int) or not 1 <= pages <= 100:
            raise ValueError('Sayfa sayısı 1-100 arasında olmalıdır.')
        item = {key: required_text(raw.get(key), label) for key, label in (
            ('spice', 'Ürün adı'), ('weight', 'Gramaj'),
            ('origin', 'Menşei'), ('date', 'TETT'))}
        item['ingredients'] = optional_text(raw.get('ingredients'), 'İçindekiler')
        item['storage'] = required_text(raw.get('storage') or DEFAULT_STORAGE, 'Muhafaza koşulu')
        try:
            item['date'] = datetime.strptime(item['date'], '%Y-%m-%d').strftime('%d.%m.%Y')
        except ValueError:
            raise ValueError('TETT geçerli bir gün/ay/yıl olmalıdır.') from None
        if raw.get('verified') is not True:
            raise ValueError(f"{item['spice']} için ürün bilgilerini doğrulayın.")
        item['allergens'] = str(raw.get('allergens') or '').strip()
        if len(item['allergens']) > 120:
            raise ValueError('Alerjen bilgisi çok uzun.')
        raw_nutrition = raw.get('nutrition', {})
        if raw_nutrition is None:
            raw_nutrition = {}
        if not isinstance(raw_nutrition, dict):
            raise ValueError('Besin değerleri geçersiz.')
        item['nutrition'] = {}
        for key, label in NUTRITION_FIELDS:
            raw_value = raw_nutrition.get(key)
            if raw_value is not None and not isinstance(raw_value, str):
                raise ValueError(f'{label} metin olarak girilmelidir.')
            value = ' '.join((raw_value or '').split())
            if len(value) > 40:
                raise ValueError(f'{label} en fazla 40 karakter olabilir.')
            if value:
                item['nutrition'][key] = value
        item['pages'] = pages
        cart.append(item)
        total_pages += pages
    if total_pages > 500:
        raise ValueError('Bir seferde en fazla 500 sayfa oluşturulabilir.')
    return create_labels_pdf(cart, common, orientation), orientation


@app.route('/')
def index():
    data = load_json_data()
    return render_template('index.html', baharat_listesi=data.get('baharatlar', []),
                           gramaj_listesi=data.get('gramajlar', []), profiles=SPICE_PROFILES,
                           business=load_business_settings(), default_storage=DEFAULT_STORAGE)


@app.route('/save-business', methods=['POST'])
def save_business():
    try:
        data = request.get_json(silent=True) or {}
        if not isinstance(data, dict):
            raise ValueError('İşletme bilgileri geçersiz.')
        business = save_business_settings(data)
        return jsonify(success=True, message='İşletme bilgileri kaydedildi.', business=business)
    except ValueError as exc:
        return jsonify(success=False, message=str(exc)), 400


@app.route('/preview-cart', methods=['POST'])
def preview_cart():
    try:
        pdf, _ = prepare_pdf_from_request()
        return send_file(pdf, mimetype='application/pdf', as_attachment=True,
                         download_name='etiket-onizleme.pdf')
    except ValueError as exc:
        return jsonify(success=False, message=str(exc)), 400


@app.route('/print-cart', methods=['POST'])
def handle_print_cart():
    try:
        pdf, orientation = prepare_pdf_from_request()
        path = os.path.join(BASE_DIR, 'etiket.pdf')
        with open(path, 'wb') as file:
            file.write(pdf.getvalue())
        if sys.platform == 'win32':
            os.startfile(path, 'print')
        else:
            subprocess.run(['lp', '-o', 'media=A4', '-o', 'print-scaling=none', path],
                           check=True, capture_output=True, text=True)
        return jsonify(success=True, message=f'{orientation} etiketler yazıcıya gönderildi.')
    except ValueError as exc:
        return jsonify(success=False, message=str(exc)), 400
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = exc.stderr.strip() if isinstance(exc, subprocess.CalledProcessError) else str(exc)
        return jsonify(success=False, message=f'Yazıcıya gönderilemedi: {detail}'), 503


@app.route('/add-spice', methods=['POST'])
def add_spice():
    try:
        name = required_text((request.get_json(silent=True) or {}).get('spice_name'), 'Baharat adı', 60).upper()
        data = load_json_data()
        spices = data.setdefault('baharatlar', [])
        if name in spices:
            return jsonify(success=False, message='Bu baharat zaten listede var.'), 400
        spices.append(name)
        spices.sort()
        save_json_data(data)
        return jsonify(success=True, message=f'{name} eklendi.')
    except ValueError as exc:
        return jsonify(success=False, message=str(exc)), 400


@app.route('/add-weight', methods=['POST'])
def add_weight():
    try:
        weight = required_text((request.get_json(silent=True) or {}).get('weight_name'), 'Gramaj', 30).upper()
        data = load_json_data()
        weights = data.setdefault('gramajlar', [])
        if weight in weights:
            return jsonify(success=False, message='Bu gramaj zaten listede var.'), 400
        weights.append(weight)
        save_json_data(data)
        return jsonify(success=True, message=f'{weight} eklendi.')
    except ValueError as exc:
        return jsonify(success=False, message=str(exc)), 400


@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory(STATIC_PATH, 'manifest.json')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_PATH, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '5000')))
