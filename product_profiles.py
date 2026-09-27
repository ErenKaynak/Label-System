"""Internet-sourced reference profiles used to prefill the label form.

Nutrition values are per 100 g. Commodity values primarily come from USDA
FoodData Central SR Legacy. They are reference values, not a substitute for
the supplier's formulation, specification or laboratory analysis.
"""


def nutrition(calories=None, fat=None, carbohydrate=None, sugar=None,
              protein=None, fiber=None, sodium=None):
    values = {}
    if calories is not None:
        values['calories'] = f'{calories:g} kcal'
    for key, value, unit in (
        ('fat', fat, 'g'),
        ('carbohydrate', carbohydrate, 'g'),
        ('sugar', sugar, 'g'),
        ('protein', protein, 'g'),
        ('fiber', fiber, 'g'),
        ('sodium', sodium, 'mg'),
    ):
        if value is not None:
            if key == 'sodium' and value >= 1000:
                value, unit = value / 1000, 'g'
            values[key] = f'{value:g} {unit}'
    return values


REFERENCE_NUTRITION = {
    # USDA FoodData Central SR Legacy FDC IDs are included for traceability.
    'black_pepper': (170931, nutrition(251, 3.26, 64, 0.64, 10.4, 25.3, 20)),
    'red_pepper': (170932, nutrition(318, 17.3, 56.6, 10.3, 12, 27.2, 30)),
    'white_pepper': (170933, nutrition(296, 2.12, 68.6, None, 10.4, 26.2, 5)),
    'oregano': (171328, nutrition(265, 4.28, 68.9, 4.09, 9, 42.5, 25)),
    'cumin': (170923, nutrition(375, 22.3, 44.2, 2.25, 17.8, 10.5, 168)),
    'ginger': (170926, nutrition(335, 4.24, 71.6, 3.39, 8.98, 14.1, 27)),
    'bay_leaf': (170917, nutrition(313, 8.36, 75, None, 7.61, 26.3, 23)),
    'curry': (170924, nutrition(325, 14, 55.8, 2.76, 14.3, 53.2, 52)),
    'turmeric': (172231, nutrition(312, 3.25, 67.1, 3.21, 9.68, 22.7, 27)),
    'garlic': (171325, nutrition(331, 0.73, 72.7, 2.43, 16.6, 9, 60)),
    'onion': (171327, nutrition(341, 1.04, 79.1, 6.63, 10.4, 15.2, 73)),
    'allspice': (171315, nutrition(263, 8.69, 72.1, None, 6.09, 21.6, 77)),
    'coriander': (170922, nutrition(298, 17.8, 55, None, 12.4, 41.9, 35)),
    'sesame': (170150, nutrition(573, 49.7, 23.4, 0.3, 17.7, 11.8, 11)),
    'currants': (171724, nutrition(290, 0.22, 77, 62.3, 3.43, 4.4, 43)),
    'coconut': (170170, nutrition(660, 64.5, 23.6, 7.35, 6.88, 16.3, 37)),
    'cinnamon': (171320, nutrition(247, 1.24, 80.6, 2.17, 3.99, 53.1, 10)),
    'cloves': (171321, nutrition(274, 13, 65.5, 2.38, 5.97, 33.9, 277)),
    'mint': (172239, nutrition(285, 6.03, 52, None, 19.9, 29.8, 344)),
    'paprika': (171329, nutrition(282, 12.9, 54, 10.3, 14.1, 34.9, 68)),
    'chili_mix': (171319, nutrition(282, 14.3, 49.7, 7.19, 13.5, 34.8, 2870)),
    'poultry': (171331, nutrition(307, 7.53, 65.6, 1.8, 9.59, 11.3, 27)),
    'bouillon': (171562, nutrition(267, 13.9, 18, 17.4, 16.7, 0, 23900)),
    'corn_flour': (170290, nutrition(361, 3.86, 76.8, 0.64, 6.93, 7.3, 5)),
    'breadcrumbs': (174924, nutrition(266, 3.33, 49.4, 5.67, 8.85, 2.7, 490)),
    'baking_soda': (175040, nutrition(0, 0, 0, 0, 0, 0, 27400)),
    # Single-sample published composition data; calculated energies use Atwater factors.
    # Nigella sativa: Horticulturae 2022, 8(7), 575 (doi:10.3390/horticulturae8070575).
    'nigella': ('Horticulturae 2022, 8, 575', nutrition(539, 39.02, 25.86, None, 21.07, 6.01, None)),
    # Dried Rhus coriaria sample summarized in PMCID PMC9414570.
    'sumac': ('Rhus coriaria review, PMC9414570', nutrition(472, 18.74, 71.21, None, 4.69, None, None)),
    # Unsieved Hibiscus sabdariffa calyx powder from PMCID PMC6526627.
    'hibiscus': ('Hibiscus sabdariffa study, PMC6526627', nutrition(327, 2.39, 69.41, None, 7, None, None)),
    # Pure citric acid; EU/FAO organic-acid conversion factor is 13 kJ/3 kcal per g.
    'citric_acid': ('EU 1169/2011 Annex XIV', nutrition(300, 0, 0, 0, 0, 0, 0)),
}


