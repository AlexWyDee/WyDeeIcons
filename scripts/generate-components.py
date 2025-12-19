#!/usr/bin/env python3
"""
Generate React icon components from Figma SVG URLs.
Fetches SVG content and creates component files with embedded SVG.
"""

import urllib.request
import urllib.error
import json
import os
import re
from pathlib import Path

# Component data with correct URL mappings from Figma design context
COMPONENT_DATA = {
    'Soup': {
        'metadata': {'name': 'Soup'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/8a60b153ef4c274d57a2971b83808fc65c428041.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/14dc24a0ffcaabb4b5aab7dc695b72b9f9662f2e.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/b73368ee11c40b9e21a16b12a570587007db2a9b.svg',
            'Outline-Soft': 'http://localhost:3845/assets/0dd729454b8c0c7bcbd2e5c9d22c9020e8037e4d.svg',
            'Solid-Soft': 'http://localhost:3845/assets/3e06d73feadf79db163c55b5e03b659332743bda.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/bbe0f85c1fb69355df9277add64a2cb0239bfc0f.svg',
            'Outline-Round': 'http://localhost:3845/assets/9bcfe34fee7f76ab06cbecf92113d8dd20adbc7b.svg',
            'Solid-Round': 'http://localhost:3845/assets/cc3121a0da6f8faa6bd7072d60725f585331588a.svg',
            'Tonal-Round': 'http://localhost:3845/assets/8846a01365214d5368e14fbd058127425fcedcab.svg',
        }
    },
    'Burger': {
        'metadata': {'name': 'Burger'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/1219185624a5299a313502a746705d21e2c7fa86.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/e174ada2b47ee0987fc2bbba40ca579e71dfb63d.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/993449a9666d95e4bfabb6f4c08cd07618385f37.svg',
            'Outline-Soft': 'http://localhost:3845/assets/ee7e9d6ad4ba233e5d91e5a7235a26595e6639d3.svg',
            'Solid-Soft': 'http://localhost:3845/assets/0b7d6f037a315d99a26c6f7f513488d67423c7c2.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/22062fe19946c3b5d7c0216d0a0b9abca2bf2765.svg',
            'Outline-Round': 'http://localhost:3845/assets/717a22eabca9585244ae27da242b7792b4e942b4.svg',
            'Solid-Round': 'http://localhost:3845/assets/889cc4cccc872da404a20eba923881ccdfe56cce.svg',
            'Tonal-Round': 'http://localhost:3845/assets/445c029a66c42b9bc02605c6dd589e808b1cd9a5.svg',
        }
    },
    'Drumstick': {
        'metadata': {'name': 'Drumstick'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/11864e4fe911c4b87bf863941f822836f868f1cc.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/5a7505a830d7bb79e2ef98db28a4265f0902b3b7.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/e09450cb908e70033c458f10b7d8b22a716fb7a6.svg',
            'Outline-Soft': 'http://localhost:3845/assets/c5371c9c47659b97842eb05e9b3c2d4830371bf1.svg',
            'Solid-Soft': 'http://localhost:3845/assets/cb81131b8d570a9bef83ba257be1b593ad26f639.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/e71480cdcc2bcd57c1d62d652e50a6da2abd29bd.svg',
            'Outline-Round': 'http://localhost:3845/assets/4ffceb91fd2ecf3d632ac7411dd068b2e6891fcf.svg',
            'Solid-Round': 'http://localhost:3845/assets/b8f379e00ede24f95549e89d006f98f65d4ff2f2.svg',
            'Tonal-Round': 'http://localhost:3845/assets/d865e80c364c9a598ddbf198cc572950a68ea3a9.svg',
        }
    },
    'CarrotAlt': {
        'metadata': {'name': 'Carrot Alt'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/62854c3d3cfb7f6c49e6fbb6431ff96a9f5beff7.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/0d231e61586e48de329fb33f45adbee458608ea4.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/ed5bc1c96eb4a945ebac60cf422b90ea97c3b90b.svg',
            'Outline-Soft': 'http://localhost:3845/assets/0342b8fb36d11ce235ee9586cb02bbb9674c807e.svg',
            'Solid-Soft': 'http://localhost:3845/assets/7778c8ed4dffc9a66c1900c0e235c2db2e29136b.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/2008e8740117c868a2b6fa39ce99a9ebd3ac16de.svg',
            'Outline-Round': 'http://localhost:3845/assets/256140d3d374cf80e011564aadd17c45b72a4cf8.svg',
            'Solid-Round': 'http://localhost:3845/assets/f71818d6313e6a48953196b6de0337e34607acd1.svg',
            'Tonal-Round': 'http://localhost:3845/assets/5f4f16a83dd384c7bff04ac3b5104a1c0edacad4.svg',
        }
    },
    'Carrot': {
        'metadata': {'name': 'Carrot'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/c3d3b14983ba39ca54e353339ee5c9fbcf703bf1.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/b440613af1f384b510c9ddf9bfea5565e439e310.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/175c37ab0cff253269af522cbcce0c0024a2adf3.svg',
            'Outline-Soft': 'http://localhost:3845/assets/cb97eb5d64ad346ef9260e8dd3e5afc8151ec5d1.svg',
            'Solid-Soft': 'http://localhost:3845/assets/1f87ac5c402603976bff6fc9af7c35f05095c18d.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/0315307c56befed4ab04c3a70393d6a9759e4864.svg',
            'Outline-Round': 'http://localhost:3845/assets/12685e836417a969a14b34f9a68424fb5ca4006c.svg',
            'Solid-Round': 'http://localhost:3845/assets/4965b35da145c3ac9f82537eccde65d8570b5481.svg',
            'Tonal-Round': 'http://localhost:3845/assets/c73fccbd2ca2a222fcef339e43923310a4298e10.svg',
        }
    },
    'Mug': {
        'metadata': {'name': 'Mug'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/3fca5a38f6662d2d970920ba1adf1ea2de70bab2.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/ccf753c525467f5dd0532aa7b999a4a6d4091834.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/2129807d703d4a6fc118750ae222cfe4fc3a1c6d.svg',
            'Outline-Soft': 'http://localhost:3845/assets/7cc1e21bbc3e4f67af73cfa9d0f1a7064e32a779.svg',
            'Solid-Soft': 'http://localhost:3845/assets/e269f2708e5e565b914641e0d75ce945759ea4e7.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/346ee6de8648c3b230878aa015d5057d2724b0f7.svg',
            'Outline-Round': 'http://localhost:3845/assets/61f07ee618f3e09170f17370333685f187d614b0.svg',
            'Solid-Round': 'http://localhost:3845/assets/4d54f5f27f1a0c0bcd474706baca952ea83d3eb3.svg',
            'Tonal-Round': 'http://localhost:3845/assets/a19cb5554420ad949868f864a3abdebe0c1b9f57.svg',
        }
    },
    'HotDrink': {
        'metadata': {'name': 'Hot Drink'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/de89b9d0edb98eceb8962603327f06eba4f1e80b.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/105b367077180dd0dedc851c8e07755e3d25c0f8.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/188f1d4c3a07c06b2e2f559a04611cc449161554.svg',
            'Outline-Soft': 'http://localhost:3845/assets/b1bab7df90fa3a7ae54907392952f2af1cf87533.svg',
            'Solid-Soft': 'http://localhost:3845/assets/e2b3c662891c20ed9c8e882d6c00d435d9d6c0dc.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/aa3bba06cf0b055551bee434bfeb2b2d823f3ae5.svg',
            'Outline-Round': 'http://localhost:3845/assets/8cfa5280e0b244c368506c674f085f46dbda90e9.svg',
            'Solid-Round': 'http://localhost:3845/assets/59c2535b00f89499c29e3d037eae7904f8ef3bf3.svg',
            'Tonal-Round': 'http://localhost:3845/assets/a23266aa08a5bf3e188c2bb0b490bb00d9032802.svg',
        }
    },
    'GlassBottle': {
        'metadata': {'name': 'Glass Bottle'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/66767baf446a1b80f24d28ce54e5cabde0a7e11f.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/c521a76daef0e1f925de42b49121816ecb69606c.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/a1e9cba19f2af69190d45233a93cefac09375fbf.svg',
            'Outline-Soft': 'http://localhost:3845/assets/09e5f83417cb72268477f1c63e901906a213ff89.svg',
            'Solid-Soft': 'http://localhost:3845/assets/76763ac5e309b78c6890ec74b82a9ed877d8e28d.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/4eebeee4e600e40b065917835f3ad1c64a2217b3.svg',
            'Outline-Round': 'http://localhost:3845/assets/cc8eb17b12fd0738d32a3f200354fa1a23cec853.svg',
            'Solid-Round': 'http://localhost:3845/assets/6a1e17139ab7200f0f9db1685e8fdc98cc5f38cf.svg',
            'Tonal-Round': 'http://localhost:3845/assets/ecd94777a8c29abd5a4d7016aa00caa1eb1efdff.svg',
        }
    },
    'MilkBottle': {
        'metadata': {'name': 'Milk Bottle'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/f390527b797eb66c752bc7b5c96962f90d9fef6f.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/6a5b65c42138159a25329a8b0b6e417633cbaa69.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/9dd013d67b6a7e2d6d7bd41509d421f6401c2083.svg',
            'Outline-Soft': 'http://localhost:3845/assets/9159c9e8e6e10e910f0d36e74e40f0ba9f580921.svg',
            'Solid-Soft': 'http://localhost:3845/assets/0f44d482f226626e7edf1963e98dc2e78aeb426a.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/c33816c386cd299f1dd7bc059b4e7891bb9cd7f3.svg',
            'Outline-Round': 'http://localhost:3845/assets/63fec9ed7230986dcdec844b25d739c0e6cdf4a3.svg',
            'Solid-Round': 'http://localhost:3845/assets/98d6d77d1950e29013208c701a8c6823b6fe8b19.svg',
            'Tonal-Round': 'http://localhost:3845/assets/7e036371fbe273714d480b97df3826b1677fbfcd.svg',
        }
    },
    'Carton': {
        'metadata': {'name': 'Carton'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/ad8a137faf42d772a785ecaebb8a4858286373c7.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/b975ccb846b0b7bd32ce834473569c295169098e.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/b5e0ff938c72581f3a085b6dc118d2c3b5e6155e.svg',
            'Outline-Soft': 'http://localhost:3845/assets/e20dc2e72f848c9d917afb7328f5f082f92f8187.svg',
            'Solid-Soft': 'http://localhost:3845/assets/ef268b15e6f0719334775acaea58fc879a8d4d96.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/7fb2379aba9fd705a84726f32e3793eee6eeddfb.svg',
            'Outline-Round': 'http://localhost:3845/assets/483ad346c5cb8f806fc16ab5587f069e15735075.svg',
            'Solid-Round': 'http://localhost:3845/assets/6ee322fde7b0e633aca100131db97ea7f74148fc.svg',
            'Tonal-Round': 'http://localhost:3845/assets/4f8936f8396c0b3171136e77364f50f4a16f59ed.svg',
        }
    },
    'Grapes': {
        'metadata': {'name': 'Grapes'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/6b4b76effa5d437a2bb2687d2d62ff5c800d1ac9.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/cd498ce7ff645d174998f52ddae1024231b9c50e.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/3f316bc0362e7664d5f8a385b1779f8663813de2.svg',
            'Outline-Soft': 'http://localhost:3845/assets/f9ae78e1faa899e102546d2bc6a8677b19be10e5.svg',
            'Solid-Soft': 'http://localhost:3845/assets/1454eb8f35a92e5855039fb3e54a10dae2cdf494.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/a0d6b093fbbcddcc973ab8fed80dacb38ed86404.svg',
            'Outline-Round': 'http://localhost:3845/assets/cbc38706b4688ed7992cac1ec0068cd4e81f295b.svg',
            'Solid-Round': 'http://localhost:3845/assets/5219dd3d0f083dc7f63f4a4447a3de1a4da34f52.svg',
            'Tonal-Round': 'http://localhost:3845/assets/54e6fbe9b5c100aa087861071810b32a7d995353.svg',
        }
    },
}

