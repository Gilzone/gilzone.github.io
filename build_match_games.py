#!/usr/bin/env python3
"""Build the four matching-game pages for gilzone.github.io.

One shared flip-card memory engine; each game plugs in its own lesson content:
  morse-match    letter  <->  Morse code pattern (tap a code to HEAR it)
  asl-match      sign photo  <->  English word
  chess-match    piece glyph  <->  piece name
  spanish-match  Spanish word  <->  English word (tap a card to hear it)
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects")

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>%%TITLE%%</title>
<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  html, body { margin: 0; padding: 0; }
  body { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; background: #f6f8fc;
         color: #17202e; min-height: 100vh; display: flex; flex-direction: column; }
  .topbar { display: flex; align-items: center; gap: 16px; padding: 14px 20px;
            background: #fff; border-bottom: 1px solid #e6e9f0; }
  .topbar a.back { color: #2b6bff; text-decoration: none; font-weight: 600; white-space: nowrap; }
  .topbar h1 { margin: 0; font-size: 18px; font-weight: 700; overflow: hidden;
               text-overflow: ellipsis; white-space: nowrap; }
  .wrap { max-width: 760px; width: 100%; margin: 0 auto; padding: 20px 16px 48px; }
  .hud { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-bottom: 6px; }
  .pill { background: #fff; border: 1px solid #e6e9f0; border-radius: 999px;
          padding: 8px 16px; font-size: 15px; font-weight: 600; }
  .pill b { color: #2b6bff; }
  #restart { margin-left: auto; border: 0; border-radius: 999px; background: #eef2ff;
             color: #2b6bff; font-weight: 700; font-size: 15px; padding: 9px 18px; cursor: pointer; }
  #restart:hover { background: #dfe7ff; }
  .hint { color: #5c6675; font-size: 15px; margin: 6px 0 16px; }
  .board { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
  @media (max-width: 480px) { .board { gap: 8px; } }
  .card { aspect-ratio: 1 / 1.12; perspective: 800px; cursor: pointer; }
  .card .inner { position: relative; width: 100%; height: 100%;
                 transform-style: preserve-3d; transition: transform .45s; }
  .card.open .inner, .card.done .inner { transform: rotateY(180deg); }
  .face { position: absolute; inset: 0; backface-visibility: hidden; -webkit-backface-visibility: hidden;
          border-radius: 16px; display: flex; align-items: center; justify-content: center;
          text-align: center; padding: 8px; overflow: hidden; }
  .front { background: linear-gradient(135deg, #2b6bff, #6a4dff); color: #fff;
           font-size: 40px; box-shadow: 0 6px 16px rgba(43,107,255,.30); }
  .card.done .front { visibility: hidden; }
  .back { background: #fff; border: 2px solid #e6e9f0; transform: rotateY(180deg);
          flex-direction: column; gap: 4px; }
  .card.done .back { border-color: #22c55e; background: #f0fdf4;
                     animation: pop .35s ease; }
  @keyframes pop { 0% { transform: rotateY(180deg) scale(1); }
                   50% { transform: rotateY(180deg) scale(1.08); }
                   100% { transform: rotateY(180deg) scale(1); } }
  .big { font-size: 52px; font-weight: 800; color: #17202e; line-height: 1; }
  .word { font-size: 19px; font-weight: 700; color: #17202e; line-height: 1.25; }
  .morse { font-size: 40px; font-weight: 800; color: #17202e; letter-spacing: 4px; line-height: 1; }
  .piece { font-size: 56px; line-height: 1; color: #17202e; }
  .emoji { font-size: 30px; }
  .esword { font-size: 22px; font-weight: 800; color: #17202e; }
  .enword { font-size: 17px; font-weight: 600; color: #5c6675; }
  .signimg { width: 100%; height: 100%; object-fit: cover; border-radius: 10px; }
  .tag { font-size: 11px; font-weight: 700; color: #8a94a6; text-transform: uppercase;
         letter-spacing: .08em; }
  .win { position: fixed; inset: 0; background: rgba(23,32,46,.55); display: flex;
         align-items: center; justify-content: center; z-index: 50; padding: 20px; }
  .win[hidden] { display: none; }
  .win .box { background: #fff; border-radius: 24px; padding: 36px 32px; text-align: center;
              max-width: 380px; width: 100%; box-shadow: 0 24px 64px rgba(0,0,0,.25); }
  .win .trophy { font-size: 64px; }
  .win h2 { margin: 8px 0 4px; font-size: 26px; }
  .win .stars { font-size: 36px; margin: 6px 0; letter-spacing: 4px; }
  .win p { color: #5c6675; margin: 0 0 20px; }
  .rowbtns { display: flex; gap: 12px; justify-content: center; }
  .rowbtns button, .rowbtns a { border: 0; border-radius: 12px; padding: 14px 22px;
      font-size: 16px; font-weight: 700; cursor: pointer; text-decoration: none; }
  #again { background: #2b6bff; color: #fff; }
  #again:hover { background: #1f58e0; }
  .rowbtns a { background: #eef1f6; color: #17202e; }
  footer { text-align: center; color: #8a94a6; font-size: 13px; margin-top: 28px; }
</style>
</head>
<body>
<div class="topbar">
  <a class="back" href="../../">&larr; All lessons</a>
  <h1>%%EMOJI%% %%TITLE%%</h1>
</div>
<div class="wrap">
  <div class="hud">
    <div class="pill">Moves <b id="moves">0</b></div>
    <div class="pill">&#9201; <b id="time">0:00</b></div>
    <div class="pill">&#11088; Pairs <b id="found">0/%%NPAIRS%%</b></div>
    <button id="restart">&#8635; Restart</button>
  </div>
  <p class="hint">%%HINT%%</p>
  <div class="board" id="board"></div>
  <footer>%%TITLE%% &mdash; made for Edwin&rsquo;s class.</footer>
</div>
<div class="win" id="win" hidden>
  <div class="box">
    <div class="trophy">&#x1F3C6;</div>
    <h2>You did it!</h2>
    <div class="stars" id="stars"></div>
    <p id="winStats"></p>
    <div class="rowbtns">
      <button id="again">PLAY AGAIN</button>
      <a href="../../">ALL LESSONS</a>
    </div>
  </div>
</div>
<script>
var PAIRS = %%PAIRS_JSON%%;
var NPAIRS = PAIRS.length;
var BACKEMOJI = "%%BACKEMOJI%%";

var board = document.getElementById("board");
var movesEl = document.getElementById("moves");
var timeEl = document.getElementById("time");
var foundEl = document.getElementById("found");
var winEl = document.getElementById("win");

var first = null, lock = false, moves = 0, found = 0, secs = 0, timer = null, started = false;

/* ---------- tiny synth ---------- */
var AC = null;
function ac() {
  if (!AC) { try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) {} }
  if (AC && AC.state === "suspended") { AC.resume(); }
  return AC;
}
function tone(freq, dur, when, type) {
  var c = ac(); if (!c) return;
  when = when || 0; type = type || "sine";
  var o = c.createOscillator(), g = c.createGain();
  o.type = type; o.frequency.value = freq;
  var t = c.currentTime + when;
  g.gain.setValueAtTime(0.0001, t);
  g.gain.exponentialRampToValueAtTime(0.25, t + 0.02);
  g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  o.connect(g); g.connect(c.destination);
  o.start(t); o.stop(t + dur + 0.05);
}
function sndFlip() { tone(520, 0.07); }
function sndMatch() { tone(660, 0.12); tone(880, 0.16, 0.1); }
function sndNo() { tone(196, 0.18, 0, "triangle"); }
function sndWin() { var n = [523, 659, 784, 1047]; for (var i = 0; i < n.length; i++) tone(n[i], 0.22, i * 0.14); }
function playMorse(pattern) {
  var c = ac(); if (!c) return;
  var t = 0;
  for (var i = 0; i < pattern.length; i++) {
    var d = pattern[i] === "-" ? 0.28 : 0.1;
    tone(700, d, t, "sine"); t += d + 0.09;
  }
}

/* ---------- speech ---------- */
function speak(text, lang) {
  try {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(text);
    u.lang = lang; u.rate = 0.9;
    window.speechSynthesis.speak(u);
  } catch (e) {}
}

/* ---------- game ---------- */
function shuffle(a) {
  a = a.slice();
  for (var i = a.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var t = a[i]; a[i] = a[j]; a[j] = t;
  }
  return a;
}
function fmt(s) { return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }
function startTimer() {
  if (started) return; started = true;
  timer = setInterval(function () { secs++; timeEl.textContent = fmt(secs); }, 1000);
}
function build() {
  var deck = [];
  PAIRS.forEach(function (p, i) {
    deck.push({ pair: i, html: p.a, fx: p.fx || null });
    deck.push({ pair: i, html: p.b, fx: p.fx || null });
  });
  deck = shuffle(deck);
  board.innerHTML = "";
  deck.forEach(function (c) {
    var d = document.createElement("div");
    d.className = "card";
    d.innerHTML = '<div class="inner"><div class="face front">' + BACKEMOJI +
      '</div><div class="face back">' + c.html + "</div></div>";
    d._pair = c.pair; d._fx = c.fx;
    d.addEventListener("click", function () { onFlip(d); });
    board.appendChild(d);
  });
  first = null; lock = false; moves = 0; found = 0; secs = 0; started = false;
  clearInterval(timer); timer = null;
  movesEl.textContent = "0"; timeEl.textContent = "0:00";
  foundEl.textContent = "0/" + NPAIRS;
  winEl.hidden = true;
}
function playFx(card) {
  if (!card._fx) return;
  if (card._fx.type === "morse") playMorse(card._fx.pattern);
  else if (card._fx.type === "say") speak(card._fx.text, card._fx.lang);
}
function onFlip(card) {
  if (lock || card.classList.contains("open") || card.classList.contains("done")) {
    if (card.classList.contains("open") && !card.classList.contains("done")) playFx(card);
    return;
  }
  startTimer();
  card.classList.add("open");
  sndFlip(); playFx(card);
  if (!first) { first = card; return; }
  moves++; movesEl.textContent = moves;
  if (first._pair === card._pair) {
    lock = true;
    var a = first, b = card; first = null;
    setTimeout(function () {
      a.classList.add("done"); b.classList.add("done");
      sndMatch();
      found++; foundEl.textContent = found + "/" + NPAIRS;
      lock = false;
      if (found === NPAIRS) win();
    }, 450);
  } else {
    lock = true;
    var x = first, y = card; first = null;
    sndNo();
    setTimeout(function () {
      x.classList.remove("open"); y.classList.remove("open");
      lock = false;
    }, 950);
  }
}
function win() {
  clearInterval(timer);
  sndWin();
  var stars = moves <= Math.ceil(NPAIRS * 1.6) ? 3 : (moves <= Math.ceil(NPAIRS * 2.4) ? 2 : 1);
  var s = "";
  for (var i = 0; i < 3; i++) s += i < stars ? "&#11088;" : "&#9734;";
  document.getElementById("stars").innerHTML = s;
  document.getElementById("winStats").textContent =
    NPAIRS + " pairs in " + moves + " moves, " + fmt(secs) + "!";
  setTimeout(function () { winEl.hidden = false; }, 500);
}
document.getElementById("restart").addEventListener("click", build);
document.getElementById("again").addEventListener("click", build);
build();
</script>
</body>
</html>
"""

