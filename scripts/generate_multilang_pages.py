#!/usr/bin/env python3
"""
英語・フランス語・中国語版のメーカーページを一括生成。
UIラベルのみ翻訳。説明文（desc）は日本語のまま。
"""

import json, glob, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE, 'template_liqueur.html'), 'r') as f:
    tmpl = f.read()
CSS = tmpl[tmpl.find('<style>') + 7:tmpl.find('</style>')]

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

PREF_EN = {
    'hokkaido':'Hokkaido','aomori':'Aomori','iwate':'Iwate','miyagi':'Miyagi','akita':'Akita',
    'yamagata':'Yamagata','fukushima':'Fukushima','ibaraki':'Ibaraki','tochigi':'Tochigi','gunma':'Gunma',
    'saitama':'Saitama','chiba':'Chiba','tokyo':'Tokyo','kanagawa':'Kanagawa','niigata':'Niigata',
    'toyama':'Toyama','ishikawa':'Ishikawa','fukui':'Fukui','yamanashi':'Yamanashi','nagano':'Nagano',
    'gifu':'Gifu','shizuoka':'Shizuoka','aichi':'Aichi','mie':'Mie','shiga':'Shiga',
    'kyoto':'Kyoto','osaka':'Osaka','hyogo':'Hyogo','nara':'Nara','wakayama':'Wakayama',
    'tottori':'Tottori','shimane':'Shimane','okayama':'Okayama','hiroshima':'Hiroshima','yamaguchi':'Yamaguchi',
    'tokushima':'Tokushima','kagawa':'Kagawa','ehime':'Ehime','kochi':'Kochi','fukuoka':'Fukuoka',
    'saga':'Saga','nagasaki':'Nagasaki','kumamoto':'Kumamoto','oita':'Oita','miyazaki':'Miyazaki',
    'kagoshima':'Kagoshima','okinawa':'Okinawa'
}

UI = {
    'en': {
        'html_lang': 'en', 'title_suffix': 'Terroir HUB LIQUEUR',
        'story_label': 'STORY', 'story_title': 'The Story of {name}',
        'features_label': 'FEATURES', 'features_title': 'Characteristics of {name}',
        'feature_prefix': 'Feature',
        'brands_label': 'LIQUEUR', 'brands_title': 'Signature Products',
        'info_label': 'INFORMATION', 'info_title': 'Information',
        'location': 'Location', 'phone': 'Phone', 'website': 'Website', 'visit': 'Tours',
        'years_history': 'Years of History', 'founded_text': 'Founded in {year}.',
        'ask_sakura': 'Ask Sakura', 'official_site': 'Official Website',
        'sakura_title': 'Sakura — AI Concierge', 'sakura_online': 'Online',
        'sakura_placeholder': 'Ask anything about this producer',
        'sakura_greet': 'Welcome to {name}.\\n\\nFeel free to ask anything about this producer.',
        'sug1': 'What is {brand} like?', 'sug2': 'How should I drink this?',
        'sug3': 'What food goes well?', 'sug4': 'Tell me about the history',
        'sakura_demo': 'Thank you for your question.\\n\\n* Sakura AI will provide real answers once connected to the API.',
        'source': 'Source', 'photo': 'PHOTO',
    },
    'fr': {
        'html_lang': 'fr', 'title_suffix': 'Terroir HUB LIQUEUR',
        'story_label': 'HISTOIRE', 'story_title': "L'histoire de {name}",
        'features_label': 'CARACTERISTIQUES', 'features_title': 'Les caracteristiques de {name}',
        'feature_prefix': 'Caracteristique',
        'brands_label': 'LIQUEUR', 'brands_title': 'Produits Signature',
        'info_label': 'INFORMATIONS', 'info_title': 'Informations',
        'location': 'Adresse', 'phone': 'Telephone', 'website': 'Site web', 'visit': 'Visite',
        'years_history': "Ans d'histoire", 'founded_text': 'Fondee en {year}.',
        'ask_sakura': 'Demander a Sakura', 'official_site': 'Site officiel',
        'sakura_title': 'Sakura — Concierge IA', 'sakura_online': 'En ligne',
        'sakura_placeholder': 'Posez vos questions sur ce producteur',
        'sakura_greet': "Bienvenue chez {name}.\\n\\nN'hesitez pas a poser vos questions.",
        'sug1': 'Comment est le {brand} ?', 'sug2': 'Comment le deguster ?',
        'sug3': 'Quels accords mets ?', 'sug4': "Quelle est l'histoire ?",
        'sakura_demo': "Merci pour votre question.\\n\\n* Sakura IA fournira de vraies reponses une fois connectee.",
        'source': 'Source', 'photo': 'PHOTO',
    },
    'zh': {
        'html_lang': 'zh-CN', 'title_suffix': 'Terroir HUB LIQUEUR',
        'story_label': '故事', 'story_title': '{name}的故事',
        'features_label': '特色', 'features_title': '{name}的特色',
        'feature_prefix': '特色',
        'brands_label': 'LIQUEUR', 'brands_title': '代表品牌',
        'info_label': 'INFORMATION', 'info_title': '基本信息',
        'location': '地址', 'phone': '电话', 'website': '网站', 'visit': '参观',
        'years_history': '年历史', 'founded_text': '创立于{year}年。',
        'ask_sakura': '问樱花', 'official_site': '官方网站',
        'sakura_title': '樱花 — AI礼宾', 'sakura_online': '在线',
        'sakura_placeholder': '关于这家生产商，您可以随意提问',
        'sakura_greet': '欢迎来到{name}。\\n\\n请随意提问关于这家生产商的任何问题。',
        'sug1': '{brand}是什么样的？', 'sug2': '推荐的饮用方式？',
        'sug3': '搭配什么料理？', 'sug4': '请介绍历史',
        'sakura_demo': '感谢您的提问。\\n\\n※ 樱花AI将在连接API后提供真实回答。',
        'source': '来源', 'photo': '照片',
    },
}

