#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_faq_to_guide.py
liqueur/guide/ 以下の8HTMLファイルにJSON-LD（BreadcrumbList + FAQPage）を追加する。
既にFAQPageがあればスキップ。
"""

import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDE_DIR = os.path.join(BASE_DIR, "liqueur", "guide")

# 各ページの設定: (ファイル名, パンくず3番目の名前, BreadcrumbListにposition3を含めるか, FAQリスト)
PAGES = [
    {
        "file": "index.html",
        "breadcrumb3": None,  # index.htmlはguideトップなのでposition3なし
        "faqs": [
            {
                "q": "日本のリキュールとは何ですか？",
                "a": "日本のリキュール（梅酒・ゆず酒・桃酒など）は、果実や植物素材をアルコールに漬け込んだり、混合して造る醸造酒です。代表的なものに梅酒・ゆず酒・桃酒・抹茶リキュール・桜リキュールがあります。Terroir HUB LIQUEURでは全国584社のメーカーを掲載しています。"
            },
            {
                "q": "梅酒と他のリキュールの違いは？",
                "a": "梅酒は青梅を焼酎・日本酒・ブランデーなどに砂糖と共に漬け込んで造ります。ゆず酒はゆずの果汁・果皮を使い、爽やかな柑橘風味が特徴。桃酒は桃の甘い香りが魅力です。各リキュールはベーススピリッツと素材の組み合わせで個性が決まります。"
            },
            {
                "q": "全国にリキュールメーカーはいくつありますか？",
                "a": "Terroir HUB LIQUEURでは全国47都道府県の584社のリキュールメーカーを掲載しています。梅酒メーカーが最も多く、次いでゆず酒・桃酒・みかん酒メーカーが各地に点在しています。"
            },
        ],
    },
    {
        "file": "types.html",
        "breadcrumb3": "リキュールの種類",
        "faqs": [
            {
                "q": "梅酒・ゆず酒・桃酒の違いは？",
                "a": "梅酒は青梅を砂糖と共にアルコールに漬け込んだ酸甘のバランスが特徴。ゆず酒はゆずの香りと柑橘の酸味が爽やか。桃酒は桃の甘くやわらかな風味が魅力。それぞれ原料の個性を活かした味わいが楽しめます。"
            },
            {
                "q": "抹茶リキュールはどんな味ですか？",
                "a": "抹茶リキュールは宇治・西尾など産地の抹茶の旨みと苦みをアルコールに溶け込ませたリキュールです。ミルクや牛乳で割ると抹茶ラテのような味わいになり、デザートとの相性も抜群です。"
            },
            {
                "q": "リキュールのアルコール度数はどれくらいですか？",
                "a": "日本のリキュールのアルコール度数は種類によって異なります。一般的な梅酒は8〜15度、ゆず酒は5〜12度程度です。低アルコールタイプ（3〜5度）から高アルコールタイプ（20度以上）まで多様なバリエーションがあります。"
            },
        ],
    },
    {
        "file": "production.html",
        "breadcrumb3": "製法",
        "faqs": [
            {
                "q": "梅酒の漬け込み製法とは？",
                "a": "漬け込み製法は、青梅・砂糖・ベーススピリッツ（焼酎・日本酒・ブランデーなど）を容器に入れ、数ヶ月〜数年かけて果実のエキスをアルコールに抽出する製法です。熟成期間が長いほどまろやかで複雑な味わいになります。"
            },
            {
                "q": "リキュールのベーススピリッツの種類は？",
                "a": "日本のリキュールで使われる主なベーススピリッツは、ホワイトリカー（甲類焼酎）・本格焼酎・日本酒・ブランデーです。ホワイトリカーは素材の風味を引き立て、ブランデーベースは深みとコクが増します。日本酒ベースは米の旨みが加わった複雑な味わいになります。"
            },
            {
                "q": "熟成期間はリキュールの味にどう影響しますか？",
                "a": "熟成期間が長いほど、アルコールと素材のエキスが馴染み、まろやかで複雑な味わいになります。チョーヤ梅酒の「3年熟成」のように、長期熟成品は深いコクと風味が生まれます。一般的に1〜6ヶ月の短期熟成品はフレッシュな風味、1〜3年熟成品は深みのある味わいになります。"
            },
        ],
    },
    {
        "file": "drinking.html",
        "breadcrumb3": "飲み方",
        "faqs": [
            {
                "q": "梅酒のおすすめの飲み方は？",
                "a": "梅酒の代表的な飲み方はロック（氷を入れてそのまま）・ソーダ割り（炭酸水で割る）・水割り・お湯割り・カクテルです。ロックは梅酒本来の濃厚な甘みと酸みが楽しめ、ソーダ割りはさっぱりとした夏向きの飲み方です。お湯割りは梅の香りが立ち、冬に人気です。"
            },
            {
                "q": "リキュールのカクテルレシピを教えてください",
                "a": "代表的なリキュールカクテルには、梅酒＋ジンジャーエール（梅酒ジンジャー）・ゆず酒＋トニックウォーター（ゆずトニック）・桃酒＋スパークリングワイン（ピーチベリーニ）などがあります。梅酒はウイスキーと合わせると深みのあるカクテルになります。"
            },
            {
                "q": "リキュールの適切な保存方法は？",
                "a": "リキュールは開封後は冷暗所（冷蔵庫推奨）で保存してください。特に梅酒は開封後もゆっくり熟成が進みます。直射日光を避け、10〜15℃程度の場所で保存するとフレッシュな風味が長持ちします。一般的に開封後1〜2年以内に飲むのがおすすめです。"
            },
        ],
    },
    {
        "file": "pairing.html",
        "breadcrumb3": "料理ペアリング",
        "faqs": [
            {
                "q": "梅酒に合う料理は？",
                "a": "梅酒は甘みと酸みのバランスが和食と相性抜群です。特に焼き鳥・唐揚げ・天ぷら・刺身・寿司などと合います。デザートとの相性も良く、チーズケーキ・羊羹・アイスクリームと組み合わせるとリッチな楽しみ方ができます。"
            },
            {
                "q": "ゆず酒・桃酒に合う料理は？",
                "a": "ゆず酒は柑橘の爽やかな酸みが魚介料理（刺身・寿司・海鮮サラダ）や鍋料理と抜群の相性です。桃酒はまろやかな甘みがフルーツデザート・クレームブリュレ・パンケーキなどと合います。抹茶リキュールはロールケーキやあんこ系和菓子と組み合わせると日本らしいペアリングになります。"
            },
            {
                "q": "食前・食後にリキュールを楽しむには？",
                "a": "食前酒としては、ゆず酒ソーダやスパークリングタイプのリキュールが食欲を刺激します。食後酒（ディジェスティフ）としては、梅酒のロックやブランデーベースの熟成梅酒がデザート代わりになります。少量をゆっくり味わうのがポイントです。"
            },
        ],
    },
    {
        "file": "history.html",
        "breadcrumb3": "歴史",
        "faqs": [
            {
                "q": "梅酒の歴史はどのくらい古いですか？",
                "a": "梅酒の起源は江戸時代（17世紀）以前にさかのぼります。梅は奈良時代に中国から薬用として伝わり、平安時代には薬酒として珍重されました。江戸時代に庶民にも広まり、1959年の酒税法改正で家庭での梅酒造りが合法化されたことで普及が進みました。チョーヤ梅酒が1914年に創業し、現代の梅酒産業の基礎を築きました。"
            },
            {
                "q": "日本のリキュールはいつから輸出されていますか？",
                "a": "チョーヤ梅酒が1975年頃から海外輸出を開始し、現在は世界40カ国以上に輸出されています。近年は「UMESHU」という呼び名で海外でも認知度が上がり、日本食レストランやバーを中心に世界中で楽しまれています。ゆず酒も欧米のバーシーンで高い人気を誇ります。"
            },
            {
                "q": "現代のクラフトリキュールはどんなものがありますか？",
                "a": "近年は小規模な「クラフトリキュール」メーカーが全国各地に登場しています。地元産のフルーツ（いちご・みかん・メロン）や素材（抹茶・桜・よもぎ）を使った個性的なリキュール、地元の日本酒や焼酎をベースにした地域色豊かなリキュールが生産されています。"
            },
        ],
    },
    {
        "file": "glossary.html",
        "breadcrumb3": "用語集",
        "faqs": [
            {
                "q": "梅酒とリキュールの違いは？",
                "a": "梅酒は酒税法上「リキュール類」に分類されます。リキュールは蒸留酒（スピリッツ）に果実・植物・砂糖などを混合した醸造酒の総称で、梅酒はその中の一種です。日本ではホワイトリカー（甲類焼酎）が最もよく使われるベーススピリッツです。"
            },
            {
                "q": "ホワイトリカーとはなんですか？",
                "a": "ホワイトリカーは甲類焼酎（連続式蒸留焼酎）の別名で、無色透明でクセがなくアルコール度数が35度程度の蒸留酒です。梅酒造りに最も広く使われ、素材（梅・果実）の風味を引き立てる特性があります。お酒の「土台」として機能します。"
            },
            {
                "q": "精製アルコールと本格焼酎の違いは？",
                "a": "ホワイトリカー（精製アルコール/甲類焼酎）はクセのない中性の味わいで素材を引き立てます。本格焼酎（乙類）は芋・麦・米などの原料由来の風味があり、リキュールに使うとよりコクのある複雑な味わいになります。どちらを使うかで完成品のキャラクターが変わります。"
            },
        ],
    },
    {
        "file": "umeshu.html",
        "breadcrumb3": "梅酒とは",
        "faqs": [
            {
                "q": "梅酒の有名なメーカーはどこですか？",
                "a": "日本を代表する梅酒メーカーには、チョーヤ梅酒（大阪府、The CHOYA）・中野BC（和歌山県、紀州）・梅乃宿酒造（奈良県、あらごし梅酒）・明利酒類（茨城県、百年梅酒）などがあります。各メーカーが南高梅をはじめとする高品質な梅を使ったこだわりの梅酒を生産しています。"
            },
            {
                "q": "南高梅とはどんな梅ですか？",
                "a": "南高梅は和歌山県みなべ町が発祥の高級梅品種で、梅酒・梅干し用として最も評価が高い梅です。大粒で果肉が厚く、上品な甘みと豊かな香りが特徴。全国の梅酒メーカーが南高梅産地（和歌山・群馬・長野など）と契約栽培することが多く、高品質梅酒の代名詞的原料です。"
            },
            {
                "q": "梅酒の選び方を教えてください",
                "a": "梅酒を選ぶポイントは①ベーススピリッツ（ホワイトリカー・日本酒・ブランデー）②梅の品種（南高梅・古城梅等）③甘さと酸のバランス（甘口・中口・辛口）④熟成期間（フレッシュ/長期熟成）⑤アルコール度数（8〜17度）です。初めての方はチョーヤの「さらりとした梅酒」（10度）や梅乃宿の「あらごし梅酒」が飲みやすくおすすめです。"
            },
        ],
    },
]


def build_json_ld(page_cfg: dict) -> str:
    """ページ設定からJSON-LDブロックを生成する。"""
    breadcrumb_items = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Terroir HUB LIQUEUR",
            "item": "https://liqueur.terroirhub.com/",
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "リキュールガイド",
            "item": "https://liqueur.terroirhub.com/liqueur/guide/",
        },
    ]
    if page_cfg["breadcrumb3"]:
        breadcrumb_items.append(
            {
                "@type": "ListItem",
                "position": 3,
                "name": page_cfg["breadcrumb3"],
            }
        )

    faq_entities = []
    for faq in page_cfg["faqs"]:
        faq_entities.append(
            {
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["a"],
                },
            }
        )

    graph = [
        {
            "@type": "BreadcrumbList",
            "itemListElement": breadcrumb_items,
        },
        {
            "@type": "FAQPage",
            "mainEntity": faq_entities,
        },
    ]

    ld = {"@context": "https://schema.org", "@graph": graph}
    json_str = json.dumps(ld, ensure_ascii=False, indent=2)
    return f'<script type="application/ld+json">\n{json_str}\n</script>'


def process_file(page_cfg: dict) -> str:
    """1ファイルを処理してJSON-LDを挿入する。戻り値はステータスメッセージ。"""
    filepath = os.path.join(GUIDE_DIR, page_cfg["file"])

    if not os.path.exists(filepath):
        return f"  SKIP (not found): {page_cfg['file']}"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 既にFAQPageが存在する場合はスキップ
    if "FAQPage" in content:
        return f"  SKIP (already has FAQPage): {page_cfg['file']}"

    json_ld_block = build_json_ld(page_cfg)

    # </head> の直前に挿入
    if "</head>" not in content:
        return f"  ERROR (no </head> found): {page_cfg['file']}"

    new_content = content.replace("</head>", f"{json_ld_block}\n</head>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    faq_count = len(page_cfg["faqs"])
    return f"  OK ({faq_count} FAQs inserted): {page_cfg['file']}"


def verify_file(page_cfg: dict) -> str:
    """挿入後の確認。FAQPageの件数を返す。"""
    filepath = os.path.join(GUIDE_DIR, page_cfg["file"])
    if not os.path.exists(filepath):
        return f"  MISSING: {page_cfg['file']}"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    faq_count = content.count('"@type": "Question"')
    has_breadcrumb = "BreadcrumbList" in content
    has_faq = "FAQPage" in content
    return (
        f"  {page_cfg['file']}: FAQPage={has_faq}, BreadcrumbList={has_breadcrumb}, "
        f"Question count={faq_count}"
    )


def main():
    print(f"=== add_faq_to_guide.py ===")
    print(f"Guide dir: {GUIDE_DIR}\n")

    print("[1] Inserting JSON-LD into guide HTML files...")
    for page_cfg in PAGES:
        result = process_file(page_cfg)
        print(result)

    print("\n[2] Verification...")
    for page_cfg in PAGES:
        result = verify_file(page_cfg)
        print(result)

    print("\nDone.")


if __name__ == "__main__":
    main()
