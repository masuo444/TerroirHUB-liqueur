#!/usr/bin/env python3
"""
各県のリキュールメーカー一覧ページ（index.html）を生成。
"""

import json
import glob
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = 'liqueur.terroirhub.com'

PREF_NAMES = {
    'hokkaido':'北海道','aomori':'青森県','iwate':'岩手県','miyagi':'宮城県','akita':'秋田県',
    'yamagata':'山形県','fukushima':'福島県','ibaraki':'茨城県','tochigi':'栃木県','gunma':'群馬県',
    'saitama':'埼玉県','chiba':'千葉県','tokyo':'東京都','kanagawa':'神奈川県','niigata':'新潟県',
    'toyama':'富山県','ishikawa':'石川県','fukui':'福井県','yamanashi':'山梨県','nagano':'長野県',
    'gifu':'岐阜県','shizuoka':'静岡県','aichi':'愛知県','mie':'三重県','shiga':'滋賀県',
    'kyoto':'京都府','osaka':'大阪府','hyogo':'兵庫県','nara':'奈良県','wakayama':'和歌山県',
    'tottori':'鳥取県','shimane':'島根県','okayama':'岡山県','hiroshima':'広島県','yamaguchi':'山口県',
    'tokushima':'徳島県','kagawa':'香川県','ehime':'愛媛県','kochi':'高知県','fukuoka':'福岡県',
    'saga':'佐賀県','nagasaki':'長崎県','kumamoto':'熊本県','oita':'大分県','miyazaki':'宮崎県',
    'kagoshima':'鹿児島県','okinawa':'沖縄県'
}

LIQUEUR_TYPE_LABELS = {
    'umeshu': '梅酒', 'yuzu': 'ゆず酒', 'peach': '桃酒',
    'mikan': 'みかん酒', 'strawberry': 'いちご酒', 'matcha': '抹茶',
    'sakura': '桜', 'melon': 'メロン', 'yogurt': 'ヨーグルト', 'other': 'その他',
}

def esc(s):
    if not s: return ''
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'","&#39;")

def generate_pref_index(pref_slug, producers):
    pref_name = PREF_NAMES.get(pref_slug, pref_slug)
    count = len(producers)
    if count == 0:
        return None

    inline_data = []
    for d in producers:
        inline_data.append({
            'id': d.get('id',''),
            'name': d.get('name',''),
            'brand': d.get('brand',''),
            'type': d.get('type',''),
            'area': d.get('area',''),
            'founded': d.get('founded',''),
            'desc': (d.get('desc','')[:100] + '…') if len(d.get('desc','')) > 100 else d.get('desc',''),
            'liqueur_type': d.get('liqueur_type',''),
        })

    json_str = json.dumps(inline_data, ensure_ascii=False)

    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{pref_name}のリキュールメーカー一覧",
        "numberOfItems": count,
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"https://{DOMAIN}/liqueur/{pref_slug}/{d['id']}.html", "name": d.get('name','')} for i, d in enumerate(producers)]
    }, ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(pref_name)}のリキュールメーカー一覧（{count}社）— Terroir HUB</title>
