#!/usr/bin/env python3
"""
楽天商品が「リキュール・梅酒・果実酒」かどうかを判定する共通フィルタ。
whisky_filter / shochu_filter と同設計で語彙だけ差し替えたもの。
方針: 精度優先（リキュール類以外を出さない）。
"""
import re

_EXCLUDE_HARD = re.compile(
    r'カーディガン|スカート|ニット|セーター|シャツ|Tシャツ|ブラウス|ワンピース|パンツ|デニム|ジーンズ'
    r'|コート|ジャケット|アウター|パーカー|スウェット|スカジャン|半纏|法被|前掛け|エプロン|木綿|手ぬぐい'
    r'|ランジェリー|インナー|下着|靴下|帽子|マフラー|手袋|スニーカー|シューズ'
    r'|バッグ|\bbag\b|カバン|鞄|財布|ポーチ|リュック|ピアス|ネックレス|ブレスレット|指輪|アクセサリ'
    r'|腕時計|掛け時計|サングラス|眼鏡|スマホケース|手芸|フィギュア|ぬいぐるみ|ボールペン|タオル|マット|クッション'
    r'|ワイングラス|ロックグラス|グラスセット|タンブラー|食器|お皿|プレート|ボウル|カトラリー|急須|湯呑|栓抜き'
    r'|電子書籍|\bebook\b|kindle|楽天kobo|文庫|新書|コミック|単行本|写真集|カレンダー'
    r'|石鹸|化粧水|コスメ|入浴剤'
    # 酒ではない梅・果実の加工品（梅干し・ジュース・ジャム等）
    r'|梅干|梅干し|練り梅|梅ジャム|ジャム|ドレッシング|レトルト|ソーセージ|燻製'
    r'|ジュース|果汁100|シロップ|ゼリー|アイス|ヨーグルト\s*\d+個|ケーキ|クッキー|焼き菓子|チョコレート'
    r'|青梅\s*\d+kg|生梅|梅酒用|梅酒作り|果実酒用|漬け込み用|ホワイトリカー',
    re.IGNORECASE,
)

# リキュール類であるシグナル
_LIQUEUR = re.compile(
    r'リキュール|liqueur|梅酒|うめ酒|果実酒|ゆず酒|柚子酒|すだち酒|かぼす酒|みかん酒|いちご酒|苺酒'
    r'|りんご酒|ぶどう酒|もも酒|桃酒|ブルーベリー酒|レモン酒|シークヮーサー|ヨーグルト酒|ヨーグルトリキュール'
    r'|抹茶リキュール|桜リキュール|クリームリキュール|和リキュール|フルーツリキュール'
    r'|にごり梅|完熟梅|南高梅.*酒|紀州.*梅酒|黒糖梅酒|日本酒仕込|ブランデー仕込',
    re.IGNORECASE,
)

_ABV = re.compile(r'(7|8|9|10|11|12|13|14|15|16|17|18|19|20|25)\s*(度|%|％)')
_VOL = re.compile(r'(1800|1\.8|900|720|750|500|360|300|200|180)\s?(ml|mL|ML|L|リットル)|一升|四合', re.IGNORECASE)

_EXCLUDE_BOOZE = re.compile(
    r'日本酒|清酒|純米|吟醸|本醸造|大吟醸|どぶろく'
    r'|ワイン|\bwine\b|ヴァン|スパークリング|シャンパン'
    r'|ウイスキー|ウィスキー|whisky|whiskey|シングルモルト|バーボン|スコッチ'
    r'|ビール|発泡酒|\bbeer\b|クラフトビール|エール|ラガー'
    r'|焼酎|泡盛|芋焼酎|麦焼酎|米焼酎|黒糖焼酎',
    re.IGNORECASE,
)


def is_liqueur_item(name: str) -> bool:
    """商品名がリキュール・梅酒・果実酒として妥当ならTrue。"""
    if not name:
        return False
    if _EXCLUDE_HARD.search(name):
        return False
    if _LIQUEUR.search(name):
        return True
    if _EXCLUDE_BOOZE.search(name):
        return False
    if _ABV.search(name) or _VOL.search(name):  # 度数/定番容量があり除外語も無い → 蔵のリキュール類とみなす
        return True
    return False


if __name__ == '__main__':
    tests = [
        ('チョーヤ The CHOYA AGED 3 YEARS 720ml', True),
        ('【ふるさと納税】紀州南高梅 完熟梅酒 720ml', True),
        ('中野BC 紀州 blossom ゆず酒 720ml', True),
        ('八鹿 coconoe ヨーグルトリキュール 500ml', True),
        ('南高梅 青梅 5kg 梅酒用', False),
        ('八海山 純米大吟醸 1800ml', False),
        ('黒霧島 25度 1800ml 芋焼酎', False),
        ('梅干し 塩分5% 1kg 紀州南高梅', False),
        ('奏 Kanade 抹茶リキュール 500ml', True),
        ('サントリー 知多 700ml ウイスキー', False),
        ('梅ジュース 果汁100% 1000ml', False),
    ]
    ok = 0
    for nm, exp in tests:
        got = is_liqueur_item(nm)
        m = 'OK' if got == exp else 'NG'
        if got == exp:
            ok += 1
        print(f'  [{m}] {got!s:5} (期待{exp!s:5}) {nm}')
    print(f'\n{ok}/{len(tests)} passed')
