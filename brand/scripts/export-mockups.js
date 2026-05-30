/**
 * Oli Brand — Hero / Mockup Export Pipeline
 * Exports all hero SVGs to PNG at multiple sizes.
 *
 * Outputs go to: /dist/heroes/
 *
 * Usage: npm run export:mockups
 */

const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const HEROES_DIR = path.join(ROOT, 'heroes');
const DIST_HEROES = path.join(ROOT, 'dist', 'heroes');

const PNG_SIZES = [512, 1024, 2048];

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

async function main() {
  console.log('\n🎨 Oli Brand — Mockup Export Pipeline\n');
  ensureDir(DIST_HEROES);

  const heroFiles = fs.readdirSync(HEROES_DIR).filter(f => f.endsWith('.svg'));

  if (heroFiles.length === 0) {
    console.log('No hero SVGs found in /heroes/');
    return;
  }

  for (const file of heroFiles) {
    const name = path.basename(file, '.svg');
    const srcPath = path.join(HEROES_DIR, file);
    const svgBuffer = fs.readFileSync(srcPath);

    for (const size of PNG_SIZES) {
      const out = path.join(DIST_HEROES, `${name}-${size}.png`);
      await sharp(svgBuffer)
        .resize(size)
        .png({ compressionLevel: 9 })
        .toFile(out);
      console.log(`  ✓ ${name}-${size}.png`);
    }
  }

  console.log('\n✅ All mockups exported to /dist/heroes/\n');
}

main().catch(err => {
  console.error('Mockup export failed:', err.message);
  process.exit(1);
});