def fetch_svg(url):
    """Fetch SVG content from URL."""
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"  ⚠ Warning: Could not fetch {url}: {e}")
        return None
    except Exception as e:
        print(f"  ⚠ Warning: Error fetching {url}: {e}")
        return None

def extract_svg_content(svg_string):
    """Extract inner SVG content, removing outer <svg> tags."""
    if not svg_string:
        return ''
    
    # Try to extract content between <svg> tags
    match = re.search(r'<svg[^>]*>(.*?)</svg>', svg_string, re.DOTALL)
    if match:
        return match.group(1).strip()
    return svg_string.strip()

def generate_component(component_name, component_info, svg_data):
    """Generate React component code."""
    component_config = component_info['metadata'].get('componentConfig', component_info['metadata']['name'])
    
    # Build SVG_VARIANTS object
    variants_code = []
    for variant_key in sorted(svg_data.keys()):
        svg_content = svg_data[variant_key]
        # Escape for JavaScript string
        escaped_content = json.dumps(svg_content)
        variants_code.append(f"  '{variant_key}': {escaped_content},")
    
    variants_str = '\n'.join(variants_code)
    
    template = f'''import React from 'react';
import {{ IconProps, Fill, Style }} from '../types';

export interface {component_name}Props extends IconProps {{
  'data-component-config'?: string;
}}

const SVG_VARIANTS: Record<string, string> = {{
{variants_str}
}};

export function {component_name}({{ 
  className = '', 
  fill = 'Outline' as Fill, 
  style = 'Sharp' as Style,
  size = 24,
  'data-component-config': dataComponentConfig,
  ...props 
}}: {component_name}Props) {{
  const variantKey = `${{fill}}-${{style}}`;
  const svgContent = SVG_VARIANTS[variantKey] || SVG_VARIANTS['Outline-Sharp'] || '';

  return (
    <svg
      width={{size}}
      height={{size}}
      viewBox="0 0 24 24"
      fill="currentColor"
      className={{className}}
      data-fill={{fill}}
      data-style={{style}}
      data-component-config={{dataComponentConfig || '{component_config}'}}
      {{...props}}
      dangerouslySetInnerHTML={{{{ __html: svgContent }}}}
    />
  );
}}
'''
    return template

