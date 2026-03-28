# Terroir HUB LIQUEUR — エージェント作業マニュアル

## プロジェクト概要
全国のリキュール（梅酒・ゆず酒・桃酒・抹茶リキュール等）メーカーデータベース。
日本独自のフルーツリキュール・和素材リキュールを網羅。
デプロイ先: （未設定）
GitHub: （未設定）
姉妹サイト: https://sake.terroirhub.com/（日本酒版）、https://shochu.terroirhub.com/（焼酎版）、https://whisky.terroirhub.com/（ウイスキー版）
ドメイン: liqueur.terroirhub.com

## ファイル構成

```
/Users/masuo/Desktop/terroirHUB liqueur/
├── index.html                          # トップページ
├── RULES.md                            # 情報正確性ルール（必読）
├── CLAUDE.md                           # このファイル
├── template_liqueur.html               # CSSテンプレート（メーカーページ用）
├── data/
│   └── data_{県slug}_liqueurs.json     # 各県のリキュールメーカーデータ
├── liqueur/
│   ├── sakura_kb.json                  # AIサクラ ナレッジベース
│   ├── track.js                        # 行動データ取得スクリプト
│   ├── auth.js                         # Supabase認証
│   ├── features.js                     # ログイン後機能
│   ├── region/                         # 8地域ページ
│   │   ├── hokkaido.html
│   │   ├── tohoku.html
│   │   ├── kanto.html
│   │   ├── chubu.html
│   │   ├── kinki.html
│   │   ├── chugoku.html
│   │   ├── shikoku.html
│   │   └── kyushu.html
│   ├── guide/                          # 教科書ページ
│   │   ├── index.html                  # リキュールガイド
│   │   ├── types.html                  # 種類（梅酒・ゆず酒・桃酒等）
│   │   ├── production.html             # 製法（漬け込み・ブレンド）
│   │   ├── drinking.html               # 飲み方（ロック・ソーダ割り・カクテル）
│   │   ├── pairing.html                # 料理ペアリング
│   │   ├── history.html                # 歴史（梅酒の起源〜現代）
│   │   ├── umeshu.html                 # 梅酒とは（専門ページ）
│   │   └── glossary.html               # 用語集
│   ├── en/                             # 英語版
│   ├── fr/                             # フランス語版
│   └── {県slug}/                       # 各県ディレクトリ
│       ├── index.html                  # 県一覧ページ
│       └── {producer_id}.html          # 個別メーカーページ
├── admin/
│   └── index.html                      # 管理ダッシュボード
├── api/
│   ├── sakura.js                       # Claude AI プロキシ（AIサクラ）
│   ├── create-checkout.js              # Stripe決済
│   └── webhook.js                      # Stripeウェブフック
├── scripts/
│   ├── regenerate_all_pages.py         # 全メーカーページ一括生成
│   ├── generate_pref_index.py          # 県一覧ページ生成
│   ├── generate_sitemap.py             # サイトマップ生成
│   ├── build_search_index.py           # 検索インデックス構築
│   ├── build_sakura_kb.py              # AIナレッジベース構築
│   └── generate_multilang_pages.py     # 多言語版生成
├── vercel.json
├── robots.txt
├── sitemap.xml
└── package.json
```

## データ形式（JSON）

各`data/{県slug}_liqueurs.json`は配列。1メーカーあたり:

```json
{
  "id": "choya",
  "name": "チョーヤ梅酒",
  "company": "チョーヤ梅酒株式会社",
  "brand": "CHOYA",
  "type": "梅酒",
  "liqueur_type": "umeshu",
  "base_spirit": "ホワイトリカー",
  "fruit_ingredient": "南高梅",
  "abv": "15",
  "founded": "1914",
  "founded_era": "大正3年",
  "address": "大阪府羽曳野市駒ヶ谷160番地の1",
  "tel": "072-956-0511",
  "url": "https://www.choya.co.jp/",
  "area": "羽曳野市",
  "desc": "大正3年（1914年）創業。南高梅と国産ブランデーを使用した本格梅酒の代名詞。",
  "visit": "",
  "brands": [
    {
      "name": "The CHOYA AGED 3 YEARS",
      "type": "梅酒",
      "specs": "3年熟成、アルコール17度"
    },
    {
      "name": "さらりとした梅酒",
      "type": "梅酒",
      "specs": "アルコール10度、すっきりタイプ"
    }
  ],
  "features": [
    "1914年創業、日本を代表する梅酒メーカー",
    "南高梅を丸ごと漬け込む本格製法",
    "世界40カ国以上に輸出"
  ],
  "nearest_station": "",
  "source": "https://www.choya.co.jp/",
  "lat": 34.5484,
  "lng": 135.6122,
  "name_en": "Choya Umeshu"
}
```

