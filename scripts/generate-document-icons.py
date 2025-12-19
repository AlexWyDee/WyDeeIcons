#!/usr/bin/env python3
"""
Generate React icon components for document-related icons from Figma.
All components have 9 variants (Outline/Solid/Tonal × Sharp/Soft/Round).
"""

import urllib.request
import urllib.error
import json
import re
from pathlib import Path

def fetch_svg(url):
    """Fetch SVG content from URL."""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"  ⚠ Warning: Could not fetch {url}: {e}")
        return None
    except Exception as e:
        print(f"  ⚠ Warning: Error fetching {url}: {e}")
        return None

def extract_svg_content(svg_string):
    """Extract the inner content of an SVG (paths, groups, etc.)."""
    if not svg_string:
        return ''
    
    # Remove XML declaration and DOCTYPE if present
    svg_string = re.sub(r'<\?xml[^>]*\?>', '', svg_string)
    svg_string = re.sub(r'<!DOCTYPE[^>]*>', '', svg_string)
    
    # Extract content between <svg> tags
    svg_match = re.search(r'<svg[^>]*>(.*?)</svg>', svg_string, re.DOTALL)
    if svg_match:
        return svg_match.group(1).strip()
    
    return svg_string.strip()

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

def generate_component(component_name, component_info, svg_data):
    """Generate React component code."""
    component_config = component_info.get('metadata', {}).get('name', component_name)
    
    # Build SVG_VARIANTS map
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

