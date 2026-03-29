#!/usr/bin/env python3
"""
sitemap.xmlを全ページから自動生成。
"""

import json
import glob
import os
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = 'https://liqueur.terroirhub.com'
TODAY = date.today().isoformat()

GUIDE_PAGES = ['index','types','production','drinking','pairing','history','umeshu','glossary']
REGIONS = ['hokkaido','tohoku','kanto','chubu','kinki','chugoku','shikoku','kyushu']

# English blog posts
EN_BLOG_POSTS = ['what-is-umeshu','best-japanese-liqueurs','umeshu-vs-plum-wine','japanese-yuzu-liqueur']
FR_BLOG_POSTS = ['quest-ce-que-umeshu','meilleurs-liqueurs-japonaises','liqueur-yuzu-japonaise']
ZH_BLOG_POSTS = ['what-is-umeshu','best-japanese-liqueurs']

urls = []

def add(loc, priority, changefreq='monthly', langs=None):
    urls.append({'loc': loc, 'priority': priority, 'changefreq': changefreq, 'langs': langs})

add('/', '1.0', 'weekly', {'ja': '/', 'en': '/en/'})
add('/en/', '0.9', 'weekly')

# Guide pages (JA)
for g in GUIDE_PAGES:
    path = f'/liqueur/guide/{g}.html' if g != 'index' else '/liqueur/guide/'
    en_path = f'/liqueur/guide/en/{g}.html' if g != 'index' else '/liqueur/guide/en/'
    langs = {'ja': path, 'en': en_path}
    add(path, '0.9', 'monthly', langs)

# Guide pages (EN)
for g in GUIDE_PAGES:
    path = f'/liqueur/guide/en/{g}.html' if g != 'index' else '/liqueur/guide/en/'
    ja_path = f'/liqueur/guide/{g}.html' if g != 'index' else '/liqueur/guide/'
    langs = {'ja': ja_path, 'en': path}
    add(path, '0.8', 'monthly', langs)

# Region pages
for r in REGIONS:
    add(f'/liqueur/region/{r}.html', '0.8', 'monthly')

# Search page
add('/liqueur/search/', '0.9', 'weekly')

# Awards page
add('/liqueur/awards/', '0.9', 'weekly')

# Blog index pages
add('/liqueur/blog/en/', '0.8', 'weekly', {'en': '/liqueur/blog/en/', 'fr': '/liqueur/blog/fr/', 'zh': '/liqueur/blog/zh/'})
add('/liqueur/blog/fr/', '0.7', 'weekly', {'en': '/liqueur/blog/en/', 'fr': '/liqueur/blog/fr/', 'zh': '/liqueur/blog/zh/'})
add('/liqueur/blog/zh/', '0.7', 'weekly', {'en': '/liqueur/blog/en/', 'fr': '/liqueur/blog/fr/', 'zh': '/liqueur/blog/zh/'})

# Blog posts (EN)
for slug in EN_BLOG_POSTS:
    add(f'/liqueur/blog/en/{slug}.html', '0.7', 'monthly')

# Blog posts (FR)
for slug in FR_BLOG_POSTS:
    add(f'/liqueur/blog/fr/{slug}.html', '0.7', 'monthly')

# Blog posts (ZH)
for slug in ZH_BLOG_POSTS:
    add(f'/liqueur/blog/zh/{slug}.html', '0.7', 'monthly')

# Producer pages
json_files = sorted(glob.glob(os.path.join(BASE, 'data', 'data_*_liqueurs.json')))
for jf in json_files:
    pref = os.path.basename(jf).replace('data_', '').replace('_liqueurs.json', '')
    with open(jf, 'r', encoding='utf-8') as f:
        producers = json.load(f)
    if not producers:
        continue
    add(f'/liqueur/{pref}/', '0.7', 'weekly')
    for d in producers:
        if not d.get('id'):
            continue
        ja_path = f'/liqueur/{pref}/{d["id"]}.html'
        en_path = f'/liqueur/en/{pref}/{d["id"]}.html'
        fr_path = f'/liqueur/fr/{pref}/{d["id"]}.html'
        zh_path = f'/liqueur/zh/{pref}/{d["id"]}.html'
        langs = {'ja': ja_path, 'en': en_path, 'fr': fr_path, 'zh': zh_path}
        add(ja_path, '0.6', 'monthly', langs)
        add(en_path, '0.5', 'monthly', langs)
        add(fr_path, '0.5', 'monthly', langs)
        add(zh_path, '0.5', 'monthly', langs)

xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
xml_parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">')

for u in urls:
    xml_parts.append('  <url>')
    xml_parts.append(f'    <loc>{DOMAIN}{u["loc"]}</loc>')
    xml_parts.append(f'    <lastmod>{TODAY}</lastmod>')
    xml_parts.append(f'    <changefreq>{u["changefreq"]}</changefreq>')
    xml_parts.append(f'    <priority>{u["priority"]}</priority>')
    if u.get('langs'):
        for lang, href in u['langs'].items():
            xml_parts.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{DOMAIN}{href}"/>')
    xml_parts.append('  </url>')

xml_parts.append('</urlset>')

sitemap = '\n'.join(xml_parts)
out_path = os.path.join(BASE, 'sitemap.xml')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f"Sitemap generated: {len(urls)} URLs → sitemap.xml")
