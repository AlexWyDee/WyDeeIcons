#!/usr/bin/env python3
"""
Extract SVG content from existing React components and save to svgs/ directory.
This makes GitHub the source of truth for SVG files.
"""

import re
import json
from pathlib import Path

def extract_svg_from_component(component_file):
    """Extract SVG variants from a React component file."""
    content = component_file.read_text()
    
    # Find the SVG_VARIANTS object - match the entire object including multi-line strings
    # Pattern: const SVG_VARIANTS: Record<string, string> = { ... };
    pattern = r"const SVG_VARIANTS: Record<string, string> = \{([\s\S]*?)\};"
    match = re.search(pattern, content)
    
    if not match:
        return {}
    
    variants_text = match.group(1)
    variants = {}
    
    # Extract each variant - they're in format: 'key': "value",
    # Handle escaped quotes and newlines
    variant_pattern = r"'([^']+)':\s*\"([^\"]*(?:\\.[^\"]*)*)\""
    
    for match in re.finditer(variant_pattern, variants_text):
        variant_key = match.group(1)
        svg_content = match.group(2)
        
        # Unescape the content (handle \n, \", etc.)
        # Use JSON decoding for proper unescaping
        try:
            # Wrap in quotes and decode as JSON string
            svg_content = json.loads('"' + svg_content + '"')
        except:
            # Fallback: manual unescaping
            svg_content = svg_content.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
        
        variants[variant_key] = svg_content
    
    return variants

def save_svg_file(component_name, variant_key, svg_content, svgs_dir):
    """Save SVG content to file, wrapping in <svg> tags if needed."""
    if not svg_content or not svg_content.strip():
        return None
    
    # Ensure svgs_dir exists first
    svgs_dir.mkdir(parents=True, exist_ok=True)
    component_dir = svgs_dir / component_name
    component_dir.mkdir(parents=True, exist_ok=True)
    
    # Sanitize variant key for filename (replace / with -)
    safe_variant_key = variant_key.replace('/', '-')
    svg_file = component_dir / f'{safe_variant_key}.svg'
    
    # If the content doesn't start with <svg>, wrap it
    if not svg_content.strip().startswith('<svg'):
        # Check if it starts with <g> or <path> - these need wrapping
        if svg_content.strip().startswith('<'):
            svg_content = f'<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">{svg_content}</svg>'
        else:
            # Just path data, wrap in svg
            svg_content = f'<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="{svg_content}"/></svg>'
    
    svg_file.write_text(svg_content)
    return svg_file

def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    icons_dir = project_root / 'src' / 'icons'
    svgs_dir = project_root / 'svgs'
    
    svgs_dir.mkdir(parents=True, exist_ok=True)
    
    print("Extracting SVG content from existing components...")
    print("=" * 60)
    
    component_files = sorted(icons_dir.glob('*.tsx'))
    total_svgs = 0
    
    for component_file in component_files:
        component_name = component_file.stem
        print(f"\nProcessing {component_name}...")
        
        variants = extract_svg_from_component(component_file)
        
        if not variants:
            print(f"  ⚠ No SVG variants found")
            continue
        
        saved_count = 0
        for variant_key, svg_content in variants.items():
            if svg_content and svg_content.strip():  # Only save non-empty SVGs
                saved_file = save_svg_file(component_name, variant_key, svg_content, svgs_dir)
                if saved_file:
                    saved_count += 1
                    total_svgs += 1
        
        if saved_count > 0:
            print(f"  ✓ Saved {saved_count} SVG variants to svgs/{component_name}/")
        else:
            print(f"  ⚠ No valid SVG content found")
    
    print("\n" + "=" * 60)
    print(f"✓ Successfully extracted {total_svgs} SVG files!")
    print(f"✓ SVG files saved to svgs/ directory (GitHub as source of truth)")

if __name__ == '__main__':
    main()
