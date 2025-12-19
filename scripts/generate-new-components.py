#!/usr/bin/env python3
"""
Generate React icon components from Figma SVG URLs for new keyboard icons.
Handles both components with 3 variants (filled="N/A") and 9 variants (fill prop).
"""

import urllib.request
import urllib.error
import json
import os
import re
from pathlib import Path

# Component data extracted from Figma design context
# Components with filled="N/A" have only 3 variants (Sharp, Soft, Round)
# Components with fill prop have 9 variants (Outline/Solid/Tonal × Sharp/Soft/Round)
COMPONENT_DATA = {
    # Components with 3 variants (filled="N/A")
    'Tab': {
        'metadata': {'name': 'Tab'},
        'variants': {
            'N/A-Sharp': 'http://localhost:3845/assets/bacc55e2ce9dc246a3dfb9e50368f6774231a07e.svg',
            'N/A-Soft': 'http://localhost:3845/assets/bacc55e2ce9dc246a3dfb9e50368f6774231a07e.svg',
            'N/A-Round': 'http://localhost:3845/assets/bacc55e2ce9dc246a3dfb9e50368f6774231a07e.svg',
        },
        'hasFill': False
    },
    'Alt': {
        'metadata': {'name': 'Alt'},
        'variants': {
            'N/A-Sharp': 'http://localhost:3845/assets/ab406ba6e35444799191987ecff1977a5e1b88ab.svg',
            'N/A-Soft': 'http://localhost:3845/assets/9119bae35e59c75f23d502fcef414b1729eb38cd.svg',
            'N/A-Round': 'http://localhost:3845/assets/496a0ae93d7861414ee56900a1288a3f7b995909.svg',
        },
        'hasFill': False
    },
    'Control': {
        'metadata': {'name': 'Control'},
        'variants': {
            'N/A-Sharp': 'http://localhost:3845/assets/018245717f8226aaf7dc94a11528ec11a34f23ac.svg',
            'N/A-Soft': 'http://localhost:3845/assets/5e08db328fd98a61c436fb2eae958d0b3c903e25.svg',
            'N/A-Round': 'http://localhost:3845/assets/1967c670e3b4521a83b6a61da884cf6bbe95c4d3.svg',
        },
        'hasFill': False
    },
    'Option': {
        'metadata': {'name': 'Option'},
        'variants': {
            'N/A-Sharp': 'http://localhost:3845/assets/72d381bd0d1fa4e969bbb599ee6ab1b975474d27.svg',
            'N/A-Soft': 'http://localhost:3845/assets/5498ca8fe6ae55d37160914e3ea918b8625cc4d3.svg',
            'N/A-Round': 'http://localhost:3845/assets/37aaa95b7ba95f3cfd8a40c7bd7429f1f033ffcf.svg',
        },
        'hasFill': False
    },
    'Shift': {
        'metadata': {'name': 'Shift'},
        'variants': {
            'N/A-Sharp': 'http://localhost:3845/assets/abc8ce1310e8992aa072170b694b0524c599098d.svg',
            'N/A-Soft': 'http://localhost:3845/assets/c4915523ad6990d60e7faaa7db465ee70475b909.svg',
            'N/A-Round': 'http://localhost:3845/assets/ddc4c5209c7e857b4f08651ecd1b614fa7285db9.svg',
        },
        'hasFill': False
    },
    'Command': {
        'metadata': {'name': 'Command'},
        'variants': {
            'N/A-Sharp': 'http://localhost:3845/assets/7c2ad827df5160d7efd4ba4a8182cd0d4fcced32.svg',
            'N/A-Soft': 'http://localhost:3845/assets/302d5c5275e7e623c46a265cd2d1a0cd9b32b317.svg',
            'N/A-Round': 'http://localhost:3845/assets/221b43810dcabd47761449df45e7c9094dbf06a8.svg',
        },
        'hasFill': False
    },
    'OptionKey': {
        'metadata': {'name': 'Option Key'},
        'variants': {
            'N/A-Sharp': 'http://localhost:3845/assets/ca65db33a31f68d3030becaac65934d1342dace3.svg',
            'N/A-Soft': 'http://localhost:3845/assets/bc0b9526719718f13aedad391214569d19cd62f6.svg',
            'N/A-Round': 'http://localhost:3845/assets/771dd44caba488bbad552af047a1ad3318193480.svg',
        },
        'hasFill': False
    },
    'OptionKey1': {
        'metadata': {'name': 'Option Key 1'},
        'variants': {
            'N/A-Sharp': 'http://localhost:3845/assets/2503b2123d5b654026a437afc637a8df85f1fc91.svg',
            'N/A-Soft': 'http://localhost:3845/assets/589f317f72db1c0a54d416d85c1ebc3b85559b0c.svg',
            'N/A-Round': 'http://localhost:3845/assets/02c601c09a610a30147e47129598ec919c888f73.svg',
        },
        'hasFill': False
    },
    'ShiftKey': {
        'metadata': {'name': 'Shift Key'},
        'variants': {
            'N/A-Sharp': 'http://localhost:3845/assets/d5354bf07364752fe487fc8bcd7382824d4006ee.svg',
            'N/A-Soft': 'http://localhost:3845/assets/af90869e49fa82c50e899d46722a372c060ec400.svg',
            'N/A-Round': 'http://localhost:3845/assets/fb58bcaf7baae3ae009219c6a2607ac583d30bfd.svg',
        },
        'hasFill': False
    },
    'CommandKey': {
        'metadata': {'name': 'Command Key'},
        'variants': {
            'N/A-Sharp': 'http://localhost:3845/assets/2865bb02c440c69c8fc8e1468ee10cc1d8ca09b3.svg',
            'N/A-Soft': 'http://localhost:3845/assets/cc9358d33bffc985f759d6e11f2ce18d2ec09a23.svg',
            'N/A-Round': 'http://localhost:3845/assets/f653fb6e22641ba77f61aa3fd2191f4f81ad5016.svg',
        },
        'hasFill': False
    },
    # Components with 9 variants (fill prop)
    'FunctionKeyBox': {
        'metadata': {'name': 'Function Key Box'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/10f8cfe9071e5dc8891c44f8299abcadc5147d73.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/8c12db92c93112cf6af4a87d93cdc30ac7cdaefb.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/8bfbfe72f04a261c47a195c38e4a8f976067fa4d.svg',
            'Outline-Soft': 'http://localhost:3845/assets/130dc7c3518097bf447ca30192070ef28f316207.svg',
            'Solid-Soft': 'http://localhost:3845/assets/1016b28235ad7af7d3bbde3fff91838fb6bd42e0.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/a0817214e4abf20b043d95026be28dcd7b249a1d.svg',
            'Outline-Round': 'http://localhost:3845/assets/eb23493440c7a64c5a022b2ccc869ad3acb45fef.svg',
            'Solid-Round': 'http://localhost:3845/assets/2e4c17371f90f362f78734ed8957935972cdc5a3.svg',
            'Tonal-Round': 'http://localhost:3845/assets/70a7810b2810743e896fce3017b6b05a56bd9f11.svg',
        },
        'hasFill': True
    },
    'ControlKeyBox': {
        'metadata': {'name': 'Control Key Box'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/203f1c10fd8e6022bcb4f41c366eca10076d74f8.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/1badd6ddd6530b5f8215a19d41f2790f9c4e7199.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/43ea688df4659db9b2ac374c19634ea8c03abdfd.svg',
            'Outline-Soft': 'http://localhost:3845/assets/ba89e974c8706eea5c82b9e0dc881d1830a851db.svg',
            'Solid-Soft': 'http://localhost:3845/assets/3a6d432452496f01767d2e1b22702c9196d7915e.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/8a1700e058c30f65147e334b74663dfde001ffc1.svg',
            'Outline-Round': 'http://localhost:3845/assets/0ddc0efd5e6a91f5b83996ab30437e595d774be2.svg',
            'Solid-Round': 'http://localhost:3845/assets/ae1ee6500b88ea581bb916c381b0e74bd9d80785.svg',
            'Tonal-Round': 'http://localhost:3845/assets/9c25a6bfc1f9a7122633be3bc64ae56ff3643a7b.svg',
        },
        'hasFill': True
    },
    'OptionKeyBox': {
        'metadata': {'name': 'Option Key Box'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/a15caa49e5d1db8f0aa7c3e69cf42a3cb04ff62b.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/69184b78ec7bdb9e54e70fb77922fe95b0e70072.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/91b9e0ab526b891773bb4163bd3d3f4b93675cfb.svg',
            'Outline-Soft': 'http://localhost:3845/assets/f7f13e24b1bfe9908b2fd9894e2c3e49dde83bc2.svg',
            'Solid-Soft': 'http://localhost:3845/assets/28ec5bd726085f1438e453f7ac1f4d5f03a78863.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/e00c96c3f6f581d3c63d507763808588bc513ed5.svg',
            'Outline-Round': 'http://localhost:3845/assets/df9ef138546e3999bdf4326a24eede538bb1392e.svg',
            'Solid-Round': 'http://localhost:3845/assets/6ed9459e827447508104e14e95eb73258af43ce7.svg',
            'Tonal-Round': 'http://localhost:3845/assets/1d479cb3a5859755eb3bd7692e5221adbc3105bb.svg',
        },
        'hasFill': True
    },
    'ShiftKeyBox': {
        'metadata': {'name': 'Shift Key Box'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/12181e87891258e1957438658f77ece2657e4eb5.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/e67f4d08f4f4b3724dd88d4e4e47f4c6541e3d6a.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/acf9abd9729e109797a9cb850b440101c5a5050e.svg',
            'Outline-Soft': 'http://localhost:3845/assets/a1ea6029538de2000d6c7a5a3d7ec6e562f368aa.svg',
            'Solid-Soft': 'http://localhost:3845/assets/e9272cfedf26f347d8ba11e95ff09b6b2324d3b2.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/f6dd099f1a4300704f575a7361886ab0b839096d.svg',
            'Outline-Round': 'http://localhost:3845/assets/45cf737a6e5d2e6851a897d3818235b835634759.svg',
            'Solid-Round': 'http://localhost:3845/assets/3012917be0f9cd32e89990f2223942010ec94d14.svg',
            'Tonal-Round': 'http://localhost:3845/assets/a29dc129f64011f6b6e18a33c33f91c2ff455d87.svg',
        },
        'hasFill': True
    },
    'MacCommandKey': {
        'metadata': {'name': 'Mac Command Key'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/80ccaf319fa46bc50d1b903bdc9bcf18a60344a7.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/8203ffd77aac3effda67e1799ec764e2d5f606ec.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/f7c861ab54dd8c7cb8280be81ae241c8719f85d4.svg',
            'Outline-Soft': 'http://localhost:3845/assets/d8503e2d4b74a9f0719ebe38d30de78dbbf5bd63.svg',
            'Solid-Soft': 'http://localhost:3845/assets/cb5d0b75aec114248c7b128c7b83a4da59fb6a59.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/a76eef7887e8cd52da032c27cd425998e272caea.svg',
            'Outline-Round': 'http://localhost:3845/assets/01831fe3e3aac92f3c3c1c6f6dbb6c2cc21cf2bb.svg',
            'Solid-Round': 'http://localhost:3845/assets/2adc2065c4ab6ddeb0e9a88d7a30d89e582b65a1.svg',
            'Tonal-Round': 'http://localhost:3845/assets/0f1f31027ac8b8a8c03202b5f54642dee0be288f.svg',
        },
        'hasFill': True
    },
    'CommandKeyBox': {
        'metadata': {'name': 'Command Key Box'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/8b648d95481ecd91bcb35b557337714d5258ada6.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/5a2cc15b2b6c0aee4511a363a7f136aeca9cf445.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/9f2869d5258b1788356415ee99a176f98c32acf8.svg',
            'Outline-Soft': 'http://localhost:3845/assets/a7aaa42d42eac6d01442f4e33b68cd29d03512c6.svg',
            'Solid-Soft': 'http://localhost:3845/assets/9f3b397b03579cec486a1bd2575a040fde375dec.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/f0d08134f36864f851d777e9ae75f30ca6949528.svg',
            'Outline-Round': 'http://localhost:3845/assets/58537e131e9dbd4efca870292ff45ff19894fe63.svg',
            'Solid-Round': 'http://localhost:3845/assets/25c2cc4d0761b94928c027b20ee70286b5283639.svg',
            'Tonal-Round': 'http://localhost:3845/assets/85b05199d6cb808aa59f4a6734b021c98e8aed63.svg',
        },
        'hasFill': True
    },
    'SpacebarKeyBox': {
        'metadata': {'name': 'Spacebar Key Box'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/9fb6c26ecefaa1c225cf5c796008660fc3281171.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/1f0940240ce51eec287a3bb4c1d14e42a071276c.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/58fd578beb48ddeffadb5360baea498ad8e1a598.svg',
            'Outline-Soft': 'http://localhost:3845/assets/b749c24cd380e24490acb56d0ff4b165961614af.svg',
            'Solid-Soft': 'http://localhost:3845/assets/0739f7c7ef97695b0d7ec3f00219f4041b0eb08a.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/c15ddff92baaa726ca4821dccdc2610321be97f6.svg',
            'Outline-Round': 'http://localhost:3845/assets/8e17dd2a43ec88437ecd941e35d9bc57bf551d51.svg',
            'Solid-Round': 'http://localhost:3845/assets/fbaac953f25af962c47d95a9913c47697915c8b4.svg',
            'Tonal-Round': 'http://localhost:3845/assets/2d4e8bf5ed365d2adfcfd41e251227dcfb1f4b37.svg',
        },
        'hasFill': True
    },
    'TabKeyBox': {
        'metadata': {'name': 'Tab Key Box'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/7529ff58e0d12ac7c7bbde9249e3c5c98790acee.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/90d828da00dbe73fe84871551bbb84bb45a1cb71.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/050349b961b558c0e6ab0f02bdfea23ac4a1bc4e.svg',
            'Outline-Soft': 'http://localhost:3845/assets/8070a7b22117fc7f2669faadc975fe3227f4f551.svg',
            'Solid-Soft': 'http://localhost:3845/assets/dff244899eb4de46f702ffb8c92562dd2d606413.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/867b05fa4ddd2d502a3096ece66c3eb7ad189071.svg',
            'Outline-Round': 'http://localhost:3845/assets/97922d6777324bae190833d76c41d27a59a70bad.svg',
            'Solid-Round': 'http://localhost:3845/assets/f8a26a46095862dfed6b68859d42e0dd78df1bb2.svg',
            'Tonal-Round': 'http://localhost:3845/assets/c7422f81e8228f0d6f958fa3580165a4ebff4d64.svg',
        },
        'hasFill': True
    },
    'AltKeyBox': {
        'metadata': {'name': 'Alt Key Box'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/a7b4d72a18821332152c47aca695072e7e22e5e8.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/b0a9e4905f3d73daa00aebf26b963ec2b173f1ed.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/f3e212053ec9a50ab57998591b64166795de7c3e.svg',
            'Outline-Soft': 'http://localhost:3845/assets/68b4e898f4c70515515061a1346bb949dd6b73e2.svg',
            'Solid-Soft': 'http://localhost:3845/assets/66a87f51cf9727a04f019556f21218300fbb23ed.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/3a56a5071eb1f426dcf688ab1231cf457c23b854.svg',
            'Outline-Round': 'http://localhost:3845/assets/4b72d7d1df0199a8841367834b479e32cd32d508.svg',
            'Solid-Round': 'http://localhost:3845/assets/5a55fcb2edcbcbe671ae6c9f909c58d727f3eb7e.svg',
            'Tonal-Round': 'http://localhost:3845/assets/d417193a5cd8c71831f58148b33521198864866e.svg',
        },
        'hasFill': True
    },
    'ControlKeyBox1': {
        'metadata': {'name': 'Control Key Box 1'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/73e5f2b0e82e5c92046a7b1469241636abba894c.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/3b3985f25a4470c1e6be4b178a481275546c4cf8.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/4b12ba6060537403736baf455b2b9a9d38c53872.svg',
            'Outline-Soft': 'http://localhost:3845/assets/021c7c26bceeee784767b3f836437c808827d69b.svg',
            'Solid-Soft': 'http://localhost:3845/assets/11de26863031381f70407d91ef08b659a6d95578.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/83ca0ac6730ad6eba18345275c7b2f312bd16c14.svg',
            'Outline-Round': 'http://localhost:3845/assets/d01f40f8fc7f2c678e8534452631508905b65efa.svg',
            'Solid-Round': 'http://localhost:3845/assets/e56e16c7bffb88a7cec108b96abef39bbe952a2c.svg',
            'Tonal-Round': 'http://localhost:3845/assets/32a63bdee1f78e2966cb28a7e8d79dbfb8c6211f.svg',
        },
        'hasFill': True
    },
    'OptionalKeyBox': {
        'metadata': {'name': 'Optional Key Box'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/69852ad82c7a2c87f0652a978b8fcf98a41d0bc8.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/69c562760edae5026a98fb67a8e27160c8775e66.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/351e1f87ec1b6710d532eb763c350d5b3d9e56d7.svg',
            'Outline-Soft': 'http://localhost:3845/assets/ec9a14d8c6c14a176aec3cf33eb2717205daa925.svg',
            'Solid-Soft': 'http://localhost:3845/assets/3f26b7a71083e6275409dd53a0353a0e58ff05f7.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/13d6a22468a997f235ca02c0d778a02b04208b79.svg',
            'Outline-Round': 'http://localhost:3845/assets/4a6516bec6fc20794b29d302abe799a28d2fe11f.svg',
            'Solid-Round': 'http://localhost:3845/assets/2449028cca33b7e205f9433db05245dce94b3487.svg',
            'Tonal-Round': 'http://localhost:3845/assets/4fa521680f54ac291320220349fac47936fefa32.svg',
        },
        'hasFill': True
    },
    'ShiftKeyBox1': {
        'metadata': {'name': 'Shift Key Box 1'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/cf8cb1980ff7d75379674259c2f86c54e469ada3.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/5cd29d917df53ce76a21164aff3fe7b3f095fe80.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/0331b07a08957ecc5723ad197c397ed2cb5cc3be.svg',
            'Outline-Soft': 'http://localhost:3845/assets/a0cb04aec9a10fa2363d9fb80f9a70c3edbeb095.svg',
            'Solid-Soft': 'http://localhost:3845/assets/79839a4423e288562552f7df02352f6fa0d8f0c3.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/8d17ce39d0cdb2f9125d021c797ada327a34177d.svg',
            'Outline-Round': 'http://localhost:3845/assets/60c0383420134530ec697fe72d9654525858c8f3.svg',
            'Solid-Round': 'http://localhost:3845/assets/250209761305ca357f2445b57369c5d77b055f2c.svg',
            'Tonal-Round': 'http://localhost:3845/assets/d012699e7e42cdfe77dfd2c067720bf8f29a66be.svg',
        },
        'hasFill': True
    },
    'CommandKeyBox1': {
        'metadata': {'name': 'Command Key Box 1'},
        'variants': {
            'Outline-Sharp': 'http://localhost:3845/assets/b18184ad34c3b68ff60de6dd1843d8e2593d079e.svg',
            'Solid-Sharp': 'http://localhost:3845/assets/6c31682db70df109d6a1d13b35210b27f3b04210.svg',
            'Tonal-Sharp': 'http://localhost:3845/assets/de7e3acafe924ab164c06b28a53566fb98561f5c.svg',
            'Outline-Soft': 'http://localhost:3845/assets/ad787e42a842d647a1d56e39158e58c0567ba24f.svg',
            'Solid-Soft': 'http://localhost:3845/assets/e5926c49d7693016b4dba2fdcdb83416e1cd5781.svg',
            'Tonal-Soft': 'http://localhost:3845/assets/d29048a7f1da5511544f58fc77e76d565cfb32fd.svg',
            'Outline-Round': 'http://localhost:3845/assets/1626ebe448e3b226068be599ab4832d689b4deb0.svg',
            'Solid-Round': 'http://localhost:3845/assets/ae4b77af109d413442320910ee3be07e26505c19.svg',
            'Tonal-Round': 'http://localhost:3845/assets/bceebbc7173d7fa49e2abc5be57c94d8107ae53e.svg',
        },
        'hasFill': True
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
    has_fill = component_info.get('hasFill', True)
    
    # Build SVG_VARIANTS object
    variants_code = []
    for variant_key in sorted(svg_data.keys()):
        svg_content = svg_data[variant_key]
        # Escape for JavaScript string
        escaped_content = json.dumps(svg_content)
        variants_code.append(f"  '{variant_key}': {escaped_content},")
    
    variants_str = '\n'.join(variants_code)
    
    if has_fill:
        # Component with fill prop (9 variants)
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
    else:
        # Component without fill prop (3 variants, filled="N/A")
        template = f'''import React from 'react';
import {{ Style }} from '../types';

export interface {component_name}Props {{
  className?: string;
  style?: Style;
  size?: number | string;
  'data-component-config'?: string;
}}

const SVG_VARIANTS: Record<string, string> = {{
{variants_str}
}};

export function {component_name}({{ 
  className = '', 
  style = 'Sharp' as Style,
  size = 24,
  'data-component-config': dataComponentConfig,
  ...props 
}}: {component_name}Props) {{
  const variantKey = `N/A-${{style}}`;
  const svgContent = SVG_VARIANTS[variantKey] || SVG_VARIANTS['N/A-Sharp'] || '';

  return (
    <svg
      width={{size}}
      height={{size}}
      viewBox="0 0 24 24"
      fill="currentColor"
      className={{className}}
      data-style={{style}}
      data-component-config={{dataComponentConfig || '{component_config}'}}
      {{...props}}
      dangerouslySetInnerHTML={{{{ __html: svgContent }}}}
    />
  );
}}
'''
    return template

def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    icons_dir = project_root / 'src' / 'icons'
    icons_dir.mkdir(parents=True, exist_ok=True)
    
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
    existing_exports = []
    if index_file.exists():
        content = index_file.read_text()
        # Extract existing exports
        for line in content.split('\n'):
            if line.strip().startswith('export'):
                existing_exports.append(line.strip())
    
    # Add new exports
    new_exports = []
    for component_name in sorted(all_components.keys()):
        export_line = f"export {{ {component_name}, type {component_name}Props }} from './icons/{component_name}';"
        if export_line not in existing_exports:
            new_exports.append(export_line)
    
    # Write updated index
    all_exports = existing_exports + new_exports
    index_content = '''// Auto-generated index file
// Export all icon components

''' + '\n'.join(sorted(set(all_exports))) + '\n'
    
    index_file.write_text(index_content)
    print(f"✓ Updated index.ts with {len(new_exports)} new components")
    
    print("\n" + "=" * 60)
    print(f"✓ Successfully generated {len(all_components)} icon components!")
    print("\nNote: If some SVGs failed to fetch, make sure Figma is running")
    print("      and the localhost server is accessible.")

if __name__ == '__main__':
    main()