def save_svg_to_repo(component_name, variant_key, svg_string, svgs_dir):
    """Save SVG file to repo for version control and GitHub as source of truth."""
    if not svg_string:
        return None
    
    # Ensure svgs_dir exists
    svgs_dir.mkdir(parents=True, exist_ok=True)
    component_dir = svgs_dir / component_name
    component_dir.mkdir(parents=True, exist_ok=True)
    
    # Sanitize variant key for filename (replace / with -)
    safe_variant_key = variant_key.replace('/', '-')
    svg_file = component_dir / f'{safe_variant_key}.svg'
    
    # Save the full SVG (with <svg> tags) to the repo
    svg_file.write_text(svg_string)
    return svg_file.relative_to(svgs_dir.parent)

def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    icons_dir = project_root / 'src' / 'icons'
    svgs_dir = project_root / 'svgs'  # Directory for storing SVG source files
    icons_dir.mkdir(parents=True, exist_ok=True)
    svgs_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating React icon components from Figma...")
    print("=" * 60)
    
    all_components = {}
    
    for component_name, component_info in COMPONENT_DATA.items():
        print(f"\nProcessing {component_name}...")
        svg_data = {}
        
        # Fetch all SVG variants
        for variant_key, url in component_info['variants'].items():
            print(f"  Fetching {variant_key}...", end=' ')
            svg_string = fetch_svg(url)
            if svg_string:
                svg_content = extract_svg_content(svg_string)
                svg_data[variant_key] = svg_content
                
                # Save SVG file to repo (GitHub as source of truth)
                saved_path = save_svg_to_repo(component_name, variant_key, svg_string, svgs_dir)
                if saved_path:
                    print(f"✓ (saved to {saved_path})")
                else:
                    print("✓")
            else:
                svg_data[variant_key] = ''
                print("✗ (using placeholder)")
        
        # Generate component file
        component_code = generate_component(component_name, component_info, svg_data)
        component_file = icons_dir / f'{component_name}.tsx'
        component_file.write_text(component_code)
        print(f"  ✓ Generated {component_name}.tsx")
        
        all_components[component_name] = component_info['metadata']
    
    # Generate index file
    print("\n" + "=" * 60)
    print("Generating index file...")
    
    exports = []
    for component_name in sorted(all_components.keys()):
        exports.append(f"export {{ {component_name}, type {component_name}Props }} from './icons/{component_name}';")
    
    index_content = '''// Auto-generated index file
// Export all icon components

''' + '\n'.join(exports) + '\n'
    
    index_file = project_root / 'src' / 'index.ts'
    index_file.write_text(index_content)
    print(f"✓ Generated index.ts")
    
    print("\n" + "=" * 60)
    print(f"✓ Successfully generated {len(all_components)} icon components!")
    print(f"✓ SVG source files saved to svgs/ directory (GitHub as source of truth)")
    print("\nNote: If some SVGs failed to fetch, make sure Figma is running")
    print("      and the localhost server is accessible.")
    print("      SVG files are now stored in the repo for future reference.")

if __name__ == '__main__':
    main()

