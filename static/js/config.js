// Base metrics at scale 1; everything is scaled down to fit the window.
export const TILE_W = 26, TILE_H = 30, FONT_PX = 32;
export const FONT_FAMILY = '"JetBrains Mono", monospace';
export const MAX_SCALE = 1;
export const TILE_DIM = 0.35;      // opacity of the tile glyph under a monster or the player (1 = unchanged)
export const SHIFT_MS = 300;  // how long a tile takes to dim or brighten when it leaves or enters the view
export const REVEAL_MS = 350; // how long a newly discovered tile takes to fade in
export const MOVE_MS = 90; // duration of the glide between two positions

// Tiles in view are bright, tiles only remembered are dimmed.
export const COLORS = {
  '.': { seen: '#887', remembered: '#4a4a44' },
  '#': { seen: '#445', remembered: '#2a2a33' },
  '>': { seen: '#dd9', remembered: '#776' }, // stairs to the next floor
  '<': { seen: '#9bd', remembered: '#567' }, // stairs back down
  'Y': { seen: '#d6f', remembered: '#639' }, // the Grail of Chaos
  // Items lying on the floor, one glyph per part of the body
  '^': { seen: '#e8c547', remembered: '#6b5a22' }, // head
  '[': { seen: '#6fb7e8', remembered: '#2f526a' }, // body
  '/': { seen: '#e8806f', remembered: '#6a3a32' }, // hands
  '_': { seen: '#8fd18a', remembered: '#3f5f3d' }, // feet
  '*': { seen: '#ddd', remembered: '#555' },       // several items on one tile
};

export const HELP = [
  ['Move / attack', 'WASD or arrows'],
  ['Diagonally', 'Q E Z C'],
  ['Wait a turn', '.'],
  ['Stairs, pick up', 'F  (> climbs up, < goes back down)'],
  ['Inventory', 'I  (WSAD select | f use | x drop)'],
  ['Help', '?'],
];

export const KEYS = {
  ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right',
  w: 'up', s: 'down', a: 'left', d: 'right',
  q: 'up_left', e: 'up_right', z: 'down_left', c: 'down_right',
  '.': 'wait', f: 'interact', Enter: 'confirm',
};

export const fontFor = scale => `bold ${FONT_PX * scale}px ${FONT_FAMILY}`;