def esc(s):
    if not s: return ''
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def jsesc(s):
    if not s: return ''
    return str(s).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")

# Simplified page generator (same structure as regenerate_all_pages but with translated UI)
def generate_lang_page(b, pref_slug, lang, siblings=None):
    t = UI[lang]
    pref_en = PREF_EN.get(pref_slug, pref_slug)
    name = b.get('name', '')
    name_en = b.get('name_en', '')
    display_name = name_en if (name_en and lang == 'en') else name
    bid = b.get('id', '')
    page_url = f"https://{DOMAIN}/liqueur/{lang}/{pref_slug}/{bid}.html"
    desc = b.get('desc', '')
    brand = b.get('brand', '')

    _b_items = b.get('brands') or b.get('products') or b.get('liqueurs') or []
    _bn2 = [str(x.get('name','')) if isinstance(x, dict) else str(x) for x in (_b_items[:5] if isinstance(_b_items, list) else [])]
    _bn2 = [x for x in _bn2 if x]
    _disp = b.get('name_en') or name
    _sug_en = [f'Tell me about {_disp}', 'How should I drink it?', 'Can I visit?', 'What is the history?']
    _sakura_ctx = {
        'lang': lang, 'site': 'TERROIR HUB LIQUEUR (リキュール page, English site)',
        'facility': 'メーカー', 'facility_en': 'maker',
        'name': name, 'display_name': _disp, 'brand': b.get('brand',''),
        'pref': pref_slug, 'area': b.get('area','') or '',
        'founded': b.get('founded',''), 'brands': _bn2,
        'url': b.get('url',''), 'desc': b.get('desc',''),
        'suggestions': _sug_en,
    }
    # ── JSON-LD + 同県リンク（en）──
    import json as _json3
    _founded = str(b.get('founded','') or '')
    _url0 = b.get('url','') or ''
    _page_url2 = f"https://{DOMAIN}/liqueur/{lang}/{pref_slug}/{bid}.html"
    _biz = {
        "@type": "LocalBusiness",
        "name": _disp,
        "url": _page_url2,
        "address": {"@type": "PostalAddress", "addressRegion": pref_en, "addressCountry": "JP"},
    }
    if b.get('name_en') and b.get('name_en') != name:
        _biz["alternateName"] = name
    if _founded: _biz["foundingDate"] = _founded
    if _url0: _biz["sameAs"] = _url0
    if _bn2: _biz["brand"] = {"@type": "Brand", "name": _bn2[0]}
    _crumb = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Terroir HUB", "item": f"https://{DOMAIN}/en/"},
        {"@type": "ListItem", "position": 2, "name": pref_en, "item": f"https://{DOMAIN}/liqueur/{lang}/{pref_slug}/"},
        {"@type": "ListItem", "position": 3, "name": _disp, "item": _page_url2}]}
    _faq2 = []
    if _bn2:
        _faq2.append({"@type": "Question", "name": f"What does {_disp} produce?",
                      "acceptedAnswer": {"@type": "Answer", "text": f"{_disp} produces {', '.join(_bn2)}."}})
    if _founded.isdigit():
        _faq2.append({"@type": "Question", "name": f"When was {_disp} founded?",
                      "acceptedAnswer": {"@type": "Answer", "text": f"{_disp} was founded in {_founded} in {pref_en}, Japan."}})
    if _url0:
        _faq2.append({"@type": "Question", "name": f"Does {_disp} have an official website?",
                      "acceptedAnswer": {"@type": "Answer", "text": f"Yes, the official website is {_url0}."}})
    _graph2 = [_biz, _crumb]
    if _faq2: _graph2.append({"@type": "FAQPage", "mainEntity": _faq2})
    _ml_jsonld = '<script type="application/ld+json">' + _json3.dumps({"@context": "https://schema.org", "@graph": _graph2}, ensure_ascii=False) + '</script>'

    _ml_related = ''
    if siblings:
        _o2 = [x for x in siblings if isinstance(x, dict) and x.get('id') and x.get('id') != bid and x.get('name')]
        _o2.sort(key=lambda x: x.get('name_en') or x.get('name',''))
        _rc = ''
        for _x in _o2[:6]:
            _xn = esc(_x.get('name_en') or _x.get('name',''))
            _xb = esc(_x.get('brand',''))
            _rc += (f'<a href="/liqueur/en/{pref_slug}/{esc(_x["id"])}.html" '
                    f'style="display:flex;flex-direction:column;gap:5px;background:var(--surface,#fff);border:1px solid var(--border,#E7DFD5);border-radius:8px;padding:16px 18px;text-decoration:none;color:inherit;">'
                    f'<span style="font-size:15px;font-weight:600;">{_xn}</span>'
                    f'<span style="font-size:11.5px;opacity:.6;">{_xb}</span></a>')
        if _rc:
            _ml_related = (f'<section class="section" style="padding:60px 24px;max-width:1100px;margin:0 auto;">'
                           f'<h2 style="font-size:22px;margin-bottom:18px;">More makers in {pref_en}</h2>'
                           f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;">{_rc}</div>'
                           f'<div style="margin-top:20px;"><a href="/liqueur/en/{pref_slug}/" style="font-size:13px;">See all →</a></div>'
                           f'</section>')

    # ── 銘柄 + 基本情報セクション（en）──
    _ml_extra = ''
    _bl = ''
    for _bx in (_b_items[:4] if isinstance(_b_items, list) else []):
        if isinstance(_bx, dict):
            _bxn = esc(str(_bx.get('name','')))
            _bxt = esc(str(_bx.get('type','') or _bx.get('specs','') or ''))
        else:
            _bxn, _bxt = esc(str(_bx)), ''
        if not _bxn: continue
        _bl += ('<div style="background:#fff;border:1px solid #F0D5E0;border-radius:8px;padding:18px;">'
                + f'<div style="font-size:16px;font-weight:600;">{_bxn}</div>'
                + (f'<div style="font-size:12px;opacity:.65;margin-top:4px;">{_bxt}</div>' if _bxt else '') + '</div>')
    if _bl:
        _ml_extra += ('<section style="padding:50px 24px;max-width:1100px;margin:0 auto;">'
                      '<h2 style="font-size:22px;margin-bottom:16px;">Products</h2>'
                      + f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;">{_bl}</div></section>')
    _info = ''
    _addr = b.get('address','') or ''
    _tel = b.get('tel','') or ''
    _visit = b.get('visit','') or ''
    if _addr: _info += f'<div style="margin-bottom:10px;"><strong>Location:</strong> {esc(_addr)}</div>'
    if _tel: _info += f'<div style="margin-bottom:10px;"><strong>Phone:</strong> {esc(_tel)}</div>'
    if _url0: _info += f'<div style="margin-bottom:10px;"><strong>Official website:</strong> <a href="{esc(_url0)}" rel="noopener" target="_blank">{esc(_url0)}</a></div>'
    if _visit and _visit not in ('—','ー','-'): _info += f'<div style="margin-bottom:10px;"><strong>Visit:</strong> {esc(_visit)}</div>'
    if _founded: _info += f'<div style="margin-bottom:10px;"><strong>Founded:</strong> {esc(_founded)}</div>'
    if _info:
        _ml_extra += ('<section style="padding:30px 24px 60px;max-width:1100px;margin:0 auto;">'
                      '<h2 style="font-size:22px;margin-bottom:16px;">Information</h2>'
                      + f'<div style="font-size:14px;line-height:1.9;">{_info}</div></section>')

    import json as _json2
    sakura_block = _ml_jsonld + ('<script>window.SAKURA_CTX = '
                    + _json2.dumps(_sakura_ctx, ensure_ascii=False).replace('</', '<\\/')
                    + ';</script>\n<script src="/sakura-page.js" defer></script>')

    return f'''<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{'<meta name="robots" content="noindex,follow">' if lang == 'en' else ''}<title>{esc(display_name)} — {t['title_suffix']}</title>
<meta name="description" content="{esc(display_name)} — Japanese liqueur producer in {pref_en}">
<meta property="og:title" content="{esc(display_name)} — {t['title_suffix']}">
<meta property="og:description" content="{esc(display_name)} — Japanese liqueur producer in {pref_en}">
<meta property="og:type" content="website">
<meta property="og:url" content="{page_url}">
<link rel="canonical" href="{page_url}">
<link rel="alternate" hreflang="ja" href="https://{DOMAIN}/liqueur/{pref_slug}/{bid}.html">
<link rel="alternate" hreflang="x-default" href="https://{DOMAIN}/liqueur/{pref_slug}/{bid}.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=Noto+Serif+JP:wght@200;300;400&family=Zen+Old+Mincho:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
<nav class="nav">
  <a class="nav-brand" href="/"><span class="nav-logo">Terroir HUB</span><span class="nav-logo-sub">LIQUEUR</span></a>
  <div class="nav-r">
    <a class="lb" href="/liqueur/{pref_slug}/{bid}.html">日本語</a>
    <a class="lb{' active' if lang == 'en' else ''}" href="/liqueur/en/{pref_slug}/{bid}.html">EN</a>
  </div>
</nav>
<section class="hero">
  <div class="hero-bg"></div>
  <div class="hero-content">
    <div class="hero-badge"><span class="badge-dot"></span>TERROIR HUB LIQUEUR</div>
    <h1 class="hero-title">{esc(name)}</h1>
    {f'<p class="hero-subtitle">{esc(brand)}</p>' if brand else ''}
    {f'<p class="hero-tagline">{esc(desc)}</p>' if desc else ''}
    <div class="hero-actions">
      <button class="btn-p" onclick="openPanel()">{t['ask_sakura']}</button>
    </div>
  </div>
</section>
<script src="/liqueur/track.js" defer></script>
{_ml_extra}
{_ml_related}
<footer style="background:#8B2252;padding:40px 24px;text-align:center;">
  <p style="font-family:'Zen Old Mincho',serif;font-size:14px;color:rgba(255,255,255,0.5);letter-spacing:0.08em;margin-bottom:8px;">Terroir HUB</p>
  <p style="font-size:11px;color:rgba(255,255,255,0.2);">{DOMAIN}</p>
</footer>
<button class="fab" onclick="openPanel()" id="fab"><span class="fab-pulse"></span><span>🌸</span><span>{t['ask_sakura']}</span></button>
<div class="overlay" id="overlay" onclick="if(event.target===this)closePanel()"><div class="panel"><div class="p-handle"></div>
<div class="p-hdr"><div class="p-hdr-l"><div class="p-av">桜</div><div><div class="p-title">{t['sakura_title']}</div><div class="p-status"><div class="p-dot"></div><span>{t['sakura_online']}</span></div></div></div><button class="p-close" onclick="closePanel()">✕</button></div>
<div class="chat" id="chat"></div><div class="sugs" id="sugs"></div>
<div class="inp-row"><textarea id="chat-inp" rows="1" placeholder="{t['sakura_placeholder']}"></textarea><button id="chat-send" onclick="sendMsg()">↑</button></div>
</div></div>
{sakura_block}
</body>
</html>'''

# Main
json_files = sorted(glob.glob(os.path.join(BASE, 'data', 'data_*_liqueurs.json')))
grand_total = 0

for lang in ['en']:
    total = 0
    for jf in json_files:
        pref = os.path.basename(jf).replace('data_', '').replace('_liqueurs.json', '')
        with open(jf, 'r', encoding='utf-8') as f:
            producers = json.load(f)
        out_dir = os.path.join(BASE, 'liqueur', lang, pref)
        os.makedirs(out_dir, exist_ok=True)
        for b in producers:
            if not b.get('id'): continue
            try:
                html = generate_lang_page(b, pref, lang, siblings=producers)
                with open(os.path.join(out_dir, f"{b['id']}.html"), 'w', encoding='utf-8') as f:
                    f.write(html)
                total += 1
            except Exception as e:
                print(f"  ERROR [{lang}]: {pref}/{b.get('id', '?')} — {e}")
    print(f"{lang.upper()}: {total} pages generated")
    grand_total += total

print(f"\nDone! Total: {grand_total} pages generated (EN + FR + ZH)")
