#!/usr/bin/env python3
"""
英語・フランス語版のメーカーページを一括生成。
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
}

def esc(s):
    if not s: return ''
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def jsesc(s):
    if not s: return ''
    return str(s).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")

# Simplified page generator (same structure as regenerate_all_pages but with translated UI)
def generate_lang_page(b, pref_slug, lang):
    t = UI[lang]
    pref_en = PREF_EN.get(pref_slug, pref_slug)
    name = b.get('name', '')
    name_en = b.get('name_en', '')
    display_name = name_en if (name_en and lang == 'en') else name
    bid = b.get('id', '')
    page_url = f"https://{DOMAIN}/liqueur/{lang}/{pref_slug}/{bid}.html"
    desc = b.get('desc', '')
    brand = b.get('brand', '')

    return f'''<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(display_name)} — {t['title_suffix']}</title>
<meta name="description" content="{esc(display_name)} — Japanese liqueur producer in {pref_en}">
<link rel="canonical" href="{page_url}">
<link rel="alternate" hreflang="ja" href="https://{DOMAIN}/liqueur/{pref_slug}/{bid}.html">
<link rel="alternate" hreflang="en" href="https://{DOMAIN}/liqueur/en/{pref_slug}/{bid}.html">
<link rel="alternate" hreflang="fr" href="https://{DOMAIN}/liqueur/fr/{pref_slug}/{bid}.html">
<link rel="alternate" hreflang="x-default" href="https://{DOMAIN}/liqueur/en/{pref_slug}/{bid}.html">
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
    <a class="lb{' active' if lang == 'fr' else ''}" href="/liqueur/fr/{pref_slug}/{bid}.html">FR</a>
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
<script>
function openPanel(){{document.getElementById('overlay').classList.add('open');document.getElementById('fab').style.display='none';if(!ci)initChat();}}
function closePanel(){{document.getElementById('overlay').classList.remove('open');document.getElementById('fab').style.display='flex';}}
let ci=false;
function initChat(){{ci=true;addMsg('butler','{t["sakura_greet"].format(name=jsesc(name))}');}}
function addMsg(r,t){{const c=document.getElementById('chat'),d=document.createElement('div');d.className='msg '+r;d.innerHTML='<div class="av">'+(r==='butler'?'桜':'👤')+'</div><div class="bubble">'+t.replace(/\\n/g,'<br>')+'</div>';c.appendChild(d);c.scrollTop=c.scrollHeight;}}
function sendMsg(){{const i=document.getElementById('chat-inp'),q=i.value.trim();if(!q)return;i.value='';addMsg('user',q);setTimeout(()=>addMsg('butler','{t["sakura_demo"]}'),1200);}}
</script>
</body>
</html>'''

# Main
json_files = sorted(glob.glob(os.path.join(BASE, 'data', 'data_*_liqueurs.json')))
grand_total = 0

for lang in ['en', 'fr']:
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
                html = generate_lang_page(b, pref, lang)
                with open(os.path.join(out_dir, f"{b['id']}.html"), 'w', encoding='utf-8') as f:
                    f.write(html)
                total += 1
            except Exception as e:
                print(f"  ERROR [{lang}]: {pref}/{b.get('id', '?')} — {e}")
    print(f"{lang.upper()}: {total} pages generated")
    grand_total += total

print(f"\nDone! Total: {grand_total} pages generated (EN + FR)")
