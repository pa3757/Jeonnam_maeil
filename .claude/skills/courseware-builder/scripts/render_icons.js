// Render Lucide line icons (react-icons/lu) to PNG for slide icon swaps.
//
// Usage: node render_icons.js spec.json out_dir
// spec.json: [
//   {"icon":"LuSearch","color":"#FFFFFF","file":"w_search.png"},                      // plain icon, 256px
//   {"icon":"LuSun","color":"#FF4E33","file":"t_sun.png","tile":{"w":814,"h":556,"bg":"#FFE9E5"}} // icon on a tinted tile
// ]
// Needs react, react-dom, react-icons, sharp. If `require` fails:
//   mkdir -p <scratch>/node && cd <scratch>/node && npm init -y && npm i react react-dom react-icons sharp
//   NODE_PATH=<scratch>/node/node_modules node render_icons.js spec.json out
// Pick colors from the template palette (sample pixels from a render) so icons match.
const fs = require('fs'), path = require('path');
const React = require('react'), RDS = require('react-dom/server'), sharp = require('sharp'), lu = require('react-icons/lu');

const svgOf = (name, color, size, stroke) => {
  if (!lu[name]) throw new Error(`unknown icon ${name} (see https://react-icons.github.io/react-icons/icons/lu/)`);
  return RDS.renderToStaticMarkup(React.createElement(lu[name], { color, size: String(size) }))
    .replace('stroke-width="2"', `stroke-width="${stroke}"`);
};

(async () => {
  const [specPath, out] = process.argv.slice(2);
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  fs.mkdirSync(out, { recursive: true });
  for (const it of spec) {
    const dest = path.join(out, it.file);
    if (it.tile) {
      const { w, h, bg } = it.tile, s = Math.round(Math.min(w, h) * 0.54);
      const inner = svgOf(it.icon, it.color, s, 1.5)
        .replace(`height="${s}" width="${s}"`, '')
        .replace('<svg', `<svg x="${(w - s) / 2}" y="${(h - s) / 2}" width="${s}" height="${s}"`);
      const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">` +
        `<rect width="${w}" height="${h}" rx="${Math.round(w * 0.027)}" fill="${bg}"/>` +
        `<circle cx="${w / 2}" cy="${h / 2}" r="${Math.round(Math.min(w, h) * 0.34)}" fill="#FFFFFF" opacity="0.65"/>${inner}</svg>`;
      await sharp(Buffer.from(svg)).png().toFile(dest);
    } else {
      await sharp(Buffer.from(svgOf(it.icon, it.color, 256, it.stroke || 1.6))).resize(256, 256).png().toFile(dest);
    }
    console.log('wrote', dest);
  }
})().catch(e => { console.error(e.message); process.exit(1); });