def profile(ingredients, nutrition_key, note='', allergens=''):
    source, values = REFERENCE_NUTRITION[nutrition_key]
    if isinstance(source, int):
        source_text = f'USDA FoodData Central SR Legacy FDC {source}'
    else:
        source_text = source
    verification = ('100 g besin değerleri referanstır; gerçek ürünün tedarikçi '
                    'spesifikasyonu veya analiz belgesiyle doğrulayın.')
    return {
        'ingredients': ingredients,
        'allergens': allergens,
        'nutrition': values.copy(),
        'note': ' '.join(part for part in (note, f'Kaynak: {source_text}.', verification) if part),
    }


RED_PEPPER_NOTE = ('Yağ ve tuz kullanıldıysa gerçek reçeteye göre içindekilere, '
                   'miktar sırasıyla ekleyin.')
BLEND_NOTE = ('Bu genel bir karışım örneğidir; bileşenleri ve sıralarını satın '
              'aldığınız ürünün etiketi/reçetesiyle değiştirin.')
KEKIK_NOTE = ('Gerçek ürüne göre Origanum, Thymus, Coridothymus veya Satureja '
              'cinsini tedarikçi belgesinden doğrulayın.')


SPICE_PROFILES = {
    'ACI TOZ BİBER': profile('Öğütülmüş acı kırmızıbiber', 'red_pepper', RED_PEPPER_NOTE),
    'ATOM': profile('Acı kırmızıbiber ve baharat karışımı', 'chili_mix', BLEND_NOTE),
    'BEYAZ KARABİBER': profile('Beyaz karabiber (Piper nigrum L.)', 'white_pepper'),
    'ÇÖREK OTU': profile('Çörek otu (Nigella sativa L.)', 'nigella'),
    'DEFNE YAPRAĞI': profile('Kurutulmuş defne yaprağı', 'bay_leaf'),
    'EKSTRA ACI BİBER': profile('Öğütülmüş ekstra acı kırmızıbiber', 'red_pepper', RED_PEPPER_NOTE),
    'GALETE UNU': profile('Buğday unu, su, maya, tuz', 'breadcrumbs',
                          BLEND_NOTE, 'Buğday (gluten)'),
    'HALİS EKSTRA ACI BİBER': profile('Öğütülmüş ekstra acı kırmızıbiber', 'red_pepper', RED_PEPPER_NOTE),
    'HİBİSKUS': profile('Kurutulmuş hibiskus', 'hibiscus'),
    'HİNDİSTAN CEVİZİ': profile('Kurutulmuş Hindistan cevizi', 'coconut'),
    'İPEK PUL BİBER': profile('İpek pul kırmızıbiber', 'paprika', RED_PEPPER_NOTE),
    'İSOT': profile('Kurutulmuş isot biberi', 'red_pepper', RED_PEPPER_NOTE),
    'KAJUN': profile('Paprika, tuz, sarımsak, soğan, acı biber',
                     'chili_mix', BLEND_NOTE),
    'KARABİBER (TEK KULLANIMLIK)': profile('Öğütülmüş karabiber (Piper nigrum L.)', 'black_pepper'),
    'KARABİBER 1': profile('Öğütülmüş karabiber (Piper nigrum L.)', 'black_pepper'),
    'KARABİBER 2': profile('Öğütülmüş karabiber (Piper nigrum L.)', 'black_pepper'),
    'KARABİBER TANE': profile('Tane karabiber (Piper nigrum L.)', 'black_pepper'),
    'KARBONAT': profile('Sodyum bikarbonat', 'baking_soda'),
    'KARANFİL': profile('Karanfil (Syzygium aromaticum)', 'cloves'),
    'KEKİK': profile('Kurutulmuş kekik', 'oregano', KEKIK_NOTE),
    'KİMYON': profile('Kimyon (Cuminum cyminum L.)', 'cumin'),
    'KİMYON 1': profile('Kimyon (Cuminum cyminum L.)', 'cumin'),
    'KİMYON 2': profile('Kimyon (Cuminum cyminum L.)', 'cumin'),
    'KİŞNİŞ': profile('Kişniş tohumu (Coriandrum sativum L.)', 'coriander'),
    'KÖFTE BAHARATI': profile('Kimyon, karabiber, kırmızıbiber, kekik',
                              'chili_mix', BLEND_NOTE),
    'KÖRİ': profile('Zerdeçal, kişniş, kimyon, zencefil, karabiber', 'curry', BLEND_NOTE),
    'KUŞ ÜZÜMÜ': profile('Kurutulmuş kuş üzümü', 'currants'),
    'LİMON TUZU (TANE)': profile('Sitrik asit', 'citric_acid'),
    'LİMON TUZU (TOZ)': profile('Sitrik asit', 'citric_acid'),
    'MISIR UNU': profile('Tam taneli mısır unu', 'corn_flour'),
    'NANE': profile('Kurutulmuş nane (Mentha spp.)', 'mint'),
    'PUL BİBER': profile('Pul kırmızıbiber', 'red_pepper', RED_PEPPER_NOTE),
    'PUL BİBER (TEK KULLANIMLIK)': profile('Pul kırmızıbiber', 'red_pepper', RED_PEPPER_NOTE),
    'SARIMSAK GRANÜR': profile('Granül sarımsak', 'garlic'),
    'SEBZELİ ÇEŞNİ': profile('Tuz, sebzeler, nişasta ve baharatlar', 'bouillon', BLEND_NOTE),
    'SOĞAN GRANÜR': profile('Granül soğan', 'onion'),
    'SUCUK BAHARATI': profile('Kimyon, sarımsak, kırmızıbiber, karabiber',
                              'chili_mix', BLEND_NOTE),
    'SUMAK': profile('Öğütülmüş sumak (Rhus coriaria L.)', 'sumac',
                     'Tuz eklenmişse içindekiler ve besin değerlerini düzeltin.'),
    'SUSAM': profile('Susam tohumu', 'sesame', allergens='Susam'),
    'TARÇIN': profile('Öğütülmüş tarçın', 'cinnamon'),
    'TATLI PUL BİBER': profile('Tatlı pul kırmızıbiber', 'paprika', RED_PEPPER_NOTE),
    'TATLI TOZ BİBER': profile('Öğütülmüş tatlı kırmızıbiber', 'paprika', RED_PEPPER_NOTE),
    'TAVUK BAHARATI': profile('Paprika, karabiber, sarımsak, soğan, kekik',
                              'poultry', BLEND_NOTE),
    'TAVUK-ET BULYON': profile('Tuz, nişasta, yağ, et/tavuk özü, baharat',
                               'bouillon', BLEND_NOTE),
    'TOZ BİBER': profile('Öğütülmüş kırmızıbiber', 'paprika', RED_PEPPER_NOTE),
    'YAĞLI YAPRAK': profile('Pul kırmızıbiber, bitkisel yağ, tuz', 'red_pepper',
                            'Yağın türünü ve bileşen sırasını gerçek reçeteye göre düzeltin.'),
    'YEDİ ÇEŞİT': profile('Yedi çeşit baharat karışımı',
                          'chili_mix', BLEND_NOTE),
    'YENİ BAHAR': profile('Yenibahar (Pimenta dioica)', 'allspice'),
    'ZERDEÇAL': profile('Öğütülmüş zerdeçal (Curcuma longa L.)', 'turmeric'),
    'ZENCEFİL': profile('Öğütülmüş zencefil (Zingiber officinale)', 'ginger'),
}
