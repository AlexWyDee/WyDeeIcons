const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// Map of component names to their variant SVGs
// This will be populated from Figma API responses
const components = {
  'Soup': {
    variants: [
      { fill: 'Outline', style: 'Sharp', url: 'http://localhost:3845/assets/8a60b153ef4c274d57a2971b83808fc65c428041.svg' },
      { fill: 'Solid', style: 'Sharp', url: 'http://localhost:3845/assets/14dc24a0ffcaabb4b5aab7dc695b72b9f9662f2e.svg' },
      { fill: 'Tonal', style: 'Sharp', url: 'http://localhost:3845/assets/b73368ee11c40b9e21a16b12a570587007db2a9b.svg' },
      { fill: 'Outline', style: 'Soft', url: 'http://localhost:3845/assets/0dd729454b8c0c7bcbd2e5c9d22c9020e8037e4d.svg' },
      { fill: 'Solid', style: 'Soft', url: 'http://localhost:3845/assets/3e06d73feadf79db163c55b5e03b659332743bda.svg' },
      { fill: 'Tonal', style: 'Soft', url: 'http://localhost:3845/assets/bbe0f85c1fb69355df9277add64a2cb0239bfc0f.svg' },
      { fill: 'Outline', style: 'Round', url: 'http://localhost:3845/assets/9bcfe34fee7f76ab06cbecf92113d8dd20adbc7b.svg' },
      { fill: 'Solid', style: 'Round', url: 'http://localhost:3845/assets/cc3121a0da6f8faa6bd7072d60725f585331588a.svg' },
      { fill: 'Tonal', style: 'Round', url: 'http://localhost:3845/assets/8846a01365214d5368e14fbd058127425fcedcab.svg' }
    ]
  }
  // Add more components as needed
};

function fetchSVG(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    client.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode === 200) {
          resolve(data);
        } else {
          reject(new Error(`Failed to fetch: ${res.statusCode}`));
        }
      });
    }).on('error', reject);
  });
}

async function extractAllSVGs() {
  const svgsDir = path.join(__dirname, '../src/svgs');
  if (!fs.existsSync(svgsDir)) {
    fs.mkdirSync(svgsDir, { recursive: true });
  }

  for (const [componentName, component] of Object.entries(components)) {
    const componentDir = path.join(svgsDir, componentName);
    if (!fs.existsSync(componentDir)) {
      fs.mkdirSync(componentDir, { recursive: true });
    }

    for (const variant of component.variants) {
      try {
        const svgContent = await fetchSVG(variant.url);
        const filename = `${variant.fill}-${variant.style}.svg`;
        const filepath = path.join(componentDir, filename);
        fs.writeFileSync(filepath, svgContent);
        console.log(`Extracted: ${componentName}/${filename}`);
      } catch (error) {
        console.error(`Error extracting ${componentName} ${variant.fill} ${variant.style}:`, error.message);
      }
    }
  }
}

extractAllSVGs().catch(console.error);

