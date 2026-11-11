import { canvas, ctx, headerEl, logEl } from './dom.js';
import { COLORS, HELP, MAX_SCALE, MOVE_MS, REVEAL_MS, SHIFT_MS, TILE_DIM, TILE_H, TILE_W, fontFor } from './config.js';

let state = null;       // latest server state
let metrics = null;     // { scale, tw, th } for the current window size
let baseLayer = null;   // offscreen canvas with the discovered level
let anim = { from: new Map(), start: 0 }; // entity id -> {x, y} at animation start
let shown = new Map();  // entity id -> {x, y} as last drawn
let revealed = new Set();   // tiles of this level that have been drawn at least once ("x,y")
let revealedLevel = null;
let fresh = [];             // recently discovered tiles { x, y, ch, born }: faded in, not part of baseLayer
let modes = new Map();      // "x,y" -> 'seen' | 'remembered' as of the last state
let shifting = new Map();   // "x,y" -> { x, y, ch, from, to, born }: tiles changing brightness, drawn separately
let skipKeys = new Set();   // tiles not in baseLayer because they are fading in or changing brightness
let screen = null;      // null (the level), 'inventory' or 'help': drawn instead of the level

// Largest scale at which the level plus header and log fit into the window.
function fitScale(s) {
  const logSpace = logEl.offsetHeight + parseFloat(getComputedStyle(logEl).marginTop);
  const availW = window.innerWidth - 16;
  const availH = window.innerHeight - headerEl.offsetHeight - logSpace - 16;
  return Math.min(MAX_SCALE, availW / (s.w * TILE_W), availH / (s.h * TILE_H));
}

// Glyphs without a fixed color (the level of chaos) get a stable color from their character.
function chaosColor(ch, mode) {
  const hue = (ch.charCodeAt(0) * 37) % 360;
  return mode === 'seen' ? `hsl(${hue} 22% 62%)` : `hsl(${hue} 12% 30%)`;
}

function glyph(c, ch, x, y, col, m) {
  c.fillStyle = col;
  c.fillText(ch, x * m.tw + m.tw / 2, y * m.th + m.th / 2);
}

// Color of a level glyph; tiles that are out of view are dimmed.
function tileColor(ch, mode) {
  return COLORS[ch]?.[mode] ?? chaosColor(ch, mode);
}

// The tile under an entity (player or monster) gets dimmer, so the entity stands out. Only the
// glyph of that tile is dimmed (no box is drawn): erase it from the level and redraw it faint.
function dimTileUnder(x, y, m) {
  const tx = Math.round(x), ty = Math.round(y);
  const ch = state.map[ty]?.[tx];
  if (!ch || ch === ' ') return;
  ctx.clearRect(Math.floor(tx * m.tw), Math.floor(ty * m.th), Math.ceil(m.tw), Math.ceil(m.th));
  ctx.globalAlpha = TILE_DIM;
  glyph(ctx, ch, tx, ty, tileColor(ch, 'seen'), m);
  ctx.globalAlpha = 1;
}

const clamp01 = v => Math.max(0, Math.min(1, v));

