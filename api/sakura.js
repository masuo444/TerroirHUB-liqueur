// サクラ Claude API プロキシ（リキュール版）

const fs = require('fs');
const path = require('path');

let searchIndex = null;
function getSearchIndex() {
  if (searchIndex) return searchIndex;
  searchIndex = [];
  try {
    const liqueurPath = path.join(__dirname, '..', 'liqueur', 'search_index.json');
    const liqueurData = JSON.parse(fs.readFileSync(liqueurPath, 'utf-8'));
    liqueurData.forEach(e => { e._site = 'liqueur'; });
    searchIndex = searchIndex.concat(liqueurData);
  } catch (e) {}
  try {
    const sakePath = path.join(__dirname, '..', 'liqueur', 'search_index_sake.json');
    const sakeData = JSON.parse(fs.readFileSync(sakePath, 'utf-8'));
    sakeData.forEach(e => { e._site = 'sake'; });
    searchIndex = searchIndex.concat(sakeData);
  } catch (e) {}
  return searchIndex;
}

function searchProducers(query) {
  const idx = getSearchIndex();
  const ql = query.toLowerCase();
  const keywords = ql.split(/\s+/).filter(k => k.length > 0);

  const scored = idx.map(entry => {
    const name = (entry.n || '').toLowerCase();
    const brand = (entry.b || '').toLowerCase();
    const brands = (entry.br || '').toLowerCase();
    const area = (entry.a || '').toLowerCase();
    const nameEn = (entry.ne || '').toLowerCase();
    const pref = (entry.pn || '').toLowerCase();
    const full = [name, brand, brands, area, nameEn, pref].join(' ');

    let s = 0;
    if (brand === ql) s += 200;
    if (brand.includes(ql)) s += 100;
    if (brands.includes(ql)) s += 90;
    if (name === ql) s += 80;
    if (name.includes(ql)) s += 60;
    if (nameEn.includes(ql)) s += 50;
    if (pref.includes(ql)) s += 40;
    if (area.includes(ql)) s += 35;
    if (full.includes(ql)) s += 10;
    if (keywords.length > 1 && keywords.every(k => full.includes(k))) s += 80;
    return { entry, s };
  }).filter(x => x.s > 0).sort((a, b) => b.s - a.s);

  return scored.slice(0, 5).map(x => {
    const e = x.entry;
    const site = e._site || 'liqueur';
    const basePath = site === 'sake' ? 'https://sake.terroirhub.com/sake' : '/liqueur';
    return {
      name: e.n || '', brand: e.b || '', brands: e.br || '',
      prefecture: e.pn || '', area: e.a || '',
      type: site === 'sake' ? '日本酒' : 'リキュール',
      page: `${basePath}/${e.p}/${e.id}.html`,
    };
  });
}

