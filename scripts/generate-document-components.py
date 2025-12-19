#!/usr/bin/env python3
"""
Generate React icon components from Figma for document-related icons.
This script processes components from a Figma frame and generates React components.
"""

import urllib.request
import urllib.error
import json
import os
import re
from pathlib import Path

# Component data extracted from Figma design context
# All components have 9 variants (Outline/Solid/Tonal × Sharp/Soft/Round)
# Component names and their node IDs from the frame
COMPONENT_FRAMES = {
    'CopyFolder': '1:540',
    'CopyFolderOff': '1:525',
    'Bin': '1:861',
    'EditDocument': '131:2408',
    'AddStickyNote': '405:2403',
    'ClipboardText': '1:446',
    'AddToClipboard': '1:459',
    'SearchClipboard': '1:816',
    'ClipboardTimer': '1:836',
    'RemoveFromClipboard': '394:454',
    'PaperNote': '1:687',
    'StickyNote': '1:650',
    'ImportDocument': '1:736',
    'CompressDocument': '1:782',
    'ExportDocument': '1:936',
    'ScanDocument': '1:584',
    'CopyDocument': '1:713',
    'DocumentNotes': '1:675',
    'DocumentNotesOff': '1:658',
    'Newspaper': '1:921',
    'NewspaperOff': '1:903',
    'AddDocument': '1:947',
    'DocumentAlert': '1:975',
    'DocumentOptions': '1:431',
    'DownloadDocument': '1:725',
    'SearchDocument': '1:960',
    'StickyNoteOff': '1:635',
    'Folder': '1:547',
    'FolderOff': '1:570',
    'AddFolder': '1:552',
    'MinimizeFolder': '1:562',
    'CopyDocumentOff': '1:695',
    'Clipboard': '1:515',
    'ClipboardOff': '1:502',
    'ClipboardChart': '1:487',
    'ConfirmClipboard': '1:472',
    'RemoveFolder': '394:622',
    'Page': '1:396',
    'PageOff': '1:750',
    'Document': '1:767',
    'DocumentChart': '1:404',
    'ConfirmDocument': '1:420',
    'Book': '1:4974',
    'BookOpen': '1:5022',
    'Notebook': '1:598',
    'NotebookOff': '1:614',
}

def extract_component_data_from_figma_code(figma_code, component_name):
    """Extract component data from Figma-generated React code."""
    variants = {}
    
    # Extract all imgVector URLs
    img_vector_pattern = r'const\s+imgVector(\d+)\s*=\s*"([^"]+)"'
    img_vectors = {}
    for match in re.finditer(img_vector_pattern, figma_code):
        index = match.group(1)
        url = match.group(2)
        img_vectors[index] = url
        # Also handle imgVector without index (index 0)
        if index == '':
            img_vectors[''] = url
    
    # Pattern to match component function
    component_pattern = rf'type\s+{component_name}Props\s*=\s*{{[^}}]*}};\s*export\s+default\s+function\s+{component_name}\s*\([^)]*\)\s*{{'
    match = re.search(component_pattern, figma_code, re.MULTILINE)
    
    if not match:
        # Try alternative pattern without "export default"
        component_pattern = rf'function\s+{component_name}\s*\([^)]*\)\s*{{'
        match = re.search(component_pattern, figma_code, re.MULTILINE)
    
    if not match:
        return variants
    
    func_start = match.end()
    # Find the end of the function (next function or end of string)
    next_func = figma_code.find('function ', func_start)
    if next_func == -1:
        func_body = figma_code[func_start:]
    else:
        func_body = figma_code[func_start:next_func]
    
    # Extract variant mappings
    # Pattern: if (fill === "Outline" && style === "Sharp")
    variant_pattern = r'if\s*\(fill\s*===\s*"(\w+)"\s*&&\s*style\s*===\s*"(\w+)"\)'
    
    for var_match in re.finditer(variant_pattern, func_body):
        fill = var_match.group(1)
        style = var_match.group(2)
        
        # Find imgVector used in this variant
        variant_start = var_match.end()
        variant_end = func_body.find('if ', variant_start)
        if variant_end == -1:
            variant_end = func_body.find('return', variant_start)
        
        variant_code = func_body[variant_start:variant_end]
        
        # Find imgVector reference (could be imgVector, imgVector1, etc.)
        img_vector_match = re.search(r'imgVector(\d*)', variant_code)
        if img_vector_match:
            vector_index = img_vector_match.group(1) or ''
            if vector_index in img_vectors:
                url = img_vectors[vector_index]
                variant_key = f'{fill}-{style}'
                variants[variant_key] = url
            elif '' in img_vectors:
                # Fallback to imgVector without index
                url = img_vectors['']
                variant_key = f'{fill}-{style}'
                variants[variant_key] = url
    
    # Also check the default return (Outline-Sharp)
    default_match = re.search(r'return\s*\([^)]*imgVector(\d*)', func_body)
    if default_match:
        vector_index = default_match.group(1) or ''
        if vector_index in img_vectors:
            url = img_vectors[vector_index]
            if 'Outline-Sharp' not in variants:
                variants['Outline-Sharp'] = url
        elif '' in img_vectors:
            url = img_vectors['']
            if 'Outline-Sharp' not in variants:
                variants['Outline-Sharp'] = url
    
    return variants

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

def main():
    print("=" * 60)
    print("NOTE: This script requires manual extraction of Figma design context.")
    print("Please run this script after extracting component data from Figma.")
    print("=" * 60)
    print("\nTo extract component data:")
    print("1. Get design context from Figma for each component")
    print("2. Save the React code to a file")
    print("3. Run: python extract-figma-data.py <figma-code-file>")
    print("4. Update COMPONENT_DATA in this script with the extracted data")
    print("\nAlternatively, use generate-components.py with manually extracted data.")

if __name__ == '__main__':
    main()