# Component data - extracted from Figma design context
# All components have 9 variants (Outline/Solid/Tonal × Sharp/Soft/Round)
COMPONENT_DATA = {
    'CopyFolder': {
        'metadata': {'name': 'Copy Folder'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/2577216fbe222433c17cd08e956c2b9d05095b48.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/78b952a9aec36d3264d38422f8da9a4eabd8a5c1.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/2580c79fcb53d2217842cdd7017b90686a656b07.svg',
            'Outline-Soft': 'http://localhost:3845/assets/5251b0c6cffbe31620c3c30050946cd2e9173fc7.svg',
            'Solid-Soft': 'http://localhost:3845/assets/d813040f551cb5efb6a06eb383bb04123eb85086.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/440ee7acc538b736fd92b9171a5cdfcc7d6b76f8.svg',
            'Outline-Round': 'http://localhost:3845/assets/5e74281205d5fd6775628644932a16648373156c.svg',
            'Solid-Round': 'http://localhost:3845/assets/b29cbf20ec8e33460181fed46679f597bebe4b70.svg',
            'Tonal-Round': 'http://localhost:3845/assets/092e296edc9bda486fbb6dc0621434aa5b549acb.svg',
        }
    },
    'CopyFolderOff': {
        'metadata': {'name': 'Copy Folder Off'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/6663e858d6ff18ae05bc5cc291666fa400aa662f.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/5dc93f9b18b03c36e9ebf7902ce1cf873f9c0f06.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/d6367bcfd523f9935fdb05c81cee75f57c58332b.svg',
            'Outline-Soft': 'http://localhost:3845/assets/ed8ff1724826a1727cb89ac08e290f9d3bb65d62.svg',
            'Solid-Soft': 'http://localhost:3845/assets/fca5aaf3193100bab56828e71ffdf9a163ce91c3.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/e1708a34724a6da1a9063b7d749a9abb6e458cc4.svg',
            'Outline-Round': 'http://localhost:3845/assets/68c14c6e2b186c080eab65754809d781b6122fe0.svg',
            'Solid-Round': 'http://localhost:3845/assets/137c311010ee27b5ca59b8fcc36aeeee4af5dbf8.svg',
            'Tonal-Round': 'http://localhost:3845/assets/6c7a718b2a45f311d174046081c0f7a2755ab516.svg',
        }
    },
    'Bin': {
        'metadata': {'name': 'Bin'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/c1a2378d557e0a2d5bcbd879978f1504099049ce.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/86f71748f76493150a109510d8ccb82574c040f6.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/3390350e7da482728e2cf759993a25281bdaf0d8.svg',
            'Outline-Soft': 'http://localhost:3845/assets/9477400276fa292ff3b7ecd2eaf9e7dd6c3e4a9d.svg',
            'Solid-Soft': 'http://localhost:3845/assets/f8a39a1686175a4eb9f45406082caba6c9c4b02f.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/f818d36d7dd7a414fc6f1f81877672b9527fa38b.svg',
            'Outline-Round': 'http://localhost:3845/assets/80bddfdf80761ec8202dacbfe1805163ae3f6833.svg',
            'Solid-Round': 'http://localhost:3845/assets/fcb27994f87b20488fb1b0a62dc06ba7784bfe98.svg',
            'Tonal-Round': 'http://localhost:3845/assets/e7a77f5147dd22100a8506fcf9c8ecc4429b23e1.svg',
        }
    },
    'EditDocument': {
        'metadata': {'name': 'Edit Document'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/6e1bb2a7309a7a14abfd364ce4a2773b2910b466.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/a28db1cf67707447964a77637011957c3938a8e2.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/8b82434a872e3d55b0559bade1dbe2192d227f0a.svg',
            'Outline-Soft': 'http://localhost:3845/assets/690cf482bbcb95c56701bf1b50adb4a654fdbcf7.svg',
            'Solid-Soft': 'http://localhost:3845/assets/c22854a0b8c38801f3bb773b18e1d914f6482058.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/4c7bf49bb275ddedba41989fa6dfdb5299a74f8f.svg',
            'Outline-Round': 'http://localhost:3845/assets/1335768884bac81f5504aba06d073af11a1c23b4.svg',
            'Solid-Round': 'http://localhost:3845/assets/72fb770f49a9ba50c27bb40984c3979500b5c6df.svg',
            'Tonal-Round': 'http://localhost:3845/assets/45aea824cc1e2259da7dcdfef1f4e6f656582743.svg',
        }
    },
    'AddStickyNote': {
        'metadata': {'name': 'Add Sticky Note'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/83a4e8601db90fadb3835ca6b3f1e7dbcd7c2aba.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/042417f550b1dfd6007cd7135ca3cf9968235e92.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/bb02e99f236148eb6217952b97dc69517c9d766c.svg',
            'Outline-Soft': 'http://localhost:3845/assets/48cbce641c0def1417ce37801c74c6b226bd5fce.svg',
            'Solid-Soft': 'http://localhost:3845/assets/558c1cc356e371d20e353536e01bb108227deb5b.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/43ff51b232cd8d9cdca36924a17967b23a464cd7.svg',
            'Outline-Round': 'http://localhost:3845/assets/002ffaffbf0976cd9ac04d8d34b94f7ad86579ce.svg',
            'Solid-Round': 'http://localhost:3845/assets/e4cf88fe161572bd66f5fdbbfe510eca1cb61fee.svg',
            'Tonal-Round': 'http://localhost:3845/assets/33c4cb271929d8ae5b42ed0181415201c128a9d6.svg',
        }
    },
    'ClipboardText': {
        'metadata': {'name': 'Clipboard Text'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/a3a4d903f7815ba72cc5679f1ff35c45298a21e2.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/8fcd2f71405245ea67ae8ae357c3642eb75d03aa.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/3208e0a97bdadb1c022560b63c4040fb18f0531b.svg',
            'Outline-Soft': 'http://localhost:3845/assets/f20820d74dfd54b36041552c42a1e335e88b9eb7.svg',
            'Solid-Soft': 'http://localhost:3845/assets/4ec402d11960154823f70300e948e3ac8da71ff2.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/f627de7a4855226c2f96ac2b80b40caa82f17ced.svg',
            'Outline-Round': 'http://localhost:3845/assets/e9cf4ea94e54615f6b7e2123d259fd93d4dcded5.svg',
            'Solid-Round': 'http://localhost:3845/assets/ecde88be1cc8fa5fb681f98306a1d5d335743e5a.svg',
            'Tonal-Round': 'http://localhost:3845/assets/fead8e9ef3ec5ae365f5b5b5a810ef34444d7ac4.svg',
        }
    },
    'AddToClipboard': {
        'metadata': {'name': 'Add to Clipboard'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/06417d953de22efc1fc1c57e838716b0b71ad8e2.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/97c36f07486fbf60366ca70e93115fcebe674fe3.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/8744ba913acc7ab451090d78ee876a8f7b232cf6.svg',
            'Outline-Soft': 'http://localhost:3845/assets/ca367d1d3df9740fc91c1ca9d148ddb8046b8761.svg',
            'Solid-Soft': 'http://localhost:3845/assets/6d21fabac6be04f8c40270a8e8e74889e50dcbc5.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/80e72d5ec215c42de5f45a7c54ca645029f9127d.svg',
            'Outline-Round': 'http://localhost:3845/assets/1520e97570b27bc446be5d04eaf11ed5e663030c.svg',
            'Solid-Round': 'http://localhost:3845/assets/1d44713f7e8c79747ae08fb8d29fa5af4f6dcc55.svg',
            'Tonal-Round': 'http://localhost:3845/assets/0859347e3926f4ac7cbf9abcd47dda4979de8547.svg',
        }
    },
    'SearchClipboard': {
        'metadata': {'name': 'Search Clipboard'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/ba18fafb2c61cafce250b2bf75e6e379a6841edf.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/a7aa63f520a1a47d5a4cc9e2dfdd2d777038380a.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/2c09111cd8c6b0e161fa3543d7412d4e824de3a3.svg',
            'Outline-Soft': 'http://localhost:3845/assets/c388b5228619fd99f95c57256f2dfe79d8bd0961.svg',
            'Solid-Soft': 'http://localhost:3845/assets/316f72b33b2d64fa2e4545ba9b52c927728b810a.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/07c24b4db271018439db083824a25c0874807606.svg',
            'Outline-Round': 'http://localhost:3845/assets/60a4ad2dde3f1754958c3ef677b4bb4f9070b04a.svg',
            'Solid-Round': 'http://localhost:3845/assets/e647bd7ed7f7627c50aab246e242edb1d080132b.svg',
            'Tonal-Round': 'http://localhost:3845/assets/4eecec25962dc6504664a76e0157cb3726c71ef9.svg',
        }
    },
    'ClipboardTimer': {
        'metadata': {'name': 'Clipboard Timer'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/8da7029192df29f18d68d3fad7e2edd60695d8c8.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/34a4c47def94d5e61678dba0f960c2ffea3bf8f7.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/80523c76754d400a45da1c86a99cbbc5e59a8cc9.svg',
            'Outline-Soft': 'http://localhost:3845/assets/bdb9282d228029d05182fdf00a5885ec18d235f6.svg',
            'Solid-Soft': 'http://localhost:3845/assets/f0c93b4c05d39065c5fb6d90dd61f710cae4a6df.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/9183d4555997b6214fc2144148cdba070960eaab.svg',
            'Outline-Round': 'http://localhost:3845/assets/c98f9c0f6cb53034366272d1b7b92665115b7c12.svg',
            'Solid-Round': 'http://localhost:3845/assets/19d8d389813cf033556fa41898a8620bae7d2d9a.svg',
            'Tonal-Round': 'http://localhost:3845/assets/06669ced8d920462abaabe0fd29bde0a4fc96bc7.svg',
        }
    },
    'RemoveFromClipboard': {
        'metadata': {'name': 'Remove from Clipboard'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/e7fa818924b25db61ed5c5a938e5e1f0b4d176a7.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/3ccb3670074ada13c54763abc4a144c3205f227e.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/8744ba913acc7ab451090d78ee876a8f7b232cf6.svg',
            'Outline-Soft': 'http://localhost:3845/assets/7de41d18b6e840813a8fbddaee0d1f9c156746c7.svg',
            'Solid-Soft': 'http://localhost:3845/assets/f9e831ddb63caa31ebc7db46f67ad0b6fb760a4d.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/80e72d5ec215c42de5f45a7c54ca645029f9127d.svg',
            'Outline-Round': 'http://localhost:3845/assets/cd1dec5505f899a0998bd97d2bca5a0a22d95ac4.svg',
            'Solid-Round': 'http://localhost:3845/assets/4d7b8199429204305713acd8cda417235853059d.svg',
            'Tonal-Round': 'http://localhost:3845/assets/0859347e3926f4ac7cbf9abcd47dda4979de8547.svg',
        }
    },
    'PaperNote': {
        'metadata': {'name': 'Paper Note'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/57dc31547747731261409d397f3accc6fd1a72b7.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/f1564af9883844fa0cfa16795960472ac2960b0b.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/6baf127da43958d4e1d1b9ce654d6bc5e0587588.svg',
            'Outline-Soft': 'http://localhost:3845/assets/e03c86fbd02b1d266f2d550981a5d25f795ffd4f.svg',
            'Solid-Soft': 'http://localhost:3845/assets/300ab992d48c92fa97370430f76696d9459f8fd4.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/b52922f5777cff8a603b8016a006a561eb7ca8e4.svg',
            'Outline-Round': 'http://localhost:3845/assets/99d5cd9edd89a472a2ba8dc4f5f54cedfaff7521.svg',
            'Solid-Round': 'http://localhost:3845/assets/9f2fc4c7d085e4086f51e1b58837e7787f284cf6.svg',
            'Tonal-Round': 'http://localhost:3845/assets/72535578acd9b64625b33461c25524f4accd8dde.svg',
        }
    },
    'StickyNote': {
        'metadata': {'name': 'Sticky Note'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/bf6014410161133294fb824b3b760a48a899b642.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/c8ffb2d7e1dfa9d8cebe98fe8b91953a75c34691.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/ebf19d3f1726631ae76f300dfc1c64a41839ac68.svg',
            'Outline-Soft': 'http://localhost:3845/assets/021c1507b64bfbaa85030f6bc675e4c36eb9c3d8.svg',
            'Solid-Soft': 'http://localhost:3845/assets/992d8b73fa587b8321fdeb389589c8a2e0d9b5bd.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/4b74a54b566c80bf9b9f89b44f5e66227194be45.svg',
            'Outline-Round': 'http://localhost:3845/assets/c491622b73f917bec3ced93d1fce38270c33175c.svg',
            'Solid-Round': 'http://localhost:3845/assets/93345583d7a9d645b55d20ead5d65c01b7a8a12f.svg',
            'Tonal-Round': 'http://localhost:3845/assets/a8e0f6d0861eeb561e7663c77d89f1133e48c231.svg',
        }
    },
    'ImportDocument': {
        'metadata': {'name': 'Import Document'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/1b1745f275c94170847c259858e03b64ed1ba57e.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/dc0fca9ca439fad1ed2b3a4e4da653805598c272.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/fb2d4f16b5ef279e3d9398c82f42afb68499f7b0.svg',
            'Outline-Soft': 'http://localhost:3845/assets/6a7567e7bb555b17a4542419d6b27956a74f57e9.svg',
            'Solid-Soft': 'http://localhost:3845/assets/21f90cca4b1ab5c299e26cb9ba0e5e58053b6a3d.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/a99e328c760bb9328caf0a681f36aa917e15fe6a.svg',
            'Outline-Round': 'http://localhost:3845/assets/bbf287ff1ecc2742fdb1cbc20f370a4ba43d9320.svg',
            'Solid-Round': 'http://localhost:3845/assets/b74de67fda866a5774b475ec64341d1bc940b141.svg',
            'Tonal-Round': 'http://localhost:3845/assets/bb599d89a14facd5006919a11541192c71667da6.svg',
        }
    },
    'CompressDocument': {
        'metadata': {'name': 'Compress Document'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/bfbef72d1765af53ca1ab593feb015f80dc5fc93.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/8885e69461486b18d0766b54a2be88d57d1efa64.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/ed5d4390492f9c4d8f4dbd6b9556253ca303fed8.svg',
            'Outline-Soft': 'http://localhost:3845/assets/78bad0dffc009758a4ac2bc012c6e2747dbde38f.svg',
            'Solid-Soft': 'http://localhost:3845/assets/050e6cd961f6c233611cc21375bef0efe335e5e9.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/793617c4e9f669841c8f91c9aa8fd7f128ab0d66.svg',
            'Outline-Round': 'http://localhost:3845/assets/c5ad42b081b3871ac2f18b68da6d79530e4ddb78.svg',
            'Solid-Round': 'http://localhost:3845/assets/758b862826adc1feb476ff8b63ecd0fb4ce02d34.svg',
            'Tonal-Round': 'http://localhost:3845/assets/54e030f9f11edbb7e5f09c5b87d552891157b0a9.svg',
        }
    },
    'ExportDocument': {
        'metadata': {'name': 'Export Document'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/17473175016ef2eba960fce1a2d8e92ee4c5b496.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/f95d25d150f99d6691de1e4ae738dbfdea79bef5.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/9861a4ffbfdd7aa2ea1d2997c32634c87a52a816.svg',
            'Outline-Soft': 'http://localhost:3845/assets/1271ed6cadd3ffbf8845e0737a1d10f42ddff57a.svg',
            'Solid-Soft': 'http://localhost:3845/assets/3301c038f44bb92599dd945062c78a81e3067d81.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/78c1f21d2d498ec6f2a36bb727e23686b829d97b.svg',
            'Outline-Round': 'http://localhost:3845/assets/658dc0a9a622373fe13d3799b7b1544385342104.svg',
            'Solid-Round': 'http://localhost:3845/assets/29af002b564f14eda391c0a0b152521f3a482901.svg',
            'Tonal-Round': 'http://localhost:3845/assets/eb3d88602544debdff4df8bf6bac373d74493922.svg',
        }
    },
    'ScanDocument': {
        'metadata': {'name': 'Scan Document'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/6fd66d4a23b81a0d0cdf5fd62d8d7982cdd594ff.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/78a05f1c2b8ddac4f3d77c1094699cd39d77e0d3.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/4db8c0b3501971d74e95b6c8255bd9f20189e5b1.svg',
            'Outline-Soft': 'http://localhost:3845/assets/0dcc635bb640006f07bfd9b4e28ac365df56a8c4.svg',
            'Solid-Soft': 'http://localhost:3845/assets/4e2e6a630f3a8fc3d124e6a94155c15e03691a9c.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/19649cf43dcb25a750682d24456a1a3704d3e706.svg',
            'Outline-Round': 'http://localhost:3845/assets/2c520831f7f898d952250a1082535c4cf474493c.svg',
            'Solid-Round': 'http://localhost:3845/assets/d940f326a72a3f1ada59c0304512f53b349b3fc5.svg',
            'Tonal-Round': 'http://localhost:3845/assets/313d5cbf9b16df68f397f725baf6affa6e73ecb5.svg',
        }
    },
    'CopyDocument': {
        'metadata': {'name': 'Copy Document'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/7848168b49b2413e47977895f597ac945bab02ef.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/4603e3e9af287419de428f8767d856bfa08886f9.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/cb328d4fd365b032cf08be58583a4a2979ead0e7.svg',
            'Outline-Soft': 'http://localhost:3845/assets/4df1517ec8b37f946ed8dc1b5bddb141e76480c0.svg',
            'Solid-Soft': 'http://localhost:3845/assets/757f8a1da14a380bf3f435863cdf7f9e5c09a779.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/6feccca292240b4c4a4722df674cdd72a478b841.svg',
            'Outline-Round': 'http://localhost:3845/assets/320226ac04b8214f58cf1cb9c4dadd995548221a.svg',
            'Solid-Round': 'http://localhost:3845/assets/aa6eca947f1c9d794955610231e81c24291a2644.svg',
            'Tonal-Round': 'http://localhost:3845/assets/16126cda2207dfa7be692cabefbb7a0e1fc2fdda.svg',
        }
    },
    'DocumentNotes': {
        'metadata': {'name': 'Document Notes'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/601ddad6c9297f15ac6750494ae8605ceb1a849b.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/464f33c12cf9a117505a16230b4911fcc1af823a.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/dce3b3ba12cd86cf1034f411f7369d536cd40070.svg',
            'Outline-Soft': 'http://localhost:3845/assets/a09b6fa961ff60f09fa18d440312145e252eabf6.svg',
            'Solid-Soft': 'http://localhost:3845/assets/643ca916193f97b6e42a15605aec03d88867e849.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/e28d4e6027498775d1ab895db8fa2d22856c9f4b.svg',
            'Outline-Round': 'http://localhost:3845/assets/3a14b14fb3fdff0178f13d3f5d28ea21c2ba68e8.svg',
            'Solid-Round': 'http://localhost:3845/assets/5d94bee0fa2922d0ba398765176ce8c6b9db46fe.svg',
            'Tonal-Round': 'http://localhost:3845/assets/16da4c35343dd4893fe53ec59e94af97f7766f96.svg',
        }
    },
    'DocumentNotesOff': {
        'metadata': {'name': 'Document Notes Off'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/50ccc7b6287257ba13bd1a69237bc8c6071cf8a2.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/9433deeedd841ba1f288bfeb428700dbf650246b.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/df76e7389ef34b59927959daaffcae8e9a814474.svg',
            'Outline-Soft': 'http://localhost:3845/assets/ea881bde0bea67fd03a938312bdb5ac7c86b8294.svg',
            'Solid-Soft': 'http://localhost:3845/assets/65ebaba641f0c318e0146140d06dcac685455e1a.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/589794dc03ab2ecd73d01a46ef90041780c3d194.svg',
            'Outline-Round': 'http://localhost:3845/assets/b087b33f55f1af995557ecf77989d7c19ddd80b8.svg',
            'Solid-Round': 'http://localhost:3845/assets/b50edaca157e7e780e7e65e5beb968660d746b7d.svg',
            'Tonal-Round': 'http://localhost:3845/assets/f6c4288ad2876632f712cd493dde8a52d598be7d.svg',
        }
    },
    'Newspaper': {
        'metadata': {'name': 'Newspaper'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/6623e2da260054e71a22aaa46419555b4132b80d.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/a1c81a51aa367324a6bcfd44539ec1873ddb303b.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/a8e014c808023169b498e050b23758bfdc4f6deb.svg',
            'Outline-Soft': 'http://localhost:3845/assets/46af6cb205858ce284b43143c70d9e3bb87bbc8d.svg',
            'Solid-Soft': 'http://localhost:3845/assets/fe566bcb8e4cecebc35b7f035421c789b56b6327.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/1953e0c6b8d2b30332e299e6ddf6bba8d3594829.svg',
            'Outline-Round': 'http://localhost:3845/assets/348d4bcc2e5cbc0649ffeccdd2290cfad06351d2.svg',
            'Solid-Round': 'http://localhost:3845/assets/4bd072d5f465e092622b050f2ac59512e5bdbf24.svg',
            'Tonal-Round': 'http://localhost:3845/assets/92c53123c98f58b9fe5c37c697113c05986fac1b.svg',
        }
    },
    'NewspaperOff': {
        'metadata': {'name': 'Newspaper Off'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/e4bdb157344e1ade54bf656f87f437cad0c98aeb.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/e7c997b8a93955ad392cbb8e72505abdc8764f6b.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/37f80818fe3dfa6d02988dc06c0b6055a65acfee.svg',
            'Outline-Soft': 'http://localhost:3845/assets/cde4eaddabda18f73a9be78fef3e9ba40dab3d2f.svg',
            'Solid-Soft': 'http://localhost:3845/assets/08b0447b586bcf11b83ce9a4f994a0efc593ad9a.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/cb1ddb22f9f103e20252fe05088767356e6f3270.svg',
            'Outline-Round': 'http://localhost:3845/assets/b44502b3e689bccced0c11b33357d806e368ac22.svg',
            'Solid-Round': 'http://localhost:3845/assets/e4bdb157344e1ade54bf656f87f437cad0c98aeb.svg',
            'Tonal-Round': 'http://localhost:3845/assets/e4bdb157344e1ade54bf656f87f437cad0c98aeb.svg',
        }
    },
    'AddDocument': {
        'metadata': {'name': 'Add Document'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/71ca3ac957df8b1e58d41f44aa584d37acfb0f72.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/23e930464cf9d609c3578d6aae00779ee138d3c4.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/b824513ebda8ab426830f8b596a7137343a639a0.svg',
            'Outline-Soft': 'http://localhost:3845/assets/62b1e51a563501ed8a62d59fe0edf02de41cc938.svg',
            'Solid-Soft': 'http://localhost:3845/assets/33a3a6aaa136f80a701b3f567177fb82030e71f1.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/e4d928ba4f156799a59e6be0297418d4e4d5fc23.svg',
            'Outline-Round': 'http://localhost:3845/assets/292595d8aa1ba8686c6e3e59495ce28fda961d0a.svg',
            'Solid-Round': 'http://localhost:3845/assets/4e62d799e414d0a6dd8a76bdd40cd7bbb740f5cd.svg',
            'Tonal-Round': 'http://localhost:3845/assets/c3082baaa6eb852d178f813b9fec1e5b9d72a062.svg',
        }
    },
    'DocumentAlert': {
        'metadata': {'name': 'Document Alert'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/220c46ce4f793c5f3c42ac508134bed27469466e.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/4f2ec553e2f263043f8a5771ee06a74d86e4a341.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/4d97f44ac532b62a928e97023afece124e913a44.svg',
            'Outline-Soft': 'http://localhost:3845/assets/8d911d30eb2e8eb949e5c50c924e8a2c12bf415f.svg',
            'Solid-Soft': 'http://localhost:3845/assets/d68985bb89ef3d63fec447391e5b1a4548942b52.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/e4d928ba4f156799a59e6be0297418d4e4d5fc23.svg',
            'Outline-Round': 'http://localhost:3845/assets/c610a68067626b0f2e0fc315415e1e6a769bd45d.svg',
            'Solid-Round': 'http://localhost:3845/assets/b7ce9ea6b07d247df7f3ad0326f2305e9c009109.svg',
            'Tonal-Round': 'http://localhost:3845/assets/8263df760cdc3f777ae3ae7a37e05c31d8a85430.svg',
        }
    },
    'DocumentOptions': {
        'metadata': {'name': 'Document Options'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/184e0c68a1ac6c7c9bc8a1630c22ceeb2d81a16f.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/4912792c7eb46ebfc5f27ec571233932eb252390.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/b824513ebda8ab426830f8b596a7137343a639a0.svg',
            'Outline-Soft': 'http://localhost:3845/assets/6342027a94a2da35389bde9732581e31c5a9afc2.svg',
            'Solid-Soft': 'http://localhost:3845/assets/4df9c0a64a3d25f232b94b9adf62f0a976058958.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/91352bfe6ec294fb205fc40ab07660b391d8d6e2.svg',
            'Outline-Round': 'http://localhost:3845/assets/241402e840344b78b80241c0926548abe9ec5d97.svg',
            'Solid-Round': 'http://localhost:3845/assets/54323c6e593039b68c448fcf429d60127c2bd9ec.svg',
            'Tonal-Round': 'http://localhost:3845/assets/e1d9fc157d424acfa070ac6273553590969f9217.svg',
        }
    },
    'DownloadDocument': {
        'metadata': {'name': 'Download Document'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/f6a67a1b05a781a65f8ca4435851d480fa227bb8.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/f84ea639cf9d8593e8984637ed20e73422b1c934.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/73f5a856549be53d589cbac0a542c0093c9d613e.svg',
            'Outline-Soft': 'http://localhost:3845/assets/e5f97d7a62d8d572622f56a0fea1f1a1fd1d04a5.svg',
            'Solid-Soft': 'http://localhost:3845/assets/0a723a39c66a8141caf19704f4266423fac97547.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/b5d0d3aee1c3a89d84a7a2f4d69ead256da294e7.svg',
            'Outline-Round': 'http://localhost:3845/assets/92268cb0be588348b0b031da634aff02f7a46e01.svg',
            'Solid-Round': 'http://localhost:3845/assets/ca54b46e7123d9af7eb69bbd643f0d58bfb3007f.svg',
            'Tonal-Round': 'http://localhost:3845/assets/63d165428a6864e5f9eec2b1c61aeef5abe8957f.svg',
        }
    },
    'SearchDocument': {
        'metadata': {'name': 'Search Document'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/f37df74c9a557ce0a4dcb19d2b5583b479963caa.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/f5c560d751d7505230616c6abf9afa786288edce.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/9abfe0c8fb3e60eff73e7e589da03392bbc71172.svg',
            'Outline-Soft': 'http://localhost:3845/assets/768521e8bf362098e292785755c5f094491997a3.svg',
            'Solid-Soft': 'http://localhost:3845/assets/a1d3eded082d2562f07e1e671aff895085fa03a9.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/10fae2959db8fe712eaff1b2d4d897cc0283dfdb.svg',
            'Outline-Round': 'http://localhost:3845/assets/1ac92016effc48d44010e437c7ebbf2b30370b73.svg',
            'Solid-Round': 'http://localhost:3845/assets/b61c4ed81de56a3b7dfad7a2237b6b0b929fc9f2.svg',
            'Tonal-Round': 'http://localhost:3845/assets/811b041a9eec74573dd4ccbad4862dae858155a3.svg',
        }
    },
    'StickyNoteOff': {
        'metadata': {'name': 'Sticky Note Off'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/d998b2d5f78fa229cf68166e5d06e257e454e73c.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/9fbc8b2833d2b50e50c85914109e5b96bce14b27.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/df76e7389ef34b59927959daaffcae8e9a814474.svg',
            'Outline-Soft': 'http://localhost:3845/assets/976eb21bef43ebb29f4d39e0222bad274f93f6c8.svg',
            'Solid-Soft': 'http://localhost:3845/assets/95cc4febd62db4e49ee0e944639b23d7d1507cdd.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/78e8d90d9d162a0f2bb26c77ba5849a116d418b2.svg',
            'Outline-Round': 'http://localhost:3845/assets/bca6afdb2d5081f5a09b0a1b872d888778201240.svg',
            'Solid-Round': 'http://localhost:3845/assets/bf60b54b7702e2a2399bad08837c72c188fd05bd.svg',
            'Tonal-Round': 'http://localhost:3845/assets/7bfd12ca94cc862f837d56d7c6f6b5ed7475dec3.svg',
        }
    },
    'Folder': {
        'metadata': {'name': 'Folder'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/180873e7351ead841d95cb8c1401ba7c49ffbc9b.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/64969003dcb4153c8a9eb34da12819277c0f342e.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/c66d6759bb97541b708b999e0f21f76dfc54de7d.svg',
            'Outline-Soft': 'http://localhost:3845/assets/f3d88322a9fdde391c38c2fb526cb54851feed71.svg',
            'Solid-Soft': 'http://localhost:3845/assets/0d766d9c3080036d1e9ad866c00be40d26bacad5.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/21785f0fd4657e1f6bb66aa706ed653862b371fd.svg',
            'Outline-Round': 'http://localhost:3845/assets/dd63afbdc3b1c0b54eca2c4045183d6df71834a3.svg',
            'Solid-Round': 'http://localhost:3845/assets/00a6498a7dc0018f150ac39b81acff75e400207f.svg',
            'Tonal-Round': 'http://localhost:3845/assets/6c12c815d474ca3dd99bc93689adca4c124181ba.svg',
        }
    },
    'FolderOff': {
        'metadata': {'name': 'Folder Off'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/c1ae6bddc1ebb34e19c3ff4e7e5b8c6c598945cc.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/62097d07484a083d32ad6ea3531b2654ebd9ba5d.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/24dcea0c7b54a617cd77d10978ed1f8aeb7f26b8.svg',
            'Outline-Soft': 'http://localhost:3845/assets/0fc5cff490eb59e2d99f6d40ec90e191e875d2fd.svg',
            'Solid-Soft': 'http://localhost:3845/assets/a532b6d49d96971255a9a98ef01883d7e7f87e98.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/bb4fac27f46109b006485a46353a1d494cdb8d71.svg',
            'Outline-Round': 'http://localhost:3845/assets/4accbf53b27502b73a7a3dd31534b05305e18941.svg',
            'Solid-Round': 'http://localhost:3845/assets/fe90518bd6a6a9311fdda1957ecffe9c4d678796.svg',
            'Tonal-Round': 'http://localhost:3845/assets/c1ae6bddc1ebb34e19c3ff4e7e5b8c6c598945cc.svg',
        }
    },
    'AddFolder': {
        'metadata': {'name': 'Add Folder'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/74b547bb9a285d28e38f64f4393ddf7864f7ce72.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/503bcfe8d71245324cfe5109b9c7d35e5e7017e5.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/a3dd420eaa891d424cc7f0059a2817a06f63f2fd.svg',
            'Outline-Soft': 'http://localhost:3845/assets/7ae547575edacfde15b16eeaa7a8de0a5a2eda7b.svg',
            'Solid-Soft': 'http://localhost:3845/assets/546075a54e16d1c457c28661e13162ebb86e8e5f.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/6936d50d5435b203c16a3392080ef4844819920e.svg',
            'Outline-Round': 'http://localhost:3845/assets/cc489ac1b4acd90185749eb97b4faf52ccebefca.svg',
            'Solid-Round': 'http://localhost:3845/assets/103d441c6597e7ad06589a954d0d236634713746.svg',
            'Tonal-Round': 'http://localhost:3845/assets/ccd154ada2c83ad478b667f4eb982bdd88396095.svg',
        }
    },
    'MinimizeFolder': {
        'metadata': {'name': 'Minimize Folder'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/e8f24993ec966e66c922845168aaf0601bebfac9.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/63ae29a323cd5c6a5ba1ccb102e282727f895dfe.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/c9e4efb53b12ec63331568a3dce8a714d82cbb54.svg',
            'Outline-Soft': 'http://localhost:3845/assets/b1dca69aabea7214804a3a49afcef35a9bd57956.svg',
            'Solid-Soft': 'http://localhost:3845/assets/8174d2836e56dd35d89ff4f35f8f5eb730c39f2.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/060d42744b1f915965f4d0c922b2b6a83f0959af.svg',
            'Outline-Round': 'http://localhost:3845/assets/5df6e9430360521a5eecc70100571b400b674888.svg',
            'Solid-Round': 'http://localhost:3845/assets/5b5d47316b67e6a798db0df7f7f41b8db202eaf1.svg',
            'Tonal-Round': 'http://localhost:3845/assets/b38f635c9614df94962f665fca0cca45693796dd.svg',
        }
    },
    'CopyDocumentOff': {
        'metadata': {'name': 'Copy Document Off'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/c7be7bab473ac8505dbe371484b1e4f70f61161b.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/e3a2591dff65710e5494f89a126d1268e734f152.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/a4d70a30937ab68345383538e906a60f5ea99322.svg',
            'Outline-Soft': 'http://localhost:3845/assets/e842a0d388a032f067272fb8c917fc090d04dcdc.svg',
            'Solid-Soft': 'http://localhost:3845/assets/6cd09e58317b17813d5a637906a7a28f2e8eb1dc.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/21789d431082ca315a82191f682318b4874cb18d.svg',
            'Outline-Round': 'http://localhost:3845/assets/e842a0d388a032f067272fb8c917fc090d04dcdc.svg',
            'Solid-Round': 'http://localhost:3845/assets/6cd09e58317b17813d5a637906a7a28f2e8eb1dc.svg',
            'Tonal-Round': 'http://localhost:3845/assets/21789d431082ca315a82191f682318b4874cb18d.svg',
        }
    },
    'Clipboard': {
        'metadata': {'name': 'Clipboard'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/be7e899dd94fde299bbb4dabbb494dcb276487ec.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/a3cc3c62da15a57cb9c91d6ec081f47504050879.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/8744ba913acc7ab451090d78ee876a8f7b232cf6.svg',
            'Outline-Soft': 'http://localhost:3845/assets/5404e6d721d1b694599b877c7e294aa0027ae934.svg',
            'Solid-Soft': 'http://localhost:3845/assets/c2b3de6ddb75dc59ea468a917799597624e34bce.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/f627de7a4855226c2f96ac2b80b40caa82f17ced.svg',
            'Outline-Round': 'http://localhost:3845/assets/e2009bfe9ebe9b7e2f5d28d816cbd175632e20da.svg',
            'Solid-Round': 'http://localhost:3845/assets/4808c4c893c93ee803c0f6ab46fdc76aba8a8e67.svg',
            'Tonal-Round': 'http://localhost:3845/assets/fead8e9ef3ec5ae365f5b5b5a810ef34444d7ac4.svg',
        }
    },
    'ClipboardOff': {
        'metadata': {'name': 'Clipboard Off'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/70dc41d9be8c015ae8fd0d683da96131633d5aaf.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/008d345644fa549c4e99d517dcdc194bd670c080.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/4db09cb808d06211ad373ce4cc00351eab36efd1.svg',
            'Outline-Soft': 'http://localhost:3845/assets/550bad82e53211bcc62dcf35a0eb9e8d6acd3bd3.svg',
            'Solid-Soft': 'http://localhost:3845/assets/6e0368ad6280f50ce6668534df85c05713d27775.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/e899995a37de4749781e5fbffec16325ba4894be.svg',
            'Outline-Round': 'http://localhost:3845/assets/b4405d8fa7946f03b55c9080240a863806a08daa.svg',
            'Solid-Round': 'http://localhost:3845/assets/c336221e7c74b5ce18ac4833ba6166e298bc553b.svg',
            'Tonal-Round': 'http://localhost:3845/assets/3c148455bf693ecff42e6f928891517868aee1fc.svg',
        }
    },
    'ClipboardChart': {
        'metadata': {'name': 'Clipboard Chart'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/b78ca5e601fa5c36f014b5886da2a64021a817d9.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/640bac4af115d9f5b2125506723cc380e6d7ce96.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/f60024db1dc391a296e7466f3cc24a4367507748.svg',
            'Outline-Soft': 'http://localhost:3845/assets/b8d11650d0041a58e208db224aac19863fc76f0d.svg',
            'Solid-Soft': 'http://localhost:3845/assets/b5cd1396f8249a5fead274cddeacf65e4b8e2d10.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/936e497a35a95f5964241c28066c97183ec50bcc.svg',
            'Outline-Round': 'http://localhost:3845/assets/c84aac815426fd95499d6562f22a9e1f0b30d4ea.svg',
            'Solid-Round': 'http://localhost:3845/assets/aa661d193d54dc588bc0840654136179aee4b696.svg',
            'Tonal-Round': 'http://localhost:3845/assets/41cba7c7d5ed9a8750bd951b6daf55e82428f072.svg',
        }
    },
    'ConfirmClipboard': {
        'metadata': {'name': 'Confirm Clipboard'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/4fb2671d3f9a05d6cd6970bbb36235969e398933.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/01914ab1d00d9ab93f01d5513baa16551014356b.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/f60024db1dc391a296e7466f3cc24a4367507748.svg',
            'Outline-Soft': 'http://localhost:3845/assets/b8e574924fb02b977f5a5b15d6cb549eff343f4f.svg',
            'Solid-Soft': 'http://localhost:3845/assets/27c2a049fbf5c9ec4fe51d5bacc04f726f26a227.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/cdb01a37d87d970018eff076aa2c45e19d1a41a7.svg',
            'Outline-Round': 'http://localhost:3845/assets/a0463bdcecec8c52e477b79c0d20cc9cdec0fdca.svg',
            'Solid-Round': 'http://localhost:3845/assets/ecb6b898bbcfe822931a5204615c712988a31b7a.svg',
            'Tonal-Round': 'http://localhost:3845/assets/ce41f1b0f71a080eeff52020662c5f7205845e4e.svg',
        }
    },
    'RemoveFolder': {
        'metadata': {'name': 'Remove Folder'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/6c8bcdf526c1c78fc33677eab6a0d45ff049ec1b.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/6c0391290f261d89a33a3c81b70ade74cba3b010.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/3c7fe3b355a2881061202706b9274f857e7b5f73.svg',
            'Outline-Soft': 'http://localhost:3845/assets/ed2dafab02624c9f1425fe319e9d31362d35bd60.svg',
            'Solid-Soft': 'http://localhost:3845/assets/9c73e010308bd38d78bede442ef6c5ad87309a63.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/5b93b7eb9532d4e7f67731b98dd13c997053edb9.svg',
            'Outline-Round': 'http://localhost:3845/assets/e30664c41113c2ce4ee1416aff45d2cca57eac23.svg',
            'Solid-Round': 'http://localhost:3845/assets/b24d36c079dd14570a193c03b696d247088bee1c.svg',
            'Tonal-Round': 'http://localhost:3845/assets/3452de61448811f8dcab3f1a2f564c61380ce25e.svg',
        }
    },
    'Page': {
        'metadata': {'name': 'Page'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/3aba39cd09259092af9d33f1163ef5f884adec8c.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/15f75857d5e6ad8194a11535b1684649bbc8f30e.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/b824513ebda8ab426830f8b596a7137343a639a0.svg',
            'Outline-Soft': 'http://localhost:3845/assets/1f792ff5cf7781cc3a607d60f5c7800cb2f46c6e.svg',
            'Solid-Soft': 'http://localhost:3845/assets/e8bdac7e2feebd824f6f533ff0f8d146ac1a701c.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/3698536fa9a59978707524b68800b355468be999.svg',
            'Outline-Round': 'http://localhost:3845/assets/b25a6e63288a437cdea915c44ac3343a6ab51c10.svg',
            'Solid-Round': 'http://localhost:3845/assets/3e2302d98dbeb5e248ed1abcc871316bbfacbeac.svg',
            'Tonal-Round': 'http://localhost:3845/assets/ef85b41fb0d26245c04dc71fb46125c41f2e2a77.svg',
        }
    },
    'PageOff': {
        'metadata': {'name': 'Page Off'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/a88c092b63f56403ef6d470e0a523dcc99c718da.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/8993d866c4eba4cb5819474f42287f84cde176df.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/df76e7389ef34b59927959daaffcae8e9a814474.svg',
            'Outline-Soft': 'http://localhost:3845/assets/8c87c69e1489575b0e0dcfefffeb7887d1286317.svg',
            'Solid-Soft': 'http://localhost:3845/assets/d12c9d4487672d7fb533d29c04838fe1ebdf396b.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/c2683d9dacce2f552ae9a9cd4350eedb862fd8fe.svg',
            'Outline-Round': 'http://localhost:3845/assets/64c65eda2013016d4f8cb4363bf5d692ca0e1125.svg',
            'Solid-Round': 'http://localhost:3845/assets/888a63aac6bdf8611e2ef293f15321df8df20756.svg',
            'Tonal-Round': 'http://localhost:3845/assets/48db2d99286ec90a00b27541d18cb08996a3f3c2.svg',
        }
    },
    'Document': {
        'metadata': {'name': 'Document'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/4f3b79fc212ca072f5f2816c01e166441eadb5c4.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/a36b737c368d0d9c1944bcf915dca1eb83c76831.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/73f5a856549be53d589cbac0a542c0093c9d613e.svg',
            'Outline-Soft': 'http://localhost:3845/assets/8236a0feca47f6cd3c5670c05d3188532026bcb9.svg',
            'Solid-Soft': 'http://localhost:3845/assets/8c1de8890182f039663f840ae6740ed47b50a944.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/86a9b041a6237a06ba5808759299bb9583b3a80a.svg',
            'Outline-Round': 'http://localhost:3845/assets/6811e35555809b1018796a31717277d506968c15.svg',
            'Solid-Round': 'http://localhost:3845/assets/fcb66d9248ac981d836845fdcccb0ab66fad63d6.svg',
            'Tonal-Round': 'http://localhost:3845/assets/e64faa0b9ca16a97d97d6ee3ac360be4a6b40dc2.svg',
        }
    },
    'DocumentChart': {
        'metadata': {'name': 'Document Chart'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/3f0820720bd3f74e7c9f5a94e44b0fc0b4e6e0ad.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/2b00d3580e987c3504ee0babd591cc1aea2aa0e2.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/cf0aad4ae1898140b6bcd1c6f1404a9623b9b0a5.svg',
            'Outline-Soft': 'http://localhost:3845/assets/a5d53690395ce543a47e45e8cdd569a0bf8627e7.svg',
            'Solid-Soft': 'http://localhost:3845/assets/23f95719ee3e784bfd8491cfb09c56cdaa4f1e7e.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/902e9605a956652622577e47b2918d157cc66be9.svg',
            'Outline-Round': 'http://localhost:3845/assets/5ed9d18abd3d893aead6771bc13f32fa727890d6.svg',
            'Solid-Round': 'http://localhost:3845/assets/ffbbf45903e05c70a03f265d775141b210912e75.svg',
            'Tonal-Round': 'http://localhost:3845/assets/56cb347442e0204873a441e585e74d81199fbdfb.svg',
        }
    },
    'ConfirmDocument': {
        'metadata': {'name': 'Confirm Document'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/8d79fc7288fb5a5bfdc743ed43fc472f7c548983.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/7ce7c9715e9b0b0cda022d858901aae62f2d60d1.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/b824513ebda8ab426830f8b596a7137343a639a0.svg',
            'Outline-Soft': 'http://localhost:3845/assets/8b7ff9d557fdca6c407ad04a9d336d135057436e.svg',
            'Solid-Soft': 'http://localhost:3845/assets/38e460e9fe3901615677abb259efb60316ea94ed.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/6bdfe920052aab969dea0c4aa11522ba36de9cb5.svg',
            'Outline-Round': 'http://localhost:3845/assets/5ffe835a47e38d922d708033c01e7767ab932b08.svg',
            'Solid-Round': 'http://localhost:3845/assets/b16e6284866214143b2724f680fe4cffdf88040c.svg',
            'Tonal-Round': 'http://localhost:3845/assets/d6a9f5b14207b5d37df819ebd52b9b34b1541c13.svg',
        }
    },
    'Book': {
        'metadata': {'name': 'Book'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/85c87022f88962d21ac011c57e4eeadb4e222904.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/73fdd632f80144fab40faa4f021b5b7d64d892c3.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/5143ac52cb78e33e2489a5bcdd73f77473c6141e.svg',
            'Outline-Soft': 'http://localhost:3845/assets/a5bf456df3481c7f5d4bf6205d6461af9c1e91e0.svg',
            'Solid-Soft': 'http://localhost:3845/assets/0bcd6ee7ed461ffd73ad128d8ab4099dd8e6eb1e.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/660cd75b8f5424b4f488f7d6ca693cf2ca787194.svg',
            'Outline-Round': 'http://localhost:3845/assets/e5c26de3a9fa52ed13a42f5192f8fee0f3c06f6f.svg',
            'Solid-Round': 'http://localhost:3845/assets/1dd9af894404917a3426422c4f6661cdaf8fcda5.svg',
            'Tonal-Round': 'http://localhost:3845/assets/1df0849bc3bde42b10f2dbfc0ffb75b537277261.svg',
        }
    },
    'BookOpen': {
        'metadata': {'name': 'Book Open'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/729212f1ae78992c08a8cf457bb66cc15648fde2.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/39423115c8ba086fc018b6af09e32d55e4efa1d2.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/456ef225c07b72406265c3abf8f54c61738f6ca1.svg',
            'Outline-Soft': 'http://localhost:3845/assets/7dc8ac62bb3caee755f5c52ccf0babf50ddb976c.svg',
            'Solid-Soft': 'http://localhost:3845/assets/9fb157daf348452e03856043d6c4ef9c7932b075.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/b6f6c12223e0e091d35be86c69ab6cbebcf0b97e.svg',
            'Outline-Round': 'http://localhost:3845/assets/d99af07e50afa48bedfdb36d44dabadd1255d109.svg',
            'Solid-Round': 'http://localhost:3845/assets/f6388c918c989acaf55a5426ad30b0ce8a1bf190.svg',
            'Tonal-Round': 'http://localhost:3845/assets/99bfd0d5eb3281cd4f3213f3d3afbab4797a8309.svg',
        }
    },
    'Notebook': {
        'metadata': {'name': 'Notebook'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/8059dae821824e753af0dddf7d90b5cd11e34cdc.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/469988373c6488ed716548dde64cbb2ea0baf429.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/f912f8a59f73f5177b85fcb583ceb5ef93d15f10.svg',
            'Outline-Soft': 'http://localhost:3845/assets/eb4824bad517c5bffb340099c41cb3f410e0051c.svg',
            'Solid-Soft': 'http://localhost:3845/assets/fea3ebcdee15a89e6f56d4d3b2a58c0718415695.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/7167b35dd2d06bdebec8fb1c6df6f905b88602df.svg',
            'Outline-Round': 'http://localhost:3845/assets/08b339c3b7680e93a692d610c7d19c3da97786b4.svg',
            'Solid-Round': 'http://localhost:3845/assets/c1880f0fd5af44489fba6d330dc1923d78e17912.svg',
            'Tonal-Round': 'http://localhost:3845/assets/f7535f9bd542b27882ca7fec375937fd77a29263.svg',
        }
    },
    'NotebookOff': {
        'metadata': {'name': 'Notebook Off'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/d5ebc1e6cf770faa34e9363602e568e3b92d4aad.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/3e8b70fe9268fabe3d8112f9a0e525d3d81942c7.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/1c564549d86545d7d660ea001e526592f885ce83.svg',
            'Outline-Soft': 'http://localhost:3845/assets/c2a07318a76dea5d33ed40fb9b0813703430c373.svg',
            'Solid-Soft': 'http://localhost:3845/assets/1277a7fdb02eefa565b3d74777a940beb7e4d353.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/bbd64625060fa2d4b36051c3f11d9525d3593795.svg',
            'Outline-Round': 'http://localhost:3845/assets/b514e36a1a4414fd8a130c350b790e3b531b0b90.svg',
            'Solid-Round': 'http://localhost:3845/assets/be0ac71b57ef8c4594741c26fae3990a4b3e8b17.svg',
            'Tonal-Round': 'http://localhost:3845/assets/bbd64625060fa2d4b36051c3f11d9525d3593795.svg',
        }
    },
    # Component names: AddStickyNote, ClipboardText, AddToClipboard, SearchClipboard, ClipboardTimer,
    # RemoveFromClipboard, PaperNote, StickyNote, ImportDocument, CompressDocument, ExportDocument,
    # ScanDocument, CopyDocument, DocumentNotes, DocumentNotesOff, Newspaper, NewspaperOff,
    # AddDocument, DocumentAlert, DocumentOptions, DownloadDocument, SearchDocument, StickyNoteOff,
    # Folder, FolderOff, AddFolder, MinimizeFolder, CopyDocumentOff, Clipboard, ClipboardOff,
    # ClipboardChart, ConfirmClipboard, RemoveFolder, Page, PageOff, Document, DocumentChart,
    # ConfirmDocument, Book, BookOpen, Notebook, NotebookOff
}

