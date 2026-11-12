import { KEYS } from './config.js';
import { closeScreen, currentScreen, inventoryRequest, isBlank, isScreenOpen, moveCursor, openScreen } from './render.js';

const SCREENS = { i: 'inventory', '?': 'help' };

const CURSOR_KEYS = {
  ArrowUp: [0, -1], w: [0, -1], ArrowDown: [0, 1], s: [0, 1],
  ArrowLeft: [-1, 0], a: [-1, 0], ArrowRight: [1, 0], d: [1, 0],
};
const INVENTORY_KEYS = { Enter: 'use', f: 'use', x: 'drop' };

export function bindKeys(sock) {
  const send = message => sock.readyState === WebSocket.OPEN && sock.send(JSON.stringify(message));

  window.addEventListener('keydown', e => {
    if (isScreenOpen()) {
      if (e.key === 'Escape') {
        e.preventDefault();
        closeScreen();
      } else if (currentScreen() === 'inventory') {
        if (CURSOR_KEYS[e.key]) {
          e.preventDefault();
          moveCursor(...CURSOR_KEYS[e.key]);
        } else if (INVENTORY_KEYS[e.key]) {
          e.preventDefault();
          const request = inventoryRequest(INVENTORY_KEYS[e.key]);
          if (request) send(request);
        }
      }
      return;
    }
    if (SCREENS[e.key] && !isBlank()) {
      e.preventDefault();
      openScreen(SCREENS[e.key]);
      return;
    }
    const action = KEYS[e.key];
    if (action) {
      e.preventDefault();
      send({ action });
    }
  });
}