// Colors are blended as [r, g, b]; level colors are hex, the level of chaos uses hsl().
function toRgb(color) {
  if (color[0] === '#') {
    const hex = color.length === 4 ? [...color.slice(1)].map(c => c + c).join('') : color.slice(1);
    const n = parseInt(hex, 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  const [h, s, l] = color.match(/[\d.]+/g).map(Number);
  const k = n => (n + h / 30) % 12, a = (s / 100) * Math.min(l / 100, 1 - l / 100);
  const f = n => 255 * (l / 100 - a * Math.max(-1, Math.min(k(n) - 3, 9 - k(n), 1)));
  return [f(0), f(8), f(4)];
}

// What a tile that is changing brightness looks like at this moment, as [r, g, b].
function shiftRgb(rec, now) {
  const t = clamp01((now - rec.born) / SHIFT_MS);
  return rec.from.map((v, i) => v + (rec.to[i] - v) * t);
}

// Renders the discovered level into an offscreen canvas. Redrawn whenever the
// state or window changes, because what is visible/remembered changes every turn.
function renderBase(s, m, skip) {
  const layer = document.createElement('canvas');
  layer.width = canvas.width; layer.height = canvas.height;
  const c = layer.getContext('2d');
  c.font = fontFor(m.scale); c.textAlign = 'center'; c.textBaseline = 'middle';
  s.map.forEach((row, y) => [...row].forEach((ch, x) => {
    if (ch === ' ' || skip.has(`${x},${y}`)) return; // undiscovered, or fading in separately
    const mode = s.visible[y][x] === '1' ? 'seen' : 'remembered';
    glyph(c, ch, x, y, tileColor(ch, mode), m);
  }));
  return layer;
}

function layout() {
  const scale = fitScale(state);
  metrics = { scale, tw: TILE_W * scale, th: TILE_H * scale };
  canvas.width = Math.floor(state.w * metrics.tw);
  canvas.height = Math.floor(state.h * metrics.th);
  document.documentElement.style.setProperty('--game-w', `${canvas.width}px`);
  baseLayer = renderBase(state, metrics, skipKeys);
}

// Draws text on the tile grid, one character per tile, like the level itself.
function drawText(m, col, row, str, color) {
  [...str].forEach((ch, i) => ch !== ' ' && glyph(ctx, ch, col + i, row, color, m));
}

// Help screen: what each key does.
function drawHelp(m) {
  ctx.font = fontFor(m.scale); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  drawText(m, 2, 1, 'HELP', '#fff');
  const width = Math.max(...HELP.map(([what]) => what.length)) + 3;
  HELP.forEach(([what, keys], i) => {
    drawText(m, 2, 3 + i, what, '#887');
    drawText(m, 2 + width, 3 + i, keys, '#fff');
  });
  drawText(m, 2, state.h - 2, 'ESC to close', '#4a4a44');
}

// Inventory screen: plain text on the same tile grid and font as the level.
// Left column: what is worn. Right column: what is carried in the backpack.
// Cursor in the inventory: column 0 = what is worn, column 1 = the backpack.
let cursor = { col: 0, row: 0 };

function clampCursor() {
  const lengths = [Object.keys(state.equipment).length, state.backpack.length];
  if (cursor.col === 1 && lengths[1] === 0) cursor.col = 0;
  cursor.row = Math.max(0, Math.min(lengths[cursor.col] - 1, cursor.row));
}

export function moveCursor(dCol, dRow) {
  if (!state) return;
  cursor.col = Math.max(0, Math.min(1, cursor.col + dCol));
  cursor.row += dRow;
  clampCursor();
  refresh();
}

// What the player's choice under the cursor means for the server, or null.
export function inventoryRequest(kind) {
  if (!state) return null;
  clampCursor();
  if (cursor.col === 0) {
    const slot = Object.keys(state.equipment)[cursor.row];
    return kind === 'use' && state.equipment[slot] ? { action: 'unequip', arg: slot } : null;
  }
  if (state.backpack.length === 0) return null;
  return { action: kind === 'drop' ? 'drop' : 'equip', arg: cursor.row };
}

// Inventory screen: plain text on the same tile grid and font as the level.
// Left column: what is worn. Right column: what is carried in the backpack.
function drawInventory(m) {
  ctx.font = fontFor(m.scale); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  const text = (col, row, str, color) => drawText(m, col, row, str, color);
  const dim = '#4a4a44', label = '#887', bright = '#fff';
  const top = 5;  // first list row: one blank row below the titles
  clampCursor();
  text(2, 1, `INVENTORY  ${state.weight}/${state.capacity} kg`, bright);

  const slots = Object.entries(state.equipment);
  const labelWidth = Math.max(...slots.map(([slot]) => slot.length)) + 2;
  text(2, 3, 'EQUIPMENT', bright);
  slots.forEach(([slot, item], i) => {
    text(2, top + i, slot, label);
    text(2 + labelWidth, top + i, item ?? '-', item ? bright : dim);
  });

  const col = Math.floor(state.w / 2) + 2;
  text(col, 3, 'BACKPACK', bright);
  if (state.backpack.length === 0) text(col, top, '(empty)', dim);
  state.backpack.forEach((item, i) => text(col, top + i, item, bright));

  text(cursor.col === 0 ? 1 : col - 1, top + cursor.row, '>', bright);  // the cursor
  text(2, state.h - 3, 'WSAD select | f use | x drop', dim);
  text(2, state.h - 2, 'ESC to close', dim);
}

// One animation loop at a time; frames use performance.now() (not the timestamp requestAnimationFrame
// passes in, which can be earlier than a time stamped just before and would give negative ages).
let frameQueued = false;
function scheduleFrame() {
  if (frameQueued) return;
  frameQueued = true;
  requestAnimationFrame(() => { frameQueued = false; frame(); });
}

function frame() {
  if (!state) return;
  const now = performance.now();
  const m = metrics;
  if (state.blank) {  // black screen: during the intro and after death the story is told in the log only
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    return;
  }
  if (screen) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    (screen === 'help' ? drawHelp : drawInventory)(m);
    return;
  }
  const t = clamp01((now - anim.start) / MOVE_MS);
  const ease = 1 - (1 - t) * (1 - t); // ease-out
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(baseLayer, 0, 0);
  ctx.font = fontFor(m.scale); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  // Tiles discovered just now fade in, each from the moment it was discovered.
  let revealing = false;
  fresh.forEach(({ x, y, ch, born }) => {
    const alpha = clamp01((now - born) / REVEAL_MS);
    if (alpha < 1) revealing = true;
    ctx.globalAlpha = alpha;
    glyph(ctx, ch, x, y, tileColor(ch, state.visible[y][x] === '1' ? 'seen' : 'remembered'), m);
  });
  ctx.globalAlpha = 1;
  // Tiles entering or leaving the player's view change brightness smoothly.
  shifting.forEach(rec => {
    if (now - rec.born < SHIFT_MS) revealing = true;
    glyph(ctx, rec.ch, rec.x, rec.y, `rgb(${shiftRgb(rec, now).map(Math.round).join(', ')})`, m);
  });
  shown = new Map();
  // Draw the player last so it is never hidden behind another glyph.
  const entities = [...state.entities].sort((a, b) => (a.ch === '@') - (b.ch === '@')).map(e => {
    const f = anim.from.get(e.id) ?? e;
    const x = f.x + (e.x - f.x) * ease, y = f.y + (e.y - f.y) * ease;
    shown.set(e.id, { x, y });
    return { e, x, y };
  });
  entities.forEach(({ x, y }) => dimTileUnder(x, y, m));
  entities.forEach(({ e, x, y }) => glyph(ctx, e.ch, x, y, e.color, m));
  if (t < 1 || revealing) scheduleFrame();
}

// Redraw the current state, e.g. after a resize or once the font has loaded.
export function refresh() {
  if (!state) return;
  layout();
  frame();  // draw right away: the canvas was just cleared by layout() and must never be seen empty
}

// Show a new server state, gliding entities from where they are on screen now.
export function setState(s) {
  const sameLevel = state && state.level === s.level;
  const now = performance.now();
  anim = { from: sameLevel ? shown : new Map(), start: now };
  state = s;
  // Which tiles does the player see for the first time, which ones changed from seen to remembered
  // (or back)? Nothing counts as seen while the screen is blank.
  if (revealedLevel !== s.level) {
    revealed = new Set(); revealedLevel = s.level; fresh = []; modes = new Map(); shifting = new Map();
  }
  fresh = fresh.filter(f => now - f.born < REVEAL_MS);  // tiles still fading in keep fading
  for (const [key, rec] of shifting) if (now - rec.born >= SHIFT_MS) shifting.delete(key);
  const fading = new Set(fresh.map(({ x, y }) => `${x},${y}`));
  if (!s.blank) {
    s.map.forEach((row, y) => [...row].forEach((ch, x) => {
      if (ch === ' ') return;
      const key = `${x},${y}`;
      const mode = s.visible[y][x] === '1' ? 'seen' : 'remembered';
      if (!revealed.has(key)) {
        revealed.add(key); fresh.push({ x, y, ch, born: now }); fading.add(key);
      } else if (modes.get(key) !== mode && !fading.has(key)) {
        const rec = shifting.get(key);  // start from what is on screen right now, even mid-change
        const from = rec ? shiftRgb(rec, now) : toRgb(tileColor(ch, modes.get(key)));
        shifting.set(key, { x, y, ch, from, to: toRgb(tileColor(ch, mode)), born: now });
      }
      modes.set(key, mode);
    }));
  }
  skipKeys = new Set([...fresh, ...shifting.values()].map(({ x, y }) => `${x},${y}`));
  refresh();
}

export const isScreenOpen = () => screen !== null;
export const currentScreen = () => screen;
export const isBlank = () => Boolean(state?.blank);

// Show the named screen instead of the level. Esc closes it again (see input.js).
export function openScreen(name) {
  screen = name;
  refresh();
}

export function closeScreen() {
  screen = null;
  refresh();
}