import json

def card_a(html): return html

GAMES = {
    "morse-match": {
        "title": "Morse Matching Game",
        "emoji": "&#x1F4FB;",
        "back": "&#x1F4FB;",
        "hint": "Flip two cards and match each letter with its Morse code. Tap an open code card to HEAR it — short beep = dot, long beep = dash.",
        "pairs": [
            ("E", '<div class="big">E</div>', '<div class="morse">&bull;</div>', "."),
            ("T", '<div class="big">T</div>', '<div class="morse">&minus;</div>', "-"),
            ("A", '<div class="big">A</div>', '<div class="morse">&bull;&minus;</div>', ".-"),
            ("S", '<div class="big">S</div>', '<div class="morse">&bull;&bull;&bull;</div>', "..."),
            ("O", '<div class="big">O</div>', '<div class="morse">&minus;&minus;&minus;</div>', "---"),
            ("H", '<div class="big">H</div>', '<div class="morse">&bull;&bull;&bull;&bull;</div>', "...."),
            ("I", '<div class="big">I</div>', '<div class="morse">&bull;&bull;</div>', ".."),
            ("N", '<div class="big">N</div>', '<div class="morse">&minus;&bull;</div>', "-."),
        ],
        "fx": "morse",
    },
    "asl-match": {
        "title": "ASL Matching Game",
        "emoji": "&#x1F90C;",
        "back": "&#x1F90C;",
        "hint": "Flip two cards and match each sign photo with its word. Make the sign with your own hands when you find a pair!",
        "pairs": [
            ("please", None, "please.jpg"),
            ("thank you", None, "thankyou.jpg"),
            ("sorry", None, "sorry.jpg"),
            ("help", None, "help.jpg"),
            ("yes", None, "yes.jpg"),
            ("no", None, "no.jpg"),
            ("stop", None, "stop.jpg"),
            ("ready", None, "ready.jpg"),
        ],
        "fx": None,
        "asl": True,
    },
    "chess-match": {
        "title": "Chess Matching Game",
        "emoji": "&#x265E;",
        "back": "&#x265E;",
        "hint": "Flip two cards and match each chess piece with its name. Say hello to the team as you find them!",
        "pairs": [
            ("Pawn", "&#x265F;"),
            ("Knight", "&#x265E;"),
            ("Rook", "&#x265C;"),
            ("Bishop", "&#x265D;"),
            ("Queen", "&#x265B;"),
            ("King", "&#x265A;"),
        ],
        "fx": None,
        "chess": True,
    },
    "spanish-match": {
        "title": "Spanish Matching Game",
        "emoji": "&#x1F1EA;&#x1F1F8;",
        "back": "&#x1F1EA;&#x1F1F8;",
        "hint": "Flip two cards and match the Spanish word with its English meaning. Tap an open card to hear it out loud!",
        "pairs": [
            ("hola", "hello", "&#x1F44B;", "es"),
            ("adi\u00f3s", "goodbye", "&#x1F64B;", "es"),
            ("buenos d\u00edas", "good morning", "&#x2600;&#xFE0F;", "es"),
            ("buenas noches", "good night", "&#x1F319;", "es"),
            ("gracias", "thank you", "&#x1F64F;", "es"),
            ("por favor", "please", "&#x2728;", "es"),
            ("s\u00ed", "yes", "&#x2705;", "es"),
            ("no", "no", "&#x274C;", "es"),
        ],
        "fx": "say",
        "spanish": True,
    },
}

