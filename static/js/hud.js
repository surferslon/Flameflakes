import { damageEl, defenseEl, floorEl, hpEl, logEl, speedEl } from './dom.js';

const LINE_H = 26;
const LOG_MS = 300;
const lines = new Map();
let running = false;

// Driven from JavaScript (like the level), so it does not depend on CSS transitions or
// on the system's "reduce motion" setting.
function tick(now) {
  let active = false;
  for (const [id, line] of lines) {
    const a = line.anim;
    const t = Math.min(1, (now - a.start) / LOG_MS);
    const ease = 1 - (1 - t) * (1 - t);
    line.y = a.fromY + (a.toY - a.fromY) * ease;
    line.o = a.fromO + (a.toO - a.fromO) * ease;
    line.el.style.transform = `translateY(${line.y}px)`;
    line.el.style.opacity = line.o;
    if (t < 1) active = true;
    else if (line.dying) { line.el.remove(); lines.delete(id); }
  }
  running = active;
  if (active) requestAnimationFrame(tick);
}

function moveTo(line, y, o) {
  line.anim = { fromY: line.y, toY: y, fromO: line.o, toO: o, start: performance.now() };
  if (!running) { running = true; requestAnimationFrame(tick); }
}

function updateLog(texts, ids) {
  ids.forEach((id, row) => {
    let line = lines.get(id);
    if (!line) {
      const el = document.createElement('div');
      el.className = 'log-line';
      el.textContent = texts[row];  // textContent, not innerHTML: "<press enter>" is not a tag
      logEl.append(el);
      line = { el, y: -LINE_H, o: 0, dying: false };
      el.style.transform = `translateY(${line.y}px)`;
      el.style.opacity = 0;
      lines.set(id, line);
    }
    moveTo(line, row * LINE_H, 1);
  });
  for (const [id, line] of lines) {
    if (ids.includes(id) || line.dying) continue;
    line.dying = true;
    moveTo(line, line.y, 0);
  }
}

export function updateHud(s) {
  floorEl.textContent = s.blank ? '' : `FLOOR ${s.floor}/${s.floors}`;
  speedEl.textContent = s.blank ? '' : `SP ${s.speed}`;
  damageEl.textContent = s.blank ? '' : `DM ${s.damage}`;
  defenseEl.textContent = s.blank ? '' : `DV/PV ${s.dv}/${s.pv}`;
  hpEl.textContent = s.blank ? '' : `HP ${s.hp}`;
  updateLog(s.messages, s.message_ids);
}

export function showDisconnected() {
  lines.clear();
  logEl.textContent = 'Disconnected.';
}
