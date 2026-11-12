export const TILE_W = 26, TILE_H = 30, FONT_PX = 32;
export const FONT_FAMILY = '"JetBrains Mono", monospace';
export const MAX_SCALE = 1;
export const TILE_DIM = 0.35;
export const SHIFT_MS = 300;
export const REVEAL_MS = 350;
export const MOVE_MS = 90;

export const HELP = [
  ['Move/attack', 'QWEASDZXC'],
  ['Stairs, pick up', 'F'],
  ['Inventory', 'I  (WSAD select | f use | x drop)'],
  ['Help', '?'],
];

export const KEYS = {
  ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right',
  w: 'up', x: 'down', a: 'left', d: 'right', s: 'wait',
  q: 'up_left', e: 'up_right', z: 'down_left', c: 'down_right',
  '.': 'wait', f: 'interact', Enter: 'confirm',
};

export const fontFor = scale => `bold ${FONT_PX * scale}px ${FONT_FAMILY}`;
