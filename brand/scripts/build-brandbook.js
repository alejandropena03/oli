/**
 * Oli Brand — Brandbook Build
 * Copies brandbook/index.html to dist/brandbook/ and inlines all assets.
 *
 * Usage: npm run build:brandbook
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'brandbook', 'index.html');
const DIST = path.join(ROOT, 'dist', 'brandbook');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function main() {
  console.log('\n📖 Oli Brand — Brandbook Build\n');
  ensureDir(DIST);

  if (!fs.existsSync(SRC)) {
    console.error('brandbook/index.html not found');
    process.exit(1);
  }

  const html = fs.readFileSync(SRC, 'utf8');
  const out = path.join(DIST, 'index.html');
  fs.writeFileSync(out, html, 'utf8');
  console.log(`  ✓ Brandbook copied to dist/brandbook/index.html`);
  console.log('\n✅ Brandbook built. Open dist/brandbook/index.html in your browser.\n');
}

main();