<meta name="description" content="{esc(pref_name)}のリキュールメーカー{count}社を一覧表示。Terroir HUB LIQUEUR。">
<link rel="canonical" href="https://{DOMAIN}/liqueur/{pref_slug}/">
<script type="application/ld+json">{schema}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600;700&family=Noto+Sans+JP:wght@300;400;500;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#FFFBFC;color:#1A1814;font-family:'Noto Sans JP','DM Sans',sans-serif;font-size:16px;line-height:1.85;}}
.nav{{position:fixed;top:0;left:0;right:0;z-index:100;height:54px;display:flex;align-items:center;justify-content:space-between;padding:0 22px;background:rgba(255,251,252,0.96);backdrop-filter:blur(20px);border-bottom:1px solid #F0D5E0;}}
.nav-brand{{display:flex;align-items:center;gap:9px;text-decoration:none;}}
.nav-logo{{font-family:'Shippori Mincho',serif;font-size:18px;font-weight:700;letter-spacing:0.06em;color:#1A1814;}}
.nav-logo-sub{{font-size:10px;color:#8A8070;letter-spacing:0.06em;margin-left:8px;}}
.main{{max-width:1100px;margin:0 auto;padding:78px 24px 48px;}}
.breadcrumb{{font-size:13px;color:#8A8070;margin-bottom:24px;}}
.breadcrumb a{{color:#C4547A;text-decoration:none;}}
.header{{margin-bottom:32px;}}
.header h1{{font-family:'Shippori Mincho',serif;font-size:clamp(26px,4vw,36px);font-weight:700;color:#1A1814;margin-bottom:6px;}}
.header .count{{font-size:14px;color:#8A8070;}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}}
@media(max-width:900px){{.grid{{grid-template-columns:repeat(2,1fr);}}}}
@media(max-width:560px){{.grid{{grid-template-columns:1fr;}}}}
.card{{background:#fff;border:1px solid #F0D5E0;border-radius:10px;padding:20px;transition:all 0.2s;text-decoration:none;display:block;color:inherit;}}
.card:hover{{border-color:#C4547A;box-shadow:0 4px 16px rgba(0,0,0,0.04);transform:translateY(-2px);}}
.card-name{{font-family:'Shippori Mincho',serif;font-size:17px;font-weight:600;color:#1A1814;margin-bottom:2px;}}
.card-brand{{font-size:13px;color:#C4547A;font-weight:500;margin-bottom:4px;}}
.card-meta{{font-size:12px;color:#8A8070;margin-bottom:6px;}}
.card-desc{{font-size:12px;color:#8A8070;line-height:1.7;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}}
.tag{{font-size:10px;padding:2px 8px;border-radius:3px;background:rgba(196,84,122,0.06);color:#C4547A;border:1px solid rgba(196,84,122,0.12);}}
footer{{background:#8B2252;padding:32px 24px;text-align:center;margin-top:48px;}}
footer p{{font-size:12px;color:rgba(255,255,255,0.3);}}
footer a{{color:rgba(255,255,255,0.5);text-decoration:none;}}
</style>
</head>
<body>
<nav class="nav">
  <a class="nav-brand" href="/">
    <span class="nav-logo">Terroir HUB</span>
    <span class="nav-logo-sub">LIQUEUR</span>
  </a>
</nav>
<main class="main">
  <div class="breadcrumb">
    <a href="/">ホーム</a> &gt; <a href="/#regions">メーカー検索</a> &gt; {esc(pref_name)}
  </div>
  <div class="header">
    <h1>{esc(pref_name)}のリキュールメーカー</h1>
    <p class="count">{count}社</p>
  </div>
  <div class="grid" id="grid"></div>
</main>
<footer>
  <p><a href="/">Terroir HUB LIQUEUR</a> &copy; 2026 合同会社FOMUS</p>
</footer>
<script>
const B={json_str};
const LABELS={{'umeshu':'梅酒','yuzu':'ゆず酒','peach':'桃酒','mikan':'みかん酒','strawberry':'いちご酒','matcha':'抹茶','sakura':'桜','melon':'メロン','yogurt':'ヨーグルト','other':'その他'}};
document.getElementById('grid').innerHTML=B.map(b=>{{
  return '<a class="card" href="/liqueur/{pref_slug}/'+b.id+'.html">'+
    '<div class="card-name">'+b.name+'</div>'+
    (b.brand?'<div class="card-brand">'+b.brand+'</div>':'')+
    '<div class="card-meta">'+(b.area||'')+(b.founded?' ・ 創業'+b.founded+'年':'')+'</div>'+
    (b.desc?'<div class="card-desc">'+b.desc+'</div>':'')+
    (b.liqueur_type&&LABELS[b.liqueur_type]?'<div style="margin-top:8px;"><span class="tag">'+LABELS[b.liqueur_type]+'</span></div>':'')+
  '</a>';
}}).join('');
</script>
</body>
</html>'''

# Main
json_files = sorted(glob.glob(os.path.join(BASE, 'data', 'data_*_liqueurs.json')))
total = 0

for jf in json_files:
    pref = os.path.basename(jf).replace('data_', '').replace('_liqueurs.json', '')
    with open(jf, 'r', encoding='utf-8') as f:
        producers = json.load(f)

    if not producers:
        print(f"  {pref}: 0 producers (skipped)")
        continue

    html = generate_pref_index(pref, producers)
    if html:
        out_dir = os.path.join(BASE, 'liqueur', pref)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        total += 1
        print(f"  {pref}: {len(producers)} producers → index.html")

print(f"\nDone: {total} prefecture index pages generated")
