// SurvivalAI — Chat Application
// Vanilla JS, no frameworks, no build tools

(function() {
  'use strict';

  var API_URL = '/v1/chat/completions';
  var DB_PATH = 'knowledge.db';
  var PROMPTS_PATH = '../config/quick-prompts.json';
  var SYSTEM_PROMPT_PATH = '../config/system-prompt.txt';
  var MAX_CONTEXT_SECTIONS = 5;
  var MAX_CONTEXT_CHARS = 3000;
  var MAX_HISTORY = 10;

  var db = null;
  var sqlReady = false;
  var systemPrompt = 'You are SurvivalAI, an offline survival assistant. Answer questions using the provided knowledge base context when available.';
  var conversationHistory = [];
  var isGenerating = false;

  // ==================== INIT ====================
  async function init() {
    setupUI();
    await loadSystemPrompt();
    await loadQuickPrompts();
    await initDatabase();
    checkServer();
  }

  function setupUI() {
    var input = document.getElementById('user-input');

    input.addEventListener('input', function() {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });

    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
  }

  // ==================== SIDEBAR (mobile) ====================
  window.toggleSidebar = function() {
    document.getElementById('sidebar').classList.toggle('open');
  };

  window.showView = function(view) {
    document.getElementById('sidebar').classList.remove('open');
  };

  // ==================== SYSTEM PROMPT ====================
  async function loadSystemPrompt() {
    try {
      var res = await fetch(SYSTEM_PROMPT_PATH);
      if (res.ok) systemPrompt = await res.text();
    } catch (e) {}
  }

  // ==================== QUICK PROMPTS ====================
  var QUICK_ICONS = ['🩸','💧','🔥','🏕️','💨','🌿','🦴','🧭'];

  async function loadQuickPrompts() {
    try {
      var res = await fetch(PROMPTS_PATH);
      var prompts = await res.json();
      var container = document.getElementById('quick-prompts');
      prompts.forEach(function(p, i) {
        var div = document.createElement('div');
        div.className = 'quick-prompt';
        div.innerHTML =
          '<span class="qp-icon">' + (QUICK_ICONS[i] || '❓') + '</span>' +
          '<span class="qp-label">' + escapeHtml(p.label) + '</span>' +
          '<span class="qp-hint">' + escapeHtml(p.prompt.substring(0, 60)) + '...</span>';
        div.addEventListener('click', function() {
          document.getElementById('user-input').value = p.prompt;
          sendMessage();
        });
        container.appendChild(div);
      });
    } catch (e) {}
  }

  // ==================== DATABASE ====================
  async function initDatabase() {
    try {
      if (typeof initSqlJs === 'undefined') {
        await loadScript('sql-wasm.js');
      }
      if (typeof initSqlJs === 'undefined') {
        updateSearchStatus('Search unavailable');
        return;
      }
      var SQL = await initSqlJs({ locateFile: function(file) { return file; } });
      var response = await fetch(DB_PATH);
      if (!response.ok) throw new Error('not found');
      var buf = await response.arrayBuffer();
      db = new SQL.Database(new Uint8Array(buf));
      sqlReady = true;

      var countResult = db.exec('SELECT count(*) FROM articles');
      var articleCount = countResult[0] ? countResult[0].values[0][0] : '?';
      updateSearchStatus(articleCount + ' articles loaded');
    } catch (e) {
      updateSearchStatus('Search unavailable');
    }
  }

  function loadScript(src) {
    return new Promise(function(resolve, reject) {
      var s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  // ==================== SEARCH ====================
  function extractKeywords(text) {
    var stops = new Set([
      'i','me','my','we','our','you','your','he','she','it','they','them','the',
      'a','an','is','are','was','were','be','been','being','have','has','had',
      'do','does','did','will','would','could','should','can','may','might',
      'shall','must','to','of','in','for','on','with','at','by','from','as',
      'into','about','between','through','during','before','after','above',
      'below','up','down','out','off','over','under','again','further','then',
      'once','here','there','when','where','why','how','all','each','every',
      'both','few','more','most','other','some','such','no','not','only','own',
      'same','so','than','too','very','just','because','but','and','or','if',
      'what','which','who','whom','this','that','these','those','am','been',
      'don','t','s','re','ve','ll','d','m','let','got','get','go','want',
      'need','help','tell','show','give','make','know','think','walk','step'
    ]);
    return Array.from(new Set(
      text.toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/)
      .filter(function(w) { return w.length > 2 && !stops.has(w); })
    )).slice(0, 8);
  }

  function searchKnowledge(query) {
    if (!sqlReady || !db) return [];
    var keywords = extractKeywords(query);
    if (keywords.length === 0) return [];
    try {
      var stmt = db.prepare(
        'SELECT s.article_id, s.category, s.title, s.section_heading, ' +
        'snippet(search_index, 4, "", "", "...", 40) as snippet, rank ' +
        'FROM search_index s WHERE search_index MATCH ? ORDER BY rank LIMIT ?'
      );
      stmt.bind([keywords.join(' OR '), MAX_CONTEXT_SECTIONS]);
      var results = [];
      while (stmt.step()) {
        var row = stmt.getAsObject();
        results.push({ category: row.category, title: row.title, section: row.section_heading || '(intro)', snippet: row.snippet });
      }
      stmt.free();
      return results;
    } catch (e) { return []; }
  }

  function buildContextBlock(results) {
    if (results.length === 0) return '';
    var context = 'KNOWLEDGE BASE CONTEXT:\n';
    var total = 0;
    for (var i = 0; i < results.length; i++) {
      var r = results[i];
      var entry = '[' + r.category + '/' + r.title + ' > ' + r.section + ']\n' + r.snippet + '\n\n';
      if (total + entry.length > MAX_CONTEXT_CHARS) break;
      context += entry;
      total += entry.length;
    }
    context += 'Use the above context to answer. If context does not address the question, say so.\n\n';
    return context;
  }

  // ==================== CHAT ====================
  window.sendMessage = async function() {
    if (isGenerating) return;
    var input = document.getElementById('user-input');
    var text = input.value.trim();
    if (!text) return;

    var welcome = document.getElementById('welcome');
    if (welcome) welcome.style.display = 'none';

    appendMessage('user', text);
    input.value = '';
    input.style.height = 'auto';

    var searchResults = searchKnowledge(text);
    var contextBlock = buildContextBlock(searchResults);

    if (searchResults.length > 0) {
      updateSearchStatus(searchResults.length + ' relevant sections found');
    } else {
      updateSearchStatus(sqlReady ? 'No matching articles' : '');
    }

    var augmentedMessage = contextBlock ? contextBlock + 'USER QUESTION: ' + text : text;
    conversationHistory.push({ role: 'user', content: augmentedMessage });
    while (conversationHistory.length > MAX_HISTORY) conversationHistory.shift();

    var aiMsg = appendMessage('assistant', '', searchResults.length);
    var contentDiv = aiMsg.querySelector('.msg-content');
    contentDiv.innerHTML = '<div class="typing"><span></span><span></span><span></span></div>';

    isGenerating = true;
    document.getElementById('send-btn').disabled = true;

    try {
      var response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [{ role: 'system', content: systemPrompt }].concat(conversationHistory),
          stream: true, temperature: 0.4, top_p: 0.9, max_tokens: 1024
        })
      });

      if (!response.ok) throw new Error('Server returned ' + response.status);

      var reader = response.body.getReader();
      var decoder = new TextDecoder();
      var fullResponse = '';
      contentDiv.innerHTML = '';

      while (true) {
        var result = await reader.read();
        if (result.done) break;
        var chunk = decoder.decode(result.value, { stream: true });
        var lines = chunk.split('\n');
        for (var i = 0; i < lines.length; i++) {
          var line = lines[i].trim();
          if (!line.startsWith('data: ')) continue;
          var data = line.slice(6);
          if (data === '[DONE]') continue;
          try {
            var parsed = JSON.parse(data);
            var delta = parsed.choices && parsed.choices[0] && parsed.choices[0].delta;
            if (delta && delta.content) {
              fullResponse += delta.content;
              contentDiv.innerHTML = renderMarkdown(fullResponse);
              scrollToBottom();
            }
          } catch (e) {}
        }
      }

      conversationHistory.push({ role: 'assistant', content: fullResponse });

    } catch (e) {
      contentDiv.innerHTML =
        '<p style="color:var(--red)">Could not reach the AI server.</p>' +
        '<p style="color:var(--muted);font-size:.9em;margin-top:8px">Make sure the server is running (launch.bat). ' +
        'You can still use <a href="fallback.html" style="color:var(--accent)">Keyword Search</a> without the AI.</p>';
    }

    isGenerating = false;
    document.getElementById('send-btn').disabled = false;
    document.getElementById('user-input').focus();
  };

  // ==================== UI ====================
  function appendMessage(role, content, sourceCount) {
    var msg = document.createElement('div');
    msg.className = 'message ' + role;

    var bubble = document.createElement('div');
    bubble.className = 'msg-bubble';

    // Header
    var header = document.createElement('div');
    header.className = 'msg-header';
    var avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    avatar.textContent = role === 'user' ? 'Y' : 'AI';
    var name = document.createElement('div');
    name.className = 'msg-name';
    name.textContent = role === 'user' ? 'You' : 'SurvivalAI';
    header.appendChild(avatar);
    header.appendChild(name);
    bubble.appendChild(header);

    // Context badge
    if (role === 'assistant' && sourceCount > 0) {
      var badge = document.createElement('div');
      badge.className = 'context-badge';
      badge.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg> ' +
        sourceCount + ' source' + (sourceCount > 1 ? 's' : '') + ' referenced';
      bubble.appendChild(badge);
    }

    // Content
    var contentDiv = document.createElement('div');
    contentDiv.className = 'msg-content';
    if (content) contentDiv.innerHTML = renderMarkdown(content);
    bubble.appendChild(contentDiv);

    msg.appendChild(bubble);
    document.getElementById('messages').appendChild(msg);
    scrollToBottom();
    return msg;
  }

  function scrollToBottom() {
    var c = document.getElementById('messages-container');
    c.scrollTop = c.scrollHeight;
  }

  function updateSearchStatus(text) {
    var el = document.getElementById('search-status');
    if (el) el.textContent = text;
  }

  async function checkServer() {
    var dot = document.getElementById('server-dot');
    var badge = document.getElementById('mobile-status');
    var modelStatus = document.getElementById('model-status');

    try {
      var res = await fetch('/health');
      if (!res.ok) throw new Error();
      setReady();
    } catch (e) {
      try {
        var res2 = await fetch('/v1/models');
        if (res2.ok) { setReady(); return; }
      } catch(e2) {}

      // Retry a few times — model might still be loading
      var retries = 0;
      var interval = setInterval(async function() {
        retries++;
        try {
          var r = await fetch('/v1/models');
          if (r.ok) { setReady(); clearInterval(interval); return; }
        } catch(e) {}
        if (modelStatus) modelStatus.textContent = 'Loading model... (' + (retries * 3) + 's)';
        if (retries >= 20) {
          clearInterval(interval);
          if (dot) { dot.className = 'status-dot error'; }
          if (badge) { badge.textContent = 'Offline'; badge.className = 'status-badge'; }
          if (modelStatus) modelStatus.textContent = 'Server not detected';
          document.getElementById('send-btn').disabled = false;
        }
      }, 3000);
    }

    function setReady() {
      if (dot) { dot.className = 'status-dot ready'; }
      if (badge) { badge.textContent = 'Ready'; badge.className = 'status-badge ready'; }
      if (modelStatus) modelStatus.textContent = 'AI ready';
      document.getElementById('send-btn').disabled = false;
    }
  }

  // ==================== MARKDOWN ====================
  function renderMarkdown(text) {
    if (!text) return '';
    var html = escapeHtml(text);

    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, function(m, lang, code) {
      return '<pre><code>' + code.trim() + '</code></pre>';
    });
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
    html = html.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>');
    html = html.replace(/<\/blockquote>\n<blockquote>/g, '\n');
    html = html.replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>');
    html = html.replace(/(<li>.*<\/li>\n?)+/g, function(m) { return '<ol>' + m + '</ol>'; });
    html = html.replace(/^[-*] (.+)$/gm, '<li>$1</li>');

    html = html.replace(/^(\|.+\|)\n(\|[-| :]+\|)\n((\|.+\|\n?)+)/gm, function(m, header, sep, body) {
      var ths = header.split('|').filter(Boolean).map(function(c) { return '<th>' + c.trim() + '</th>'; }).join('');
      var rows = body.trim().split('\n').map(function(row) {
        return '<tr>' + row.split('|').filter(Boolean).map(function(c) { return '<td>' + c.trim() + '</td>'; }).join('') + '</tr>';
      }).join('');
      return '<table><thead><tr>' + ths + '</tr></thead><tbody>' + rows + '</tbody></table>';
    });

    html = html.replace(/\n\n/g, '</p><p>');
    html = html.replace(/\n/g, '<br>');
    html = '<p>' + html + '</p>';
    html = html.replace(/<p><(h[123]|blockquote|pre|ol|ul|table)/g, '<$1');
    html = html.replace(/<\/(h[123]|blockquote|pre|ol|ul|table)><\/p>/g, '</$1>');
    html = html.replace(/<p><\/p>/g, '');
    return html;
  }

  function escapeHtml(text) {
    var d = document.createElement('div');
    d.textContent = text;
    return d.innerHTML;
  }

  // ==================== START ====================
  document.addEventListener('DOMContentLoaded', init);

})();
