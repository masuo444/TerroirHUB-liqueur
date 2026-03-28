// Terroir HUB LIQUEUR — Supabase Auth Integration

(function(){
  'use strict';

  function escHtml(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}

  const SUPABASE_URL = 'https://hhwavxavuqqfiehrogwv.supabase.co';
  const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhod2F2eGF2dXFxZmllaHJvZ3d2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM5Njk3MzAsImV4cCI6MjA4OTU0NTczMH0.tHMQ_u51jp69AMUKKtTvxL09Sr11JFPKGRhKMmUzEjg';

  window.thubAuthSubmit = function(){
    alert('認証システムを読み込み中です。数秒お待ちください。');
  };

  if(SUPABASE_URL === 'YOUR_SUPABASE_URL') {
    console.log('[AUTH] Supabase not configured. Using demo mode.');
    window.thubAuth = { user: null, demo: true };
    return;
  }

  const script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js';
  script.onload = initAuth;
  document.head.appendChild(script);

  function initAuth() {
    const { createClient } = supabase;
    const sb = createClient(SUPABASE_URL, SUPABASE_KEY);
    let currentUser = null;
    let currentPlan = 'free';

    sb.auth.onAuthStateChange(async (event, session) => {
      if (event === 'SIGNED_IN' && session) {
        currentUser = session.user;
        await sb.from('profiles').upsert({ id: currentUser.id, plan: 'free' }, { onConflict: 'id', ignoreDuplicates: true });
        onLogin(currentUser);
      } else if (event === 'SIGNED_OUT') {
        currentUser = null;
        onLogout();
      }
    });

    sb.auth.getSession().then(function(res){
      if(res.data && res.data.session){
        currentUser = res.data.session.user;
        onLogin(currentUser);
      }
    });

    window.thubSignUp = async function(email, password) {
      const { data, error } = await sb.auth.signUp({ email, password });
      if (error) { alert(error.message); return false; }
      alert('確認メールを送信しました。メールのリンクをクリックしてください。');
      if (window.thub) window.thub.signup('email');
      return true;
    };

    window.thubSignIn = async function(email, password) {
      const { data, error } = await sb.auth.signInWithPassword({ email, password });
      if (error) { alert(error.message); return false; }
      if (window.thub) window.thub.login('email');
      return true;
    };

    window.thubSignInWithGoogle = async function() {
      await sb.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: window.location.origin } });
    };

    window.thubSignOut = async function() {
      await sb.auth.signOut();
    };

    window.thubSubscribe = function(plan) {
      window.location.href = 'https://sake.terroirhub.com/api/create-checkout?plan=' + plan;
    };

    function onLogin(user) {
      currentUser = user;
      window.thubAuth = { user: user, supabase: sb, isLoggedIn: true, plan: currentPlan, userId: user.id };
      if (window.thub) window.thub.setUser(user.id);
      document.querySelectorAll('.nav-login-btn,.nav-signup-btn,.mm-cta,.mm-login-btn').forEach(function(el){ el.style.display = 'none'; });
    }

    function onLogout() {
      window.thubAuth = { user: null, supabase: sb, isLoggedIn: false, plan: 'free' };
      document.querySelectorAll('.nav-login-btn,.nav-signup-btn,.mm-cta,.mm-login-btn').forEach(function(el){ el.style.display = ''; });
    }

    window.thubAuthSubmit = function() {
      var email = document.getElementById('auth-email').value;
      var pass = document.getElementById('auth-pass').value;
      if (!email || !pass) { alert('メールアドレスとパスワードを入力してください'); return; }
      var btn = document.getElementById('auth-btn');
      if (btn.textContent.includes('登録')) { window.thubSignUp(email, pass); }
      else { window.thubSignIn(email, pass); }
    };

    window.thubAuth = { user: null, supabase: sb, isLoggedIn: false, plan: 'free' };
  }
})();