def build_pairs(slug, g):
    out = []
    if g.get("asl"):
        for word, _, img in g["pairs"]:
            a = '<img class="signimg" src="../asl-basic-signs-1/img/%s" alt="Sign for %s" />' % (img, word)
            b = '<div class="tag">ASL sign</div><div class="word">%s</div>' % word
            out.append({"a": a, "b": b})
    elif g.get("chess"):
        for name, glyph in g["pairs"]:
            a = '<div class="piece">%s</div>' % glyph
            b = '<div class="tag">chess piece</div><div class="word">%s</div>' % name
            fx = {"type": "say", "text": name, "lang": "en-US"}
            out.append({"a": a, "b": b, "fx": fx})
    elif g.get("spanish"):
        for es, en, emoji, lang in g["pairs"]:
            a = ('<div class="emoji">%s</div><div class="esword">%s</div>'
                 '<div class="tag">tap to hear</div>' % (emoji, es))
            b = '<div class="enword">%s</div>' % en
            fx = {"type": "say", "text": es, "lang": "es-US"}
            out.append({"a": a, "b": b, "fx": fx})
    else:  # morse
        for letter, a_html, b_html, pattern in g["pairs"]:
            a = a_html
            b = b_html + '<div class="tag">tap to hear</div>'
            fx = {"type": "morse", "pattern": pattern}
            out.append({"a": a, "b": b, "fx": fx})
    return out

for slug, g in GAMES.items():
    pairs = build_pairs(slug, g)
    html = PAGE
    html = html.replace("%%TITLE%%", g["title"])
    html = html.replace("%%EMOJI%%", g["emoji"])
    html = html.replace("%%BACKEMOJI%%", g["back"])
    html = html.replace("%%HINT%%", g["hint"])
    html = html.replace("%%NPAIRS%%", str(len(pairs)))
    html = html.replace("%%PAIRS_JSON%%", json.dumps(pairs))
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(html)
    print("wrote", slug, "->", len(pairs), "pairs")
