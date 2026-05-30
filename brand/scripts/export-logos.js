/**
 * Oli Brand — Logo Export Pipeline
 * Exports all Route A wordmark SVGs to PNG (multiple sizes), optimized SVG, and ICO.
 *
 * Outputs go to: /dist/logos/
 *
 * Usage: npm run export:logos
 */

const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
const { optimize } = require('svgo');

const ROOT = path.resolve(__dirname, '..');
const LOGOS_DIR = path.join(ROOT, 'logos', 'route-a-wordmark');
const DIST_DIR = path.join(ROOT, 'dist', 'logos');

const PNG_SIZES = [512, 1024, 2048, 4096, 8192];

// All logo variants to export
const VARIANTS = [
  'full-dark',
  'full-light',
  'full-mono',
  'horizontal-dark',
  'horizontal-light',
  'horizontal-mono',
  'icon-dark',
  'icon-light',
  'icon-mono',
];

// Ensure dist directory exists
function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

// Optimize SVG with svgo
function optimizeSvg(svgContent) {
  const result = optimize(svgContent, {
    plugins: [
      { name: 'preset-default' },
      { name: 'removeDimensions' },
    ],
  });
  return result.data;
}

async function exportVariant(variant) {
  const srcPath = path.join(LOGOS_DIR, `${variant}.svg`);
  if (!fs.existsSync(srcPath)) {
    console.warn(`  SKIP: ${variant}.svg not found`);
    return;
  }

  const svgContent = fs.readFileSync(srcPath, 'utf8');
  const variantDir = path.join(DIST_DIR, variant);
  ensureDir(variantDir);

  // 1. Optimized SVG
  const optimized = optimizeSvg(svgContent);
  const svgOut = path.join(variantDir, `${variant}.svg`);
  fs.writeFileSync(svgOut, optimized, 'utf8');
  console.log(`  SVG  → ${path.relative(ROOT, svgOut)}`);

  // 2. PNG at each size (transparent background)
  for (const size of PNG_SIZES) {
    const pngOut = path.join(variantDir, `${variant}-${size}.png`);
    await sharp(Buffer.from(svgContent))
      .resize(size)
      .png({ compressionLevel: 9, adaptiveFiltering: true })
      .toFile(pngOut);
    console.log(`  PNG  → ${path.relative(ROOT, pngOut)} (${size}px)`);
  }

  console.log(`  ✓ ${variant}`);
}

async function exportFavicon() {
  // Use icon-dark for favicon
  const srcPath = path.join(LOGOS_DIR, 'icon-dark.svg');
  if (!fs.existsSync(srcPath)) return;

  const svgContent = fs.readFileSync(srcPath, 'utf8');
  const faviconDir = path.join(ROOT, 'dist', 'favicons');
  ensureDir(faviconDir);

  // favicon 16, 32, 64, 180 (apple touch), 192 (android)
  const faviconSizes = [
    { size: 16,  name: 'favicon-16.png' },
    { size: 32,  name: 'favicon-32.png' },
    { size: 64,  name: 'favicon-64.png' },
    { size: 180, name: 'apple-touch-icon.png' },
    { size: 192, name: 'android-icon-192.png' },
    { size: 512, name: 'pwa-icon-512.png' },
  ];

  for (const { size, name } of faviconSizes) {
    const out = path.join(faviconDir, name);
    await sharp(Buffer.from(svgContent))
      .resize(size, size, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .png()
      .toFile(out);
    console.log(`  ICO  → dist/favicons/${name}`);
  }
}

async function exportOpenGraph() {
  // OG image: 1200x630, dark background with centered wordmark
  const srcPath = path.join(ROOT, 'social', 'og-image.svg');
  if (!fs.existsSync(srcPath)) {
    // Generate a simple OG image from the wordmark
    const wordmarkPath = path.join(LOGOS_DIR, 'full-dark.svg');
    const svgContent = fs.readFileSync(wordmarkPath, 'utf8');
    const ogDir = path.join(ROOT, 'dist', 'social');
    ensureDir(ogDir);

    const ogOut = path.join(ogDir, 'og-image.png');
    await sharp(Buffer.from(svgContent))
      .resize(1200, 630, { fit: 'contain', background: { r: 10, g: 10, b: 10, alpha: 1 } })
      .flatten({ background: { r: 10, g: 10, b: 10 } })
      .png()
      .toFile(ogOut);
    console.log(`  OG   → dist/social/og-image.png`);

    // Twitter card (1200x600)
    const twitterOut = path.join(ogDir, 'twitter-card.png');
    await sharp(Buffer.from(svgContent))
      .resize(1200, 600, { fit: 'contain', background: { r: 10, g: 10, b: 10, alpha: 1 } })
      .flatten({ background: { r: 10, g: 10, b: 10 } })
      .png()
      .toFile(twitterOut);
    console.log(`  OG   → dist/social/twitter-card.png`);
    return;
  }

  const svgContent = fs.readFileSync(srcPath, 'utf8');
  const ogDir = path.join(ROOT, 'dist', 'social');
  ensureDir(ogDir);
  const ogOut = path.join(ogDir, 'og-image.png');
  await sharp(Buffer.from(svgContent)).resize(1200, 630).png().toFile(ogOut);
  console.log(`  OG   → dist/social/og-image.png`);
}

async function main() {
  console.log('\n🎨 Oli Brand — Logo Export Pipeline\n');
  ensureDir(DIST_DIR);

  for (const variant of VARIANTS) {
    await exportVariant(variant);
  }

  console.log('\n📌 Favicons...');
  await exportFavicon();

  console.log('\n🌐 Open Graph images...');
  await exportOpenGraph();

  console.log('\n✅ All logos exported to /dist/logos/\n');
}

main().catch(err => {
  console.error('Export failed:', err.message);
  process.exit(1);
});
