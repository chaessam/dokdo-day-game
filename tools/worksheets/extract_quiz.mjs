import fs from 'fs'; import vm from 'vm';
const src = fs.readFileSync(new URL('../../src/game.html', import.meta.url), 'utf8');
const grab = (start) => { const i = src.indexOf(start); if (i < 0) throw new Error(start); let depth = 0, j = src.indexOf(start.endsWith('{') ? '{' : '[', i + start.length - 1); for (let k = j; k < src.length; k++) { const c = src[k]; if (c === '[' || c === '{') depth++; else if (c === ']' || c === '}') { depth--; if (depth === 0) return src.slice(j, k + 1); } else if (c === '"' || c === '`' || c === "'") { const q = c; k++; while (src[k] !== q) { if (src[k] === '\\') k++; k++; } } } };
const out = {};
for (const [name, start] of [['RECORDS', 'const RECORDS = ['], ['SEA', 'const SEA = ['], ['SPOTS', 'const SPOTS = ['], ['WEATHER', 'const WEATHER_NOTE = {']]) {
  try { out[name] = vm.runInNewContext('(' + grab(start) + ')'); } catch (e) { out[name] = 'ERR ' + e.message; }
}
fs.writeFileSync(process.argv[2], JSON.stringify(out, null, 1));
for (const k of Object.keys(out)) { const v = out[k]; console.log(k, Array.isArray(v) ? v.length + ' items, quiz=' + v.filter(x => x.quiz).length : (typeof v === 'string' ? v : 'obj quiz=' + !!v.quiz)); }
