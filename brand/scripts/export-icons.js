/**
 * Oli Brand — App Icon Export Pipeline
 * Exports app icons for iOS, Android, macOS, Windows, PWA.
 *
 * Outputs go to: /dist/icons/
 *
 * Usage: npm run export:icons
 */

const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const ICON_SRC = path.join(ROOT, 'app-icons', 'app-icon-1024.svg');
const DIST_ICONS = path.join(ROOT, 'dist', 'icons');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

const ICON_SIZES = [
  // iOS
  { size: 20,   name: 'ios-20.png' },
  { size: 29,   name: 'ios-29.png' },
  { size: 40,   name: 'ios-40.png' },
  { size: 58,   name: 'ios-58.png' },
  { size: 60,   name: 'ios-60.png' },
  { size: 76,   name: 'ios-76.png' },
  { size: 80,   name: 'ios-80.png' },
  { size: 87,   name: 'ios-87.png' },
  { size: 120,  name: 'ios-120.png' },
  { size: 152,  name: 'ios-152.png' },
  { size: 167,  name: 'ios-167.png' },
  { size: 180,  name: 'ios-180.png' },
  { size: 1024, name: 'ios-1024.png' },
  // macOS
  { size: 16,   name: 'mac-16.png' },
  { size: 32,   name: 'mac-32.png' },
  { size: 64,   name: 'mac-64.png' },
  { size: 128,  name: 'mac-128.png' },
  { size: 256,  name: 'mac-256.png' },
  { size: 512,  name: 'mac-512.png' },
  { size: 1024, name: 'mac-1024.png' },
  // Android
  { size: 36,   name: 'android-36.png' },
  { size: 48,   name: 'android-48.png' },
  { size: 72,   name: 'android-72.png' },
  { size: 96,   name: 'android-96.png' },
  { size: 144,  name: 'android-144.png' },
  { size: 192,  name: 'android-192.png' },
  { size: 512,  name: 'android-512.png' },
  // PWA
  { size: 192,  name: 'pwa-192.png' },
  { size: 512,  name: 'pwa-512.png' },
  // Windows
  { size: 70,   name: 'win-70.png' },
  { size: 150,  name: 'win-150.png' },
  { size: 310,  name: 'win-310.png' },
  // Generic
  { size: 512,  name: 'icon-512.png' },
  { size: 1024, name: 'icon-1024.png' },
  { size: 2048, name: 'icon-2048.png' },
  { size: 4096, name: 'icon-4096.png' },
  { size: 8192, name: 'icon-8192.png' },
];

async function main() {
  console.log('\n🎨 Oli Brand — Icon Export Pipeline\n');

  if (!fs.existsSync(ICON_SRC)) {
    console.error(`Source icon not found: ${ICON_SRC}`);
    process.exit(1);
  }

  ensureDir(DIST_ICONS);
  const svgBuffer = fs.readFileSync(ICON_SRC);

  for (const { size, name } of ICON_SIZES) {
    const out = path.join(DIST_ICONS, name);
    await sharp(svgBuffer)
      .resize(size, size, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .png({ compressionLevel: 9 })
      .toFile(out);
    console.log(`  ✓ ${name} (${size}x${size})`);
  }

  console.log('\n✅ All icons exported to /dist/icons/\n');
}

main().catch(err => {
  console.error('Icon export failed:', err.message);
  process.exit(1);
});
