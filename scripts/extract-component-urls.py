#!/usr/bin/env python3
"""
Extract component variant URLs from Figma design context code.
Parses the React code output from Figma to extract imgVector URLs and their mappings.
"""

import re
import json
import sys

def extract_component_data(figma_code):
    """Extract component data from Figma-generated React code."""
    components = {}
    
    # Extract all imgVector URLs
    img_vector_pattern = r'const\s+imgVector(\d*)\s*=\s*"([^"]+)"'
    img_vectors = {}
    for match in re.finditer(img_vector_pattern, figma_code):
        index = match.group(1) or '0'  # Empty index means 0
        url = match.group(2)
        img_vectors[index] = url
    
    # Find component name from type definition
    component_name_match = re.search(r'type\s+(\w+)Props', figma_code)
    if not component_name_match:
        return None
    
    component_name = component_name_match.group(1)
    
    # Extract variant mappings from the function
    func_pattern = rf'export\s+default\s+function\s+{component_name}\s*\([^)]*\)\s*{{'
    func_match = re.search(func_pattern, figma_code)
    
    if not func_match:
        # Try without "export default"
        func_pattern = rf'function\s+{component_name}\s*\([^)]*\)\s*{{'
        func_match = re.search(func_pattern, figma_code)
    
    if not func_match:
        return None
    
    func_start = func_match.end()
    # Find the end of the function
    next_func = figma_code.find('function ', func_start)
    if next_func == -1:
        func_body = figma_code[func_start:]
    else:
        func_body = figma_code[func_start:next_func]
    
    variants = {}
    
    # Pattern to match: if (fill === "Outline" && style === "Sharp")
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
        
        # Find imgVector reference - could be imgVector, imgVector1, etc.
        # Look for the first imgVector in the variant code
        img_vector_match = re.search(r'imgVector(\d*)', variant_code)
        if img_vector_match:
            vector_index = img_vector_match.group(1) or '0'
            if vector_index in img_vectors:
                url = img_vectors[vector_index]
                variant_key = f'{fill}-{style}'
                variants[variant_key] = url
    
    # Also check the default return (Outline-Sharp)
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
        print("Usage: python extract-component-urls.py <figma-code-file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        figma_code = f.read()
    
    component_data = extract_component_data(figma_code)
    
    if component_data:
        print(json.dumps({component_data['name']: {
            'metadata': component_data['metadata'],
            'variants': component_data['variants']
        }}, indent=2))
    else:
        print("Could not extract component data", file=sys.stderr)
        sys.exit(1)