const TOOLS = [
  {
    name: 'search_producers',
    description: 'リキュールメーカー・銘柄をTerroir HUBデータベースから検索する。メーカー名、銘柄名、地域名で検索可能。',
    input_schema: {
      type: 'object',
      properties: { query: { type: 'string', description: '検索キーワード' } },
      required: ['query']
    }
  },
  { type: 'web_search_20250305', name: 'web_search', max_uses: 3 }
];

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'API not configured' });

  const { question, context, history, userId } = req.body || {};
  if (!question) return res.status(400).json({ error: 'No question' });

  const supabaseUrl = process.env.SUPABASE_URL || 'https://hhwavxavuqqfiehrogwv.supabase.co';
  const supabaseKey = process.env.SUPABASE_SERVICE_KEY;

  const systemPrompt = `あなたは「サクラ」、Terroir HUB LIQUEURのAIコンシェルジュです。
日本のリキュール（梅酒・ゆず酒・桃酒・抹茶リキュール・桜リキュール等）のデータベースを熟知しています。

キャラクター：
- 名前は「サクラ」。リキュールが大好きな、明るく親しみやすいコンシェルジュ
- 一人称は「サクラ」。敬語だが堅すぎない、友達に話すような温かさ
- 絵文字は控えめに（🌸🍑🫐程度）

会話のルール（最重要）：
- 回答は正確に、公式情報に基づいて行う
- 知らないことは「公式サイトをご確認ください」と案内する
- 情報を捏造しない。推測で埋めない
- 日本語、英語、フランス語に対応（相手の言語に合わせる）
- 回答は200〜300文字を目安に

★ ツール活用の絶対ルール：
- ユーザーが特定の銘柄名やメーカー名を挙げた場合、まず search_producers ツールでDB検索する
- 検索結果があれば、メーカーページへのリンク（page フィールド）を含めて回答する
- DB検索で見つからない場合は、web_search ツールでWeb検索する

★ 会話を続けるための絶対ルール：
- 回答の最後に必ず「関連する次の質問」を1つ投げかける
- 一方的な情報提供で終わらない。必ず対話を促す

リキュールの基礎知識：
【種類】梅酒（最も人気）、ゆず酒、桃酒、みかん酒、いちご酒、抹茶リキュール、桜リキュール、メロンリキュール、ヨーグルト酒
【ベーススピリッツ】ホワイトリカー（最も一般的）、日本酒ベース（まろやか）、焼酎ベース（コクがある）、ブランデーベース（深みのある味わい）
【飲み方】ロック、ソーダ割り、水割り、お湯割り、カクテルベース、ストレート
【ペアリング】梅酒→和食全般・チーズ、ゆず酒→刺身・寿司、桃酒→デザート・フルーツ
【有名メーカー】チョーヤ梅酒（大阪）、中野BC（和歌山）、梅乃宿酒造（奈良）、明利酒類（茨城）

姉妹サイト案内：
- 日本酒 → sake.terroirhub.com
- 焼酎 → shochu.terroirhub.com
- ウイスキー → whisky.terroirhub.com

${context ? '現在のページの情報：\n' + context : ''}`;

  const messages = [];
  if (history && Array.isArray(history)) {
    history.slice(-20).forEach(h => { messages.push({ role: h.role, content: h.content }); });
  }
  messages.push({ role: 'user', content: question });

  try {
    let response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-api-key': apiKey, 'anthropic-version': '2023-06-01' },
      body: JSON.stringify({ model: 'claude-haiku-4-5-20251001', max_tokens: 1024, system: systemPrompt, messages: messages, tools: TOOLS }),
    });

    let data = await response.json();
    if (data.error) return res.status(500).json({ error: 'AI response failed' });

    let currentMessages = [...messages];
    let maxLoops = 4;

    while (data.stop_reason === 'tool_use' && maxLoops-- > 0) {
      currentMessages.push({ role: 'assistant', content: data.content });
      const toolResults = [];
      for (const block of data.content) {
        if (block.type !== 'tool_use') continue;
        if (block.name === 'search_producers') {
          const results = searchProducers(block.input.query);
          toolResults.push({
            type: 'tool_result', tool_use_id: block.id,
            content: JSON.stringify(results.length > 0 ? { found: true, count: results.length, results } : { found: false, message: 'データベースに該当なし。' })
          });
        }
      }
      if (toolResults.length > 0) currentMessages.push({ role: 'user', content: toolResults });

      const nextResponse = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-api-key': apiKey, 'anthropic-version': '2023-06-01' },
        body: JSON.stringify({ model: 'claude-haiku-4-5-20251001', max_tokens: 800, system: systemPrompt, messages: currentMessages, tools: TOOLS }),
      });
      data = await nextResponse.json();
      if (data.error) break;
    }

    let answer = '';
    if (data.content) {
      const textBlock = data.content.find(b => b.type === 'text');
      answer = textBlock ? textBlock.text : '';
    }

    // Log
    try {
      const logKey = supabaseKey || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhod2F2eGF2dXFxZmllaHJvZ3d2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM5Njk3MzAsImV4cCI6MjA4OTU0NTczMH0.tHMQ_u51jp69AMUKKtTvxL09Sr11JFPKGRhKMmUzEjg';
      await fetch(supabaseUrl + '/rest/v1/ai_logs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'apikey': logKey, 'Authorization': 'Bearer ' + logKey, 'Prefer': 'return=minimal' },
        body: JSON.stringify({ user_id: userId || null, question: question, answer: answer.substring(0, 2000), model: 'haiku-4.5', source: 'liqueur' }),
      });
    } catch (logErr) {}

    return res.status(200).json({ answer: answer });
  } catch (err) {
    console.error('Sakura API error:', err.message);
    return res.status(500).json({ error: 'AI service unavailable' });
  }
};