### リキュール固有フィールド
| フィールド | 説明 | 例 |
|-----------|------|-----|
| `liqueur_type` | リキュールの種類 | "umeshu" / "yuzu" / "peach" / "mikan" / "strawberry" / "matcha" / "sakura" / "melon" / "yogurt" / "other" |
| `base_spirit` | ベーススピリッツ | "ホワイトリカー" / "日本酒" / "焼酎" / "ブランデー" |
| `fruit_ingredient` | 主要果実・素材 | "南高梅" / "ゆず" / "白桃" / "いちご" |
| `abv` | アルコール度数 | "8" / "10" / "14" / "17" |

### リキュールタイプ分類
| コード | 日本語 | 英語 |
|--------|--------|------|
| umeshu | 梅酒 | Umeshu (Plum Wine) |
| yuzu | ゆず酒 | Yuzushu |
| peach | 桃酒 | Momoshu |
| mikan | みかん酒 | Mikanshu |
| strawberry | いちご酒 | Ichigoshu |
| matcha | 抹茶リキュール | Matcha Liqueur |
| sakura | 桜リキュール | Sakura Liqueur |
| melon | メロンリキュール | Melon Liqueur |
| yogurt | ヨーグルト酒 | Yogurt Liqueur |
| other | その他 | Other |

## 品質ランク定義

| ランク | 条件 | 状態 |
|--------|------|------|
| A | founded + brands(1〜3銘柄) + features(2+) + url + liqueur_type | 完全版 |
| B | founded + brands or features あるがURL無し or liqueur_type未設定 | 要改善 |
| C | foundedのみ | 最低限 |
| D | 何もなし | 対象外 |

**目標: 主要メーカー（チョーヤ・サントリー・梅乃宿・中野BC等）は全てAランク**

## AIコンシェルジュ「サクラ」（全サイト共通）

全Terroir HUBサイト共通のAIコンシェルジュ「サクラ」。
- 知識ベース: `liqueur/sakura_kb.json`
- API: `/api/sakura.js`
- キャラクター: リキュールの華やかな世界を案内する、明るく親しみやすいコンシェルジュ

## データソース（メーカーリスト取得元）

### 業界団体
| ソース | URL | 備考 |
|---|---|---|
| 日本洋酒酒造組合 | https://yoshu.or.jp/ | リキュール製造者の業界団体 |
| 全国梅酒品評会 | https://umeshu-hyougi.jp/ | 梅酒専門品評会 |

### 全国データソース
| ソース | URL | 備考 |
|---|---|---|
| 国税庁 酒蔵マップ | https://www.nta.go.jp/taxes/sake/sakagura/index.htm | 公式データ |

### 主要メーカー
| メーカー名 | 所在地 | 代表銘柄 |
|---|---|---|
| チョーヤ梅酒 | 大阪府羽曳野市 | The CHOYA / さらりとした梅酒 |
| 中野BC | 和歌山県海南市 | 紀州 / 緑茶梅酒 |
| 梅乃宿酒造 | 奈良県葛城市 | あらごしシリーズ |
| 明利酒類 | 茨城県水戸市 | 梅香 百年梅酒 |
| サントリー | 大阪府大阪市 | Kanadeシリーズ |
| 白鶴酒造 | 兵庫県神戸市 | まるごと搾りシリーズ |
| 月桂冠 | 京都府京都市 | フルーツリキュールライン |
| 八海醸造 | 新潟県南魚沼市 | 八海山の梅酒 |
| 北島酒造 | 滋賀県湖南市 | 御代栄 |
| 請福酒造 | 沖縄県石垣市 | 泡盛梅酒 |

## 絶対にやってはいけないこと

1. **情報を捏造しない** — 公式サイトにない情報は入れない
2. **推測で埋めない** — 分からない項目は空欄のまま
3. **AIが文章を生成しない** — 説明文は公式サイトの文言を使う
4. **他のメーカーのデータを混同しない** — IDとメーカー名を必ず照合
5. **度数を推測で書かない** — 公式ラベル・サイトの表記通りに記載
6. **ベーススピリッツを推測で書かない** — 公式に記載がある情報のみ
7. **brandsにspecs=""で入れて「完了」と言わない** — 実データがないならBランクと正直に報告

## 県slugマッピング

```
hokkaido aomori iwate miyagi akita yamagata fukushima
ibaraki tochigi gunma saitama chiba tokyo kanagawa
niigata toyama ishikawa fukui yamanashi nagano gifu shizuoka aichi
mie shiga kyoto osaka hyogo nara wakayama
tottori shimane okayama hiroshima yamaguchi
tokushima kagawa ehime kochi
fukuoka saga nagasaki kumamoto oita miyazaki kagoshima okinawa
```
