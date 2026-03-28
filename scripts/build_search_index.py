#!/usr/bin/env python3
"""
ヒーロー検索用の軽量インデックスを生成。
メーカー名・銘柄名・地域・リキュールタイプで検索可能にする。
"""
import json, glob, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PREF_NAMES = {
    'hokkaido':'北海道','aomori':'青森','iwate':'岩手','miyagi':'宮城','akita':'秋田',
    'yamagata':'山形','fukushima':'福島','ibaraki':'茨城','tochigi':'栃木','gunma':'群馬',
    'saitama':'埼玉','chiba':'千葉','tokyo':'東京','kanagawa':'神奈川','niigata':'新潟',
    'toyama':'富山','ishikawa':'石川','fukui':'福井','yamanashi':'山梨','nagano':'長野',
    'gifu':'岐阜','shizuoka':'静岡','aichi':'愛知','mie':'三重','shiga':'滋賀',
    'kyoto':'京都','osaka':'大阪','hyogo':'兵庫','nara':'奈良','wakayama':'和歌山',
    'tottori':'鳥取','shimane':'島根','okayama':'岡山','hiroshima':'広島','yamaguchi':'山口',
    'tokushima':'徳島','kagawa':'香川','ehime':'愛媛','kochi':'高知','fukuoka':'福岡',
    'saga':'佐賀','nagasaki':'長崎','kumamoto':'熊本','oita':'大分','miyazaki':'宮崎',
    'kagoshima':'鹿児島','okinawa':'沖縄'
}

LIQUEUR_TYPE_JA = {
    'umeshu': '梅酒', 'yuzu': 'ゆず酒', 'peach': '桃酒',
    'mikan': 'みかん酒', 'strawberry': 'いちご酒', 'matcha': '抹茶リキュール',
    'sakura': '桜リキュール', 'melon': 'メロンリキュール', 'yogurt': 'ヨーグルト酒',
    'other': 'リキュール',
}

index = []
for jf in sorted(glob.glob(os.path.join(BASE, 'data', 'data_*_liqueurs.json'))):
    pref = os.path.basename(jf).replace('data_', '').replace('_liqueurs.json', '')
    pref_name = PREF_NAMES.get(pref, pref)
    for d in json.load(open(jf, 'r', encoding='utf-8')):
        if not d.get('id'):
            continue

        brand_names = []
        for br in d.get('brands', []):
            if isinstance(br, dict):
                if br.get('name'): brand_names.append(br['name'])
                if br.get('type'): brand_names.append(br['type'])
            elif isinstance(br, str):
                brand_names.append(br)

        if d.get('brand') and d['brand'] not in brand_names:
            brand_names.insert(0, d['brand'])

        lt = d.get('liqueur_type', '')
        lt_ja = LIQUEUR_TYPE_JA.get(lt, '')

        search_parts = [
            d.get('name', ''), d.get('brand', ''), ' '.join(brand_names),
            d.get('name_en', ''), pref_name, d.get('area', ''),
            d.get('type', ''), lt_ja, d.get('base_spirit', ''),
            d.get('fruit_ingredient', ''), d.get('company', ''),
        ]
        full_text = ' '.join(filter(None, search_parts))

        entry = {
            'id': d['id'], 'n': d.get('name', ''), 'b': d.get('brand', ''),
            'br': ' '.join(brand_names), 'p': pref, 'pn': pref_name,
            'a': d.get('area', ''), 'ne': d.get('name_en', ''),
            't': d.get('type', '') or lt_ja, 'lt': lt,
            'f': full_text, 'fd': d.get('founded', ''),
        }
        index.append(entry)

out = os.path.join(BASE, 'liqueur', 'search_index.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, separators=(',', ':'))

test_queries = ['チョーヤ', '梅酒', 'ゆず', '和歌山', 'choya', '桜リキュール']
for q in test_queries:
    hits = sum(1 for e in index if q.lower() in e['f'].lower())
    print(f'  "{q}" → {hits} hits')

print(f'\nSearch index: {len(index)} entries → {out} ({os.path.getsize(out)//1024} KB)')