def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    icons_dir = project_root / 'src' / 'icons'
    svgs_dir = project_root / 'svgs'
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
    
    # Update index file
    print("\n" + "=" * 60)
    print("Updating index file...")
    
    # Read existing index
    index_file = project_root / 'src' / 'index.ts'
    existing_exports = set()
    if index_file.exists():
        content = index_file.read_text()
        # Extract existing exports
        export_pattern = r"export\s+\{\s*(\w+),\s*type\s+\w+Props\s*\}\s+from\s+'\./icons/\w+';"
        for match in re.finditer(export_pattern, content):
            existing_exports.add(match.group(1))
    
    # Add new exports
    new_exports = []
    for component_name in sorted(all_components.keys()):
        if component_name not in existing_exports:
            new_exports.append(f"export {{ {component_name}, type {component_name}Props }} from './icons/{component_name}';")
    
    if new_exports:
        # Append to existing index
        with open(index_file, 'a') as f:
            f.write('\n' + '\n'.join(new_exports) + '\n')
        print(f"✓ Updated index.ts with {len(new_exports)} new components")
    else:
        print("✓ No new components to add to index")
    
    print("\n" + "=" * 60)
    print(f"✓ Successfully generated {len(all_components)} icon components!")
    print(f"✓ SVG source files saved to svgs/ directory (GitHub as source of truth)")
    print("\nNote: If some SVGs failed to fetch, make sure Figma is running")
    print("      and the localhost server is accessible.")
    print("      SVG files are now stored in the repo for future reference.")

if __name__ == '__main__':
    main()

