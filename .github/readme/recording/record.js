// Builds ../check-text.gif: a replay of the real output of scripts/check_text.py on invented text.
// Needs Node, Playwright and ffmpeg. Run from the repo root: node .github/readme/recording/record.js
const { chromium } = require('playwright');
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const DIR = __dirname;
const SCRIPT = 'scripts/check_text.py';
const RUNS = [['before.txt', 'rewrite-1.txt'], ['before.txt', 'rewrite-2.txt']];
const W = 840, H = 300, FPS = 10;

function transcript() {
  const out = [];
  for (const [a, b] of RUNS) {
    const r = spawnSync('python3', [SCRIPT, path.join(DIR, a), path.join(DIR, b)], { encoding: 'utf8' });
    const cmd = `python3 ${SCRIPT} ${a} ${b}`;
    const body = (r.stdout + r.stderr).split(path.join(DIR, '/')).join('').trimEnd();
    out.push({ cmd, body: body + `\n[exit ${r.status}]`, bad: r.status !== 0 });
  }
  return out;
}

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

function frames(steps) {
  // each frame is a list of finished blocks plus the block being typed
  const f = [];
  const hold = n => { for (let i = 0; i < n; i++) f.push(f[f.length - 1]); };
  const done = [];
  f.push({ done: [], typing: '', body: null });
  for (const s of steps) {
    for (let n = 2; n <= s.cmd.length + 1; n += 2) f.push({ done: [...done], typing: s.cmd.slice(0, n), body: null });
    hold(5);
    f.push({ done: [...done], typing: s.cmd, body: s });
    hold(25);
    done.push(s);
  }
  hold(15);
  return f;
}

function html(fr) {
  const line = s => `<div class="cmd"><span class="p">$</span> ${esc(s)}</div>`;
  const block = s => line(s.cmd) + `<pre class="${s.bad ? 'bad' : 'ok'}">${esc(s.body)}</pre>`;
  const inner = fr.done.map(block).join('') + (fr.body ? block(fr.body) : line(fr.typing) + '');
  return `<style>body{margin:0;background:#0f1628;font:15px/1.5 ui-monospace,Menlo,Consolas,monospace;color:#f3ecdc}
.bar{height:30px;background:#1b2440;border-bottom:2px solid #2a3558;display:flex;align-items:center;gap:7px;padding-left:12px}
.bar i{width:11px;height:11px;border-radius:50%;background:#2a3558}.t{padding:14px 18px}.p{color:#4fd18b}
pre{margin:2px 0 12px;font:inherit}.bad{color:#ff8a8a}.ok{color:#4fd18b}.cmd{white-space:pre}</style>
<div class="bar"><i></i><i></i><i></i></div><div class="t">${inner}</div>`;
}

(async () => {
  const fr = frames(transcript());
  const tmp = fs.mkdtempSync('/tmp/rec-');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  for (let i = 0; i < fr.length; i++) {
    await p.setContent(html(fr[i]));
    await p.screenshot({ path: `${tmp}/${String(i).padStart(4, '0')}.png` });
  }
  await b.close();
  const gif = path.join(DIR, '..', 'check-text.gif');
  const r = spawnSync('ffmpeg', ['-loglevel', 'error', '-y', '-framerate', String(FPS), '-i', `${tmp}/%04d.png`, '-vf',
    'split[a][b];[a]palettegen=max_colors=24[p];[b][p]paletteuse=dither=none', gif], { stdio: 'inherit' });
  fs.rmSync(tmp, { recursive: true });
  process.exit(r.status);
})();
