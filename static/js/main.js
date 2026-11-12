import { fontFor } from './config.js';
import { showDisconnected, updateHud } from './hud.js';
import { bindKeys } from './input.js';
import { refresh, setPalette, setState } from './render.js';

document.fonts.load(fontFor(1)).then(refresh);
window.addEventListener('resize', refresh);

setPalette(await (await fetch('/palette')).json());

const sock = new WebSocket(`${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/ws`);
sock.onmessage = e => {
  const s = JSON.parse(e.data);
  updateHud(s);
  setState(s);
};
sock.onclose = showDisconnected;
bindKeys(sock);
