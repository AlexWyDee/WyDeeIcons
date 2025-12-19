import re
import sys

# Read the metadata from stdin or a file
metadata = sys.stdin.read()

# Count component frames (frames with width="136" height="136" that contain symbols)
# These are the frames directly under the Column frame
component_pattern = r'<frame id="[^"]*" name="[^"]*"[^>]*width="136" height="136">'
components = re.findall(component_pattern, metadata)

# Count all symbol elements (variants)
symbol_pattern = r'<symbol id="[^"]*"'
symbols = re.findall(symbol_pattern, metadata)

print(f"Components: {len(components)}")
print(f"Total Variants: {len(symbols)}")


