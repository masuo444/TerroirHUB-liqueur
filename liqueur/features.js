// Terroir HUB LIQUEUR — ログイン後の機能（お気に入り・サクラ制限）

(function(){
  'use strict';

  function escHtml(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}

  const FAV_KEY = 'thub_favorites';

  function getFavs(){ return JSON.parse(localStorage.getItem(FAV_KEY) || '[]'); }
  function saveFavs(favs){ localStorage.setItem(FAV_KEY, JSON.stringify(favs)); }

  window.thubToggleFav = async function(breweryId, breweryName){
    if(!window.thubAuth || !window.thubAuth.isLoggedIn){
      if(typeof showAuth === 'function') showAuth('login');
      return;
    }
    const favs = getFavs();
    const idx = favs.findIndex(f => f.brewery_id === breweryId);
    if(idx >= 0){
      favs.splice(idx, 1);
      saveFavs(favs);
      showFavToast('お気に入りから削除しました');
      if(window.thubAuth.supabase){
        window.thubAuth.supabase.from('favorites').delete().eq('user_id', window.thubAuth.user.id).eq('brewery_id', breweryId);
      }
    } else {
      favs.push({ brewery_id: breweryId, brewery_name: breweryName, timestamp: new Date().toISOString() });
      saveFavs(favs);
      showFavToast('お気に入りに追加しました');
      if(window.thubAuth.supabase){
        window.thubAuth.supabase.from('favorites').insert({ user_id: window.thubAuth.user.id, brewery_id: breweryId, brewery_name: breweryName });
      }
      if(window.thub) window.thub.favorite(breweryId, breweryName);
    }
  };

  window.thubIsFav = function(breweryId){
    return getFavs().some(f => f.brewery_id === breweryId);
  };

  window.thubShowFavs = function(){
    const favs = getFavs();
    let content = '';
    if(favs.length === 0){
      content = '<div style="text-align:center;padding:32px;color:#aaa;font-size:13px;">まだお気に入りがありません</div>';
    } else {
      content = favs.map(f => '<div style="display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid #f0f0f0;"><div style="flex:1;font-size:13px;font-weight:500;color:#333;">' + escHtml(f.brewery_name) + '</div></div>').join('');
    }
    const modal = document.createElement('div');
    modal.id = 'fav-modal';
    modal.style.cssText = 'position:fixed;inset:0;z-index:700;background:rgba(0,0,0,0.4);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;';
    modal.onclick = function(e){ if(e.target === modal) modal.remove(); };
    modal.innerHTML = '<div style="background:#fff;border-radius:14px;max-width:440px;width:calc(100% - 32px);padding:28px;box-shadow:0 16px 48px rgba(0,0,0,0.12);max-height:85vh;overflow-y:auto;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;"><div style="font-family:Shippori Mincho,serif;font-size:18px;font-weight:600;">お気に入り</div><button onclick="this.closest(\'#fav-modal\').remove()" style="background:#fafaf8;border:none;width:26px;height:26px;border-radius:6px;cursor:pointer;color:#999;font-size:13px;">✕</button></div><div>' + content + '</div></div>';
    document.body.appendChild(modal);
  };

  function showFavToast(msg){
    const toast = document.createElement('div');
    toast.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:#333;color:#fff;padding:10px 20px;border-radius:8px;font-size:13px;z-index:800;';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = 'opacity 0.3s'; setTimeout(() => toast.remove(), 300); }, 2000);
  }

  // サクラ利用回数制限
  const ANON_CREDIT_KEY = 'thub_anon_credits';

  function getAnonCredits(){
    const data = JSON.parse(localStorage.getItem(ANON_CREDIT_KEY) || '{}');
    const month = new Date().toISOString().slice(0,7);
    if(data.month !== month){
      var limit = window.innerWidth > 700 ? 8 : 3;
      return { month: month, remaining: limit, used: 0 };
    }
    return data;
  }
  function saveAnonCredits(c){ localStorage.setItem(ANON_CREDIT_KEY, JSON.stringify(c)); }

  window.thubCheckSakuraLimit = function(){
    if(!window.thubAuth || !window.thubAuth.isLoggedIn){
      var credits = getAnonCredits();
      if(credits.remaining <= 0){
        if(typeof addM === 'function') addM('bot', 'お試し回数を使い切りました。\n\n無料会員登録すると月10回まで使えます。');
        else if(typeof addMsg === 'function') addMsg('butler', 'お試し回数を使い切りました。\n\n無料会員登録すると月10回まで使えます。');
        return false;
      }
      credits.remaining--;
      credits.used++;
      saveAnonCredits(credits);
      return true;
    }
    return true;
  };
})();
