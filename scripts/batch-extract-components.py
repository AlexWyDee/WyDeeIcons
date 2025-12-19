#!/usr/bin/env python3
"""
Batch extract component data from multiple Figma design context outputs.
This script processes design context code and extracts all component data.
"""

import re
import json
import sys
from pathlib import Path

def extract_component_data(figma_code):
    """Extract component data from Figma-generated React code."""
    # Extract all imgVector URLs
    img_vector_pattern = r'const\s+imgVector(\d*)\s*=\s*"([^"]+)"'
    img_vectors = {}
    for match in re.finditer(img_vector_pattern, figma_code):
        index = match.group(1) or '0'
        url = match.group(2)
        img_vectors[index] = url
    
    # Find component name
    component_name_match = re.search(r'type\s+(\w+)Props', figma_code)
    if not component_name_match:
        return None
    
    component_name = component_name_match.group(1)
    
    # Find function
    func_pattern = rf'(?:export\s+default\s+)?function\s+{component_name}\s*\([^)]*\)\s*{{'
    func_match = re.search(func_pattern, figma_code)
    
    if not func_match:
        return None
    
    func_start = func_match.end()
    next_func = figma_code.find('function ', func_start)
    if next_func == -1:
        func_body = figma_code[func_start:]
    else:
        func_body = figma_code[func_start:next_func]
    
    variants = {}
    
    # Extract variant mappings
    variant_pattern = r'if\s*\(fill\s*===\s*"(\w+)"\s*&&\s*style\s*===\s*"(\w+)"\)'
    
    for var_match in re.finditer(variant_pattern, func_body):
        fill = var_match.group(1)
        style = var_match.group(2)
        
        variant_start = var_match.end()
        variant_end = func_body.find('if ', variant_start)
        if variant_end == -1:
            variant_end = func_body.find('return', variant_start)
        
        variant_code = func_body[variant_start:variant_end]
        
        # Find first imgVector in variant
        img_vector_match = re.search(r'imgVector(\d*)', variant_code)
        if img_vector_match:
            vector_index = img_vector_match.group(1) or '0'
            if vector_index in img_vectors:
                url = img_vectors[vector_index]
                variant_key = f'{fill}-{style}'
                variants[variant_key] = url
    
    # Default return (Outline-Sharp)
    default_match = re.search(r'return\s*\([^)]*imgVector(\d*)', func_body)
    if default_match:
        vector_index = default_match.group(1) or '0'
        if vector_index in img_vectors:
            url = img_vectors[vector_index]
            if 'Outline-Sharp' not in variants:
                variants['Outline-Sharp'] = url
    
    if variants:
        return {
            'name': component_name,
            'metadata': {'name': component_name},
            'variants': variants
        }
    
    return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python batch-extract-components.py <figma-code-file1> [<figma-code-file2> ...]")
        sys.exit(1)
    
    all_components = {}
    
    for file_path in sys.argv[1:]:
        with open(file_path, 'r') as f:
            figma_code = f.read()
        
        component_data = extract_component_data(figma_code)
        if component_data:
            all_components[component_data['name']] = {
                'metadata': component_data['metadata'],
                'variants': component_data['variants']
            }
            print(f"✓ Extracted {component_data['name']}", file=sys.stderr)
        else:
            print(f"✗ Could not extract from {file_path}", file=sys.stderr)
    
    print(json.dumps(all_components, indent=2))

